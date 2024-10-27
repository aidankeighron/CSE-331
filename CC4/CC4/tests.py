
import solution
import unittest


class TestProgram(unittest.TestCase):
    def test_case_1(self):
        candidates = [[0, 1], [1, 0]]
        teams = [[1, 0], [1, 0]]
        expected = [[0, 0], [1, 1]]
        actual = solution.stable_assignments(candidates, teams)

        # Check if the length of actual matches the expected result
        self.assertTrue(len(actual) == len(expected))

        # Verify each expected match exists in the actual result
        for match in expected:
            contains_match = False
            for actual_match in actual:
                if actual_match[0] == match[0] and actual_match[1] == match[1]:
                    contains_match = True
            self.assertTrue(contains_match)

    def test_case_2(self):
        candidates = [[0, 1, 2], [0, 2, 1], [1, 2, 0]]
        teams = [[2, 1, 0], [0, 1, 2], [0, 1, 2]]
        expected = [[0, 1], [1, 0], [2, 2]]
        actual = solution.stable_assignments(candidates, teams)
        # Check if the length of actual matches the expected result
        self.assertTrue(len(actual) == len(expected))

        # Verify each expected match exists in the actual result
        for match in expected:
            contains_match = False
            for actual_match in actual:
                if actual_match[0] == match[0] and actual_match[1] == match[1]:
                    contains_match = True
            self.assertTrue(contains_match)


if __name__ == "__main__":
    unittest.main()
