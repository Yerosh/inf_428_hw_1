import numpy as np
import unittest

def generate_random_data(mean, variance, num_samples):
    return np.random.randint(max(mean - variance, 0), min(mean + variance + 1, 90), num_samples)

def calculate_department_mean_score(threat_scores):
    return np.mean(threat_scores)

def calculate_aggregated_threat_score(department_scores, department_importance):
    weighted_sum = sum(mean * importance for mean, importance in zip(department_scores, department_importance))
    total_importance = sum(department_importance)
    return min(max(weighted_sum / total_importance, 0), 90)  # Ensure result is within 0-90 range

class TestThreatScoreAnalytics(unittest.TestCase):

    # Test 1: This test checks whether the mean threat score calculated for a department is within the valid range of 0 to 90
    def test_calculate_department_mean_score(self):
        data = generate_random_data(50, 10, 100)
        mean_score = calculate_department_mean_score(data)
        self.assertTrue(0 <= mean_score <= 90, "Mean score should be within range 0-90.")

    # Test 2: This test evaluates the calculation of an aggregated threat score based on the mean scores of multiple departments and their importance weights
    def test_calculate_aggregated_threat_score(self):
        department_scores = [50, 60, 55, 45, 65]
        department_importance = [1, 2, 3, 4, 5]
        aggregated_score = calculate_aggregated_threat_score(department_scores, department_importance)
        self.assertTrue(0 <= aggregated_score <= 90, "Aggregated score should be within range 0-90.")

    # Test 3: All departments have equal threat scores and equal importance
    def test_equal_department_weights(self):
        data = [generate_random_data(50, 5, 100) for _ in range(5)]
        mean_scores = [calculate_department_mean_score(d) for d in data]
        importance = [1] * 5
        agg_score = calculate_aggregated_threat_score(mean_scores, importance)
        self.assertAlmostEqual(agg_score, 50, delta=5, msg="Score should be around the mean of 50.")

    # Test 4: Some departments are more important than others
    def test_varying_department_importance(self):
        data = [generate_random_data(30, 10, 100), generate_random_data(70, 10, 100)]
        mean_scores = [calculate_department_mean_score(d) for d in data]
        importance = [1, 5]
        agg_score = calculate_aggregated_threat_score(mean_scores, importance)
        self.assertTrue(agg_score > 50, "Higher importance department should skew the score towards its mean.")

    # Test 5: Large differences in the number of users per department
    def test_large_user_variance(self):
        data = [generate_random_data(50, 10, 10), generate_random_data(70, 10, 200)]
        mean_scores = [calculate_department_mean_score(d) for d in data]
        importance = [3, 3]
        agg_score = calculate_aggregated_threat_score(mean_scores, importance)
        self.assertTrue(50 <= agg_score <= 70, "Score should reflect the larger user base department more.")

    # Test 6: All departments have a threat score of 0
    def test_no_threat_in_all_departments(self):
        data = [[0] * 100 for _ in range(5)]
        mean_scores = [calculate_department_mean_score(d) for d in data]
        importance = [3, 2, 1, 4, 5]
        agg_score = calculate_aggregated_threat_score(mean_scores, importance)
        self.assertEqual(agg_score, 0, "Score should be 0 if all department scores are 0.")

    # Test 7: All departments have maximum threat score
    def test_max_threat_in_all_departments(self):
        data = [[90] * 100 for _ in range(5)]
        mean_scores = [calculate_department_mean_score(d) for d in data]
        importance = [1, 2, 3, 4, 5]
        agg_score = calculate_aggregated_threat_score(mean_scores, importance)
        self.assertEqual(agg_score, 90, "Score should be 90 if all department scores are at max.")

if __name__ == "__main__":
    unittest.main()
