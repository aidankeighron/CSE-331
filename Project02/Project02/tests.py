"""
Project 2 - Hybrid Sorting - Tests
CSE 331 Fall 2024
"""

from collections.abc import MutableSequence
from collections import defaultdict
from random import sample, seed, shuffle
import unittest

from solution import (selection_sort, bubble_sort, insertion_sort, hybrid_merge_sort, recommend_products, Product)

seed(331)


# Custom comparator used in all comprehensive testcases
def sum_digits(n: int):
    """Computes the sum of all digits in a number"""
    return sum(int(digit) for digit in str(n))


# Custom comparator used in all comprehensive testcases
def comp_sum_digits(x: int, y: int):
    """Compares two numbers by the sum of their digits"""
    return sum_digits(x) < sum_digits(y)


class Project2Tests(unittest.TestCase):

    def test_selection_sort_basic(self):
        # (1) test with basic list of integers - default comparator
        data = [7, 4, 1, 0, 8, 9, 3, 2, 12]
        expected = sorted(data)
        selection_sort(data)
        self.assertEqual(expected, data)

        # (2) test with basic list of strings - default comparator
        data = ["dog", "banana", "orange", "tree", "clutter", "candy", "silence"]
        expected = sorted(data)
        selection_sort(data)
        self.assertEqual(expected, data)

        # (3) test with already sorted data - default comparator
        data = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        expected = sorted(data)
        selection_sort(data)
        self.assertEqual(expected, data)

        # (4) test empty
        data = []
        selection_sort(data)
        self.assertEqual([], data)

        # (5) check that function does not return anything
        data = [5, 6, 3, 2]
        self.assertIsNone(selection_sort(data))

    def test_selection_sort_comparator(self):
        # (1) sort powers of ten by number of digits, in reverse
        data = [10 ** i for i in range(15)]
        shuffle(data)
        expected = sorted(data, key=lambda x: -1 * len(str(x)))
        selection_sort(data, comparator=lambda x, y: len(str(x)) > len(str(y)))
        self.assertEqual(expected, data)

        # (2) sort strings by length
        data = ['a' * i for i in range(15)]
        shuffle(data)
        expected = sorted(data, key=lambda x: len(x))
        selection_sort(data, comparator=lambda x, y: len(x) < len(y))
        self.assertEqual(expected, data)

    def test_selection_sort_descending(self):
        # (1) sort powers of ten by number of digits, in reverse
        data = [10 ** i for i in range(15)]
        shuffle(data)
        expected = sorted(data, key=lambda x: len(str(x)), reverse=True)
        selection_sort(data, comparator=lambda x, y: len(str(x)) < len(str(y)), descending=True)
        self.assertEqual(expected, data)

        # (2) sort strings by length
        data = ['a' * i for i in range(15)]
        shuffle(data)
        expected = sorted(data, key=lambda x: len(x), reverse=True)
        selection_sort(data, comparator=lambda x, y: len(x) < len(y), descending=True)
        self.assertEqual(expected, data)

    def test_selection_sort_comprehensive(self):
        # (1) sort a lot of integers
        data = list(range(1500))
        shuffle(data)
        expected = sorted(data)
        selection_sort(data)
        self.assertEqual(expected, data)

        # (2) sort a lot of integers with alternative comparator
        # this comparator compares values as follows:
        #   x < y
        #   if and only if
        #   sum(digits(x)) < sum(digits(y))
        # ex: 12 < 15 since 1 + 2 = 3 < 6 = 1 + 5
        data = list(range(1500))
        expected_data = sorted(data, key=sum_digits)
        selection_sort(data, comparator=comp_sum_digits)
        # there are multiple possible orderings, thus we must compare via sums of digits
        for expected, actual in zip(expected_data, data):
            expected_sum = sum_digits(expected)
            actual_sum = sum_digits(actual)
            self.assertEqual(expected_sum, actual_sum)

    def test_bubble_sort_basic(self):
        # (1) test with basic list of integers - default comparator
        data = [7, 4, 1, 0, 8, 9, 3, 2, 12]
        expected = sorted(data)
        bubble_sort(data)
        self.assertEqual(expected, data)

        # (2) test with basic list of strings - default comparator
        data = ["dog", "banana", "orange", "tree", "clutter", "candy", "silence"]
        expected = sorted(data)
        bubble_sort(data)
        self.assertEqual(expected, data)

        # (3) test with already sorted data - default comparator
        data = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        expected = sorted(data)
        bubble_sort(data)
        self.assertEqual(expected, data)

        # (4) test empty
        data = []
        bubble_sort(data)
        self.assertEqual([], data)

        # (5) check that function does not return anything
        data = [5, 6, 3, 2]
        self.assertIsNone(bubble_sort(data))

    def test_bubble_sort_comparator(self):
        # (1) sort powers of ten by number of digits, in reverse
        data = [10 ** i for i in range(15)]
        shuffle(data)
        expected = sorted(data, key=lambda x: -1 * len(str(x)))
        bubble_sort(data, comparator=lambda x, y: len(str(x)) > len(str(y)))
        self.assertEqual(expected, data)

        # (2) sort strings by length
        data = ['a' * i for i in range(15)]
        shuffle(data)
        expected = sorted(data, key=lambda x: len(x))
        bubble_sort(data, comparator=lambda x, y: len(x) < len(y))
        self.assertEqual(expected, data)

    def test_bubble_sort_descending(self):
        # (1) sort powers of ten by number of digits, in reverse
        data = [10 ** i for i in range(15)]
        shuffle(data)
        expected = sorted(data, key=lambda x: len(str(x)), reverse=True)
        bubble_sort(data, comparator=lambda x, y: len(str(x)) < len(str(y)), descending=True)
        self.assertEqual(expected, data)

        # (2) sort strings by length
        data = ['a' * i for i in range(15)]
        shuffle(data)
        expected = sorted(data, key=lambda x: len(x), reverse=True)
        bubble_sort(data, comparator=lambda x, y: len(x) < len(y), descending=True)
        self.assertEqual(expected, data)

    def test_bubble_sort_comprehensive(self):
        # (1) sort a lot of integers
        # Smaller than the other comprehensive tests; bubble sort is slow!
        data = list(range(500))
        shuffle(data)
        expected = sorted(data)
        bubble_sort(data)
        self.assertEqual(expected, data)

        # (2) sort a lot of integers with alternative comparator
        # this comparator compares values as follows:
        #   x < y
        #   if and only if
        #   sum(digits(x)) < sum(digits(y))
        # ex: 12 < 15 since 1 + 2 = 3 < 6 = 1 + 5
        data = list(range(500))
        expected_data = sorted(data, key=sum_digits)
        bubble_sort(data, comparator=comp_sum_digits)
        # there are multiple possible orderings, thus we must compare via sums of digits
        for expected, actual in zip(expected_data, data):
            expected_sum = sum_digits(expected)
            actual_sum = sum_digits(actual)
            self.assertEqual(expected_sum, actual_sum)

    def test_insertion_sort_basic(self):
        # (1) test with basic list of integers - default comparator
        data = [7, 4, 1, 0, 8, 9, 3, 2, 12]
        expected = sorted(data)
        insertion_sort(data)
        self.assertEqual(expected, data)

        # (2) test with basic list of strings - default comparator
        data = ["dog", "banana", "orange", "tree", "clutter", "candy", "silence"]
        expected = sorted(data)
        insertion_sort(data)
        self.assertEqual(expected, data)

        # (3) test with already sorted data - default comparator
        data = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        expected = sorted(data)
        insertion_sort(data)
        self.assertEqual(expected, data)

        # (4) test empty
        data = []
        insertion_sort(data)
        self.assertEqual([], data)

        # (5) check that function does not return anything
        data = [5, 6, 3, 2]
        self.assertIsNone(insertion_sort(data))

    def test_insertion_sort_comparator(self):
        # (1) sort powers of ten by number of digits, in reverse
        data = [10 ** i for i in range(15)]
        shuffle(data)
        expected = sorted(data, key=lambda x: -1 * len(str(x)))
        insertion_sort(data, comparator=lambda x, y: len(str(x)) > len(str(y)))
        self.assertEqual(expected, data)

        # (2) sort strings by length
        data = ['a' * i for i in range(15)]
        shuffle(data)
        expected = sorted(data, key=lambda x: len(x))
        insertion_sort(data, comparator=lambda x, y: len(x) < len(y))
        self.assertEqual(expected, data)

    def test_insertion_sort_descending(self):
        # (1) sort powers of ten by number of digits, in reverse
        data = [10 ** i for i in range(15)]
        shuffle(data)
        expected = sorted(data, key=lambda x: len(str(x)), reverse=True)
        insertion_sort(data, comparator=lambda x, y: len(str(x)) < len(str(y)), descending=True)
        self.assertEqual(expected, data)

        # (2) sort strings by length
        data = ['a' * i for i in range(15)]
        shuffle(data)
        expected = sorted(data, key=lambda x: len(x), reverse=True)
        insertion_sort(data, comparator=lambda x, y: len(x) < len(y), descending=True)
        self.assertEqual(expected, data)

    def test_insertion_sort_comprehensive(self):
        # (1) sort a lot of integers
        data = list(range(1500))
        shuffle(data)
        expected = sorted(data)
        insertion_sort(data)
        self.assertEqual(expected, data)

        # (2) sort a lot of integers with alternative comparator
        # this comparator compares values as follows:
        #   x < y
        #   if and only if
        #   sum(digits(x)) < sum(digits(y))
        # ex: 12 < 15 since 1 + 2 = 3 < 6 = 1 + 5
        data = list(range(1500))
        expected_data = sorted(data, key=sum_digits)
        insertion_sort(data, comparator=comp_sum_digits)
        # there are multiple possible orderings, thus we must compare via sums of digits
        for expected, actual in zip(expected_data, data):
            expected_sum = sum_digits(expected)
            actual_sum = sum_digits(actual)
            self.assertEqual(expected_sum, actual_sum)

    def test_hybrid_merge_sort_basic(self):
        # (1) test with basic list of integers - default comparator and threshold
        data = [7, 4, 1, 0, 8, 9, 3, 2, 12]
        expected = sorted(data)
        hybrid_merge_sort(data)
        self.assertEqual(expected, data)

        # (2) test with basic set of strings - default comparator and threshold
        data = ["dog", "banana", "orange", "tree", "clutter", "candy", "silence"]
        expected = sorted(data)
        hybrid_merge_sort(data)
        self.assertEqual(expected, data)

        # (3) test with already sorted data - default comparator and threshold
        data = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        expected = sorted(data)
        hybrid_merge_sort(data)
        self.assertEqual(expected, data)

        # (4) test empty - default comparator and threshold
        data = []
        hybrid_merge_sort(data)
        self.assertEqual([], data)

        # (5) check that function does not return anything
        data = [5, 6, 3, 2]
        self.assertIsNone(hybrid_merge_sort(data, threshold=0))

    def test_hybrid_merge_sort_threshold(self):
        # first, all the tests from basic should work with higher thresholds

        # (1) test with basic list of integers - default comparator
        data = [7, 4, 1, 0, 8, 9, 3, 2, 12]
        expected = sorted(data)
        hybrid_merge_sort(data, threshold=2)
        self.assertEqual(expected, data)

        # (2) test with basic set of strings - default comparator
        data = ["dog", "banana", "orange", "tree", "clutter", "candy", "silence"]
        expected = sorted(data)
        hybrid_merge_sort(data, threshold=2)
        self.assertEqual(expected, data)

        # (3) test with already sorted data - default comparator
        data = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        expected = sorted(data)
        hybrid_merge_sort(data, threshold=2)
        self.assertEqual(expected, data)

        # (4) now, for a longer test - a bunch of thresholds
        data = list(range(25))
        expected = sorted(data)
        for t in range(11):
            shuffle(data)
            hybrid_merge_sort(data, threshold=t)
            self.assertEqual(expected, data)

    def test_hybrid_merge_sort_comparator(self):
        # (1) sort powers of ten by number of digits, in reverse
        data = [10 ** i for i in range(15)]
        shuffle(data)
        expected = sorted(data, key=lambda x: -1 * len(str(x)))
        hybrid_merge_sort(data, comparator=lambda x, y: len(str(x)) > len(str(y)))
        self.assertEqual(expected, data)

        # (2) sort strings by length
        data = ['a' * i for i in range(15)]
        shuffle(data)
        expected = sorted(data, key=lambda x: len(x))
        hybrid_merge_sort(data, comparator=lambda x, y: len(x) < len(y))
        self.assertEqual(expected, data)

    def test_hybrid_merge_sort_descending(self):
        # (1) test with basic list of integers - default comparator, threshold of zero
        data = [7, 4, 1, 0, 8, 9, 3, 2, 12]
        expected = sorted(data, reverse=True)
        hybrid_merge_sort(data, threshold=0, descending=True)
        self.assertEqual(expected, data)

        # (2) test with basic list of strings - default comparator, threshold
        data = ["dog", "banana", "orange", "tree", "clutter", "candy", "silence"]
        expected = sorted(data, reverse=True)
        hybrid_merge_sort(data, threshold=0, descending=True)
        self.assertEqual(expected, data)

        # (3) test with already sorted data - default comparator, threshold
        data = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        expected = sorted(data, reverse=True)
        hybrid_merge_sort(data, threshold=0, descending=True)
        self.assertEqual(expected, data)

        # (4) test empty
        data = []
        hybrid_merge_sort(data, threshold=0, descending=True)
        self.assertEqual([], data)

        # (5) check that function does not return anything
        data = [5, 6, 3, 2]
        self.assertIsNone(hybrid_merge_sort(data, threshold=0, descending=True))

        # (6) now let's test with multiple thresholds
        data = list(range(50))
        expected = sorted(data, reverse=True)
        for t in range(20):
            shuffle(data)
            hybrid_merge_sort(data, threshold=t, descending=True)
            self.assertEqual(expected, data)

    def test_hybrid_merge_sort_comprehensive(self):
        # (1) sort a lot of integers, with a lot of thresholds
        data = list(range(500))
        for t in range(100):
            shuffle(data)
            expected = sorted(data)
            hybrid_merge_sort(data, threshold=t)
            self.assertEqual(expected, data)

        # (2) sort a lot of integers with alternative comparator, threshold of 8
        # this comparator compares values as follows:
        #   x < y
        #   if and only if
        #   sum(digits(x)) < sum(digits(y))
        # ex: 12 < 15 since 1 + 2 = 3 < 6 = 1 + 5
        data = list(range(1500))
        expected_data = sorted(data, key=sum_digits)
        hybrid_merge_sort(data, threshold=8, comparator=comp_sum_digits)
        # there are multiple possible orderings, thus we must compare via sums of digits
        for expected, actual in zip(expected_data, data):
            expected_sum = sum_digits(expected)
            actual_sum = sum_digits(actual)
            self.assertEqual(expected_sum, actual_sum)

        # (3) sort a lot of integers with same comparator as above, thresholds in [1, ..., 49]
        # this comparator compares values as follows:
        #   x < y
        #   if and only if
        #   sum(digits(x)) < sum(digits(y))
        # ex: 12 < 15 since 1 + 2 = 3 < 6 = 1 + 5
        data = list(range(1000))
        expected_data = sorted(data, key=sum_digits)
        for t in range(50):
            shuffle(data)
            hybrid_merge_sort(data, threshold=t, comparator=comp_sum_digits)
            for expected, actual in zip(expected_data, data):
                expected_sum = sum_digits(expected)
                actual_sum = sum_digits(actual)
                self.assertEqual(expected_sum, actual_sum)

    def test_hybrid_merge_sort_speed(self):
        # *********************************************************
        # ***WORTH NO POINTS, FOR PERSONAL TESTING PURPOSES ONLY***
        # *********************************************************
        # the point of this sort is to be fast, right?
        # this (probably) won't finish if you're not careful with time complexity,
        # but it isn't guaranteed
        data = list(range(300000))
        expected = data[:]
        shuffle(data)
        hybrid_merge_sort(data)
        self.assertEqual(expected, data)

    def test_hybrid_merge_actually_hybrid(self):
        # *********************************************************
        # ***WORTH NO POINTS, FOR PERSONAL TESTING PURPOSES ONLY***
        # *********************************************************
        # this test is to make sure that the hybrid merge sort is actually
        # hybrid by calling insertion sort when appropriate

        calling_functions = defaultdict(set)

        class MyList(MutableSequence):
            # This class was taken from
            # https://stackoverflow.com/questions/6560354/how-would-i-create-a-custom-list-class-in-python
            def __init__(self, data=None):
                super(MyList, self).__init__()
                self._list = list(data)

            def __delitem__(self, ii):
                """Delete an item"""
                del self._list[ii]

            def __setitem__(self, ii, val):
                self._list[ii] = val

            def insert(self, ii, val):
                self._list.insert(ii, val)

            def __len__(self):
                """List length"""
                return len(self._list)

            def __getitem__(self, ii):
                import inspect
                calling_functions[inspect.stack()[1].function].add(len(self))
                if isinstance(ii, slice):
                    return self.__class__(self._list[ii])
                else:
                    return self._list[ii]

        data = MyList(range(50))
        hybrid_merge_sort(data, threshold=2)
        self.assertIn('insertion_sort', calling_functions)
        self.assertIn('hybrid_merge_sort_inner', calling_functions)
        self.assertTrue(all(length <= 2 for length in calling_functions['insertion_sort']))
        self.assertAlmostEqual(len(calling_functions['hybrid_merge_sort_inner']), 10, delta=2)

    def test_recommend_products(self):
        # (1) Empty product list.
        products = []
        expected = []
        actual = recommend_products(products, 'price_low_to_high')
        self.assertEqual(expected, actual)
        actual = recommend_products(products, 'price_high_to_low')
        self.assertEqual(expected, actual)
        actual = recommend_products(products, 'rating')
        self.assertEqual(expected, actual)

        # (2) Sort 10 products by price from low to high. No products share the same price.
        products = [Product(10, 1, 1),
                    Product(20, 3, 2),
                    Product(30, 5, 4),
                    Product(10, 5, 3),
                    Product(20, 5, 7),
                    Product(30, 5, 5),
                    Product(10, 5, 6),
                    Product(10, 1, 8),
                    Product(20, 5, 9),
                    Product(30, 3, 10)]

        expected = [Product(10, 1, 8),
                    Product(20, 5, 9),
                    Product(30, 3, 10)]
        actual = recommend_products(products, 'price_low_to_high')
        self.assertEqual(expected, actual)

        # (4) Sort the same 10 products by price from high to low. No products share the same price.
        expected = [Product(30, 3, 10),
                    Product(20, 5, 9),
                    Product(10, 1, 8)]
        actual = recommend_products(products, 'price_high_to_low')
        self.assertEqual(expected, actual)

        # (5) Sort the same 10 products by rating. No products share the same rating.
        expected = [Product(20, 5, 9),
                    Product(30, 3, 10),
                    Product(10, 1, 8)]
        actual = recommend_products(products, 'rating')
        self.assertEqual(expected, actual)

        # (6) Sort 10 products by price from low to high. Two products share the same price.
        products = [Product(10, 1, 1),
                    Product(20, 3, 2),
                    Product(30, 5, 4),
                    Product(10, 5, 3),
                    Product(20, 5, 7),
                    Product(30, 5, 5),
                    Product(10, 5, 6),
                    Product(10, 1, 8),
                    Product(20, 5, 9),
                    Product(10, 3, 10)]

        expected = [Product(10, 3, 10),
                    Product(10, 1, 8),
                    Product(20, 5, 9)]
        actual = recommend_products(products, 'price_low_to_high')
        self.assertEqual(expected, actual)

        # (7) Sort the same 10 products by price from high to low. Two products share the same price.
        expected = [Product(20, 5, 9),
                    Product(10, 3, 10),
                    Product(10, 1, 8)]
        actual = recommend_products(products, 'price_high_to_low')
        self.assertEqual(expected, actual)

        # (8) Sort 10 products by rating. Two products share the same rating.
        products = [Product(10, 1, 1),
                    Product(20, 3, 2),
                    Product(30, 5, 4),
                    Product(10, 5, 3),
                    Product(20, 5, 7),
                    Product(30, 5, 5),
                    Product(10, 5, 6),
                    Product(10, 1, 8),
                    Product(7, 4, 9),
                    Product(40, 4, 10)]

        expected = [Product(7, 4, 9),
                    Product(40, 4, 10),
                    Product(10, 1, 8)]
        actual = recommend_products(products, 'rating')
        self.assertEqual(expected, actual)

        # (9) Sort a longer list of products by price from low to high.
        products = [Product(0, 0, 0) for _ in range(50)]
        prices = sample(range(1, 1001), 50)
        for i in range(50):
            products[i].relevance = i
            products[i].rating = i // 10
            products[i].price = prices[i]
        expected = sorted(products[35:], key=lambda p: (p.price, -p.rating))
        actual = recommend_products(products, 'price_low_to_high')
        self.assertEqual(expected, actual)

        # (10) Sort a longer list of products by price from high to low.
        products = [Product(0, 0, 0) for _ in range(50)]
        prices = sample(range(1, 1001), 50)
        for i in range(50):
            products[i].relevance = i
            products[i].rating = 5 - i // 10
            products[i].price = prices[i]
        expected = sorted(products[35:], key=lambda p: (-p.price, -p.rating))
        actual = recommend_products(products, 'price_high_to_low')
        self.assertEqual(expected, actual)

        # (11) Sort a longer list of products by rating.
        products = [Product(0, 0, 0) for _ in range(50)]
        prices = sample(range(1, 1001), 50)
        for i in range(50):
            products[i].relevance = i
            products[i].rating = i // 10
            products[i].price = prices[i]
        expected = sorted(products[35:], key=lambda p: (-p.rating, p.price))
        actual = recommend_products(products, 'rating')
        self.assertEqual(expected, actual)


if __name__ == '__main__':
    unittest.main()
