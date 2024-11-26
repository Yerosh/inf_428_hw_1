import os
import numpy as np
import pandas as pd
from elasticsearch import Elasticsearch
import unittest

# Connection to Elasticsearch
es = Elasticsearch([{'host': 'localhost', 'port': 9200, 'scheme': 'http'}])

def generate_random_data(mean, variance, num_samples):
    return np.random.randint(max(mean - variance, 0), min(mean + variance + 1, 90), num_samples)

def save_to_csv(data, filename):
    pd.DataFrame(data).to_csv(filename, index=False)

def load_from_csv(filename):
    return pd.read_csv(filename).values.tolist()

# Populate Elasticsearch index with data
def populate_elasticsearch_index(index_name, data):
    if not es.indices.exists(index=index_name):
        es.indices.create(index=index_name, body={
            "mappings": {
                "properties": {
                    "score": {"type": "integer"}
                }
            }
        })
    for i, value in enumerate(data):
        es.index(index=index_name, id=i, body={"score": value})

# Fetch all data from an Elasticsearch index
def fetch_from_elasticsearch_index(index_name):
    res = es.search(index=index_name, body={"query": {"match_all": {}}, "size": 10000})

    return [int(hit["_source"]["score"]) for hit in res['hits']['hits']]

def calculate_department_mean_score(threat_scores):
    return np.mean(threat_scores)

def calculate_overall_threat_score(department_scores):
    return np.mean(department_scores)

# Unit tests
class TestThreatScoreAnalytics(unittest.TestCase):

    @classmethod
    # Generate or load test data from .csv
    def setUpClass(cls):
        cls.filename = "threat_scores.csv"
        if not os.path.exists(cls.filename):
            cls.data = [generate_random_data(50, 10, 100) for _ in range(5)]
            save_to_csv(cls.data, cls.filename)
        else:
            cls.data = load_from_csv(cls.filename)
        cls.index_name = "threat_scores"
        for i, department_data in enumerate(cls.data):
            index_name = f"{cls.index_name}_{i}"
            populate_elasticsearch_index(index_name, department_data)
        cls.elasticsearch_indices = [f"{cls.index_name}_{i}" for i in range(len(cls.data))]

    
    @classmethod
    # Clean up indices after tests finish
    def tearDownClass(cls):
        for index in cls.elasticsearch_indices + ["high_score_department", "outlier_department", "small_department",
                                                  "large_department"]:
            if es.indices.exists(index=index):
                es.indices.delete(index=index)

    def test_similar_department_scores(self):
        department_scores = [calculate_department_mean_score(fetch_from_elasticsearch_index(index)) for index in self.elasticsearch_indices]
        overall_score = calculate_overall_threat_score(department_scores)
        self.assertTrue(40 <= overall_score <= 60, "Overall score should be in the mid-range for similar department scores.")

    def test_one_high_score_department(self):
        department_scores = []
        for index in self.elasticsearch_indices:
            scores = fetch_from_elasticsearch_index(index)
            department_scores.append(calculate_department_mean_score(scores))
        high_department = generate_random_data(85, 5, 300)
        populate_elasticsearch_index("high_score_department", high_department)
        high_department_score = calculate_department_mean_score(fetch_from_elasticsearch_index("high_score_department"))
        department_scores.append(high_department_score)
        overall_score = calculate_overall_threat_score(department_scores)
        self.assertTrue(overall_score > max(department_scores[:-1]),
                        "Overall score should be higher than any non-high-scoring department.")

    def test_outlier_users_in_department(self):
        outlier_department = generate_random_data(50, 10, 100).tolist() + [90] * 10
        populate_elasticsearch_index("outlier_department", outlier_department)
        department_score = calculate_department_mean_score(fetch_from_elasticsearch_index("outlier_department"))
        self.assertTrue(department_score > 50, "Department score should reflect the influence of outliers.")

    def test_varying_user_count(self):
        small_department = generate_random_data(50, 10, 50)
        large_department = generate_random_data(50, 10, 5000)
        populate_elasticsearch_index("small_department", small_department)
        populate_elasticsearch_index("large_department", large_department)
        small_score = calculate_department_mean_score(fetch_from_elasticsearch_index("small_department"))
        large_score = calculate_department_mean_score(fetch_from_elasticsearch_index("large_department"))
        self.assertTrue(abs(large_score - 50) < abs(small_score - 50), "Larger department should have a more stable mean score.")

if __name__ == "__main__":
    unittest.main()
