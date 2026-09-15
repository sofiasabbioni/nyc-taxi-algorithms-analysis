import unittest

from src.sorting_algorithms import bubble_sort, merge_sort, quick_sort


class SortingAlgorithmTests(unittest.TestCase):
    def setUp(self):
        self.values = [5, 1, 3, 3, -2, 10, 0]
        self.expected = sorted(self.values)

    def test_bubble_sort(self):
        self.assertEqual(bubble_sort(self.values), self.expected)

    def test_merge_sort(self):
        self.assertEqual(merge_sort(self.values), self.expected)

    def test_quick_sort(self):
        self.assertEqual(quick_sort(self.values), self.expected)

    def test_input_is_not_mutated(self):
        original = self.values.copy()
        bubble_sort(self.values)
        merge_sort(self.values)
        quick_sort(self.values)
        self.assertEqual(self.values, original)


if __name__ == "__main__":
    unittest.main()
