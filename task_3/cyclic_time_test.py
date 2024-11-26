import unittest
import math

def calculate_time_difference(hour1, hour2):
    # Convert hours to angles in radians
    angle1 = hour1 * (2 * math.pi / 24)
    angle2 = hour2 * (2 * math.pi / 24)

    # Calculate the absolute angular difference
    angular_diff = abs(angle2 - angle1)

    # The cyclic angular difference
    cyclic_diff = 2 * math.pi - angular_diff

    # Convert back to hours and return the minimum difference
    return min(angular_diff, cyclic_diff) * (24 / (2 * math.pi))


class TestCyclicTime(unittest.TestCase):

    # Test 1: Testing for a direct difference without crossing midnight
    def test_direct_difference(self):
        self.assertEqual(calculate_time_difference(1, 3), 2)
        self.assertEqual(calculate_time_difference(5, 8), 3)

    # Test 2: Testing difference crossing midnight
    def test_midnight_crossing_difference(self):
        self.assertAlmostEqual(calculate_time_difference(23, 1), 2, places=6)
        self.assertAlmostEqual(calculate_time_difference(22, 2), 4, places=6)

    # Test 3: Testing difference for the same hour
    def test_same_time_difference(self):
        self.assertEqual(calculate_time_difference(12, 12), 0)

    # Test 4: Testing opposite points on the clock
    def test_opposite_hours(self):
        self.assertEqual(calculate_time_difference(0, 12), 12)
        self.assertEqual(calculate_time_difference(6, 18), 12)

    # Test 5: Testing boundary cases like 0 and 24
    def test_boundary_cases(self):
        self.assertAlmostEqual(calculate_time_difference(0, 23), 1, places=6)
        self.assertAlmostEqual(calculate_time_difference(0, 24), 0, places=6)


if __name__ == "__main__":
    unittest.main()
