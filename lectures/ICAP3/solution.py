import unittest


def count_shifts(arr):
    """
    This function should count the number of shifts required to sort the array using insertion sort.
    You need to implement the insertion sort algorithm and count how many shifts happen during sorting.

    Parameters:
    arr (list of int): The array of integers to be sorted

    Returns:
    int: The number of shifts (movements of elements) during sorting
    """
    shifts = 0
    for i in range(1, len(arr)):
        temp = arr[i]
        j = i-1
        while j >= 0 and arr[j] > temp:
            arr[j+1] = arr[j]
            shifts += 1
            j -= 1
        arr[j+1] = temp
            
    return shifts


class TestCountShifts(unittest.TestCase):

    def test_case_1(self):
        arr1 = [6, 7, 3, 9, 2, 9, 3, 4, 2, 8, 8]
        self.assertEqual(count_shifts(arr1), 25)

    def test_case_2(self):
        arr2 = [1, 2, 3, 4, 5]
        self.assertEqual(count_shifts(arr2), 0)

    def test_case_3(self):
        arr2 = [1, 2, 3, 4, 0]
        self.assertEqual(count_shifts(arr2), 4)

    def test_case_4(self):
        arr2 = [5, 4, 3, 2, -1]
        self.assertEqual(count_shifts(arr2), 10)

    def test_case_5(self):
        arr2 = [1, 2]
        self.assertEqual(count_shifts(arr2), 0)

    def test_case_6(self):
        arr2 = [2, 1]
        self.assertEqual(count_shifts(arr2), 1)


# Students need to add 3 more test cases following the same structure as above.

if __name__ == "__main__":
    unittest.main()