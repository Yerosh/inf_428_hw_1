import unittest

def calculate_time_difference(hour1, hour2):

    # Calculate both forward and backward cyclic differences
    forward_diff = abs(hour2 - hour1)
    backward_diff = 24 - forward_diff

    # Return the minimum of the two differences
    return min(forward_diff, backward_diff)


class TestCyclicTime(unittest.TestCase):

    # Test 1: Testing for a direct difference without crossing midnight
    def test_direct_difference(self):
        self.assertEqual(calculate_time_difference(1, 3), 2)
        self.assertEqual(calculate_time_difference(5, 8), 3)

    # Test 2: Testing difference crossing midnight
    def test_midnight_crossing_difference(self):
        self.assertEqual(calculate_time_difference(23, 1), 2)
        self.assertEqual(calculate_time_difference(22, 2), 4)

    # Test 3: Testing difference for the same hour
    def test_same_time_difference(self):
        self.assertEqual(calculate_time_difference(12, 12), 0)

    # Test 4: Testing opposite points on the clock
    def test_opposite_hours(self):
        self.assertEqual(calculate_time_difference(0, 12), 12)
        self.assertEqual(calculate_time_difference(6, 18), 12)

    # Test 5: Testing boundary cases like 0 and 24
    def test_boundary_cases(self):
        self.assertEqual(calculate_time_difference(0, 23), 1)
        self.assertEqual(calculate_time_difference(0, 24), 0)


if __name__ == "__main__":
    unittest.main()
