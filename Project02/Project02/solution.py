"""
Project 2 - Hybrid Sorting
CSE 331 Fall 2024
"""

from typing import TypeVar, List, Callable

T = TypeVar("T")  # represents generic type


# This is an optional helper function but HIGHLY recommended, especially for the application problem!
def do_comparison(first: T, second: T, comparator: Callable[[T, T], bool], descending: bool) -> bool:
    """
    Lets your know whether or not to put first before second flipping order if descending is true

    :param first: first element
    :param second: second element
    :param comparator: lambda expression used for comparison
    :param descending: boolean to sort descending order
    :return: If first should come before second or second before first if descending
    """
    if descending:
        return comparator(second, first)
    return comparator(first, second)


def selection_sort(data: List[T], *, comparator: Callable[[T, T], bool] = lambda x, y: x < y,
                   descending: bool = False) -> None:
    """
    Sorts items by iterating through the list and finding the next element keeping the left part of the list sorted

    :param data: list of data to sort
    :param comparator: lambda expression used for comparison
    :param descending: boolean to sort descending order
    :return: None
    """

    for i in range(len(data)-1):
        smallest = i
        for j in range(i+1, len(data)):
            if do_comparison(data[j], data[smallest], comparator, descending):
                smallest = j
        
        if smallest != i:
            data[i], data[smallest] = data[smallest], data[i]

def bubble_sort(data: List[T], *, comparator: Callable[[T, T], bool] = lambda x, y: x < y,
                descending: bool = False) -> None:
    """
    Repeatedly iterates through the list swapping elements as needed until the list is sorted

    :param data: list of data to sort
    :param comparator: lambda expression used for comparison
    :param descending: boolean to sort descending order
    :return: None
    """
    is_sorted = False
    while not is_sorted:
        is_sorted = True
        for i in range(len(data)-1):
            if do_comparison(data[i+1], data[i], comparator, descending):
                data[i], data[i+1] = data[i+1], data[i]
                is_sorted = False



def insertion_sort(data: List[T], *, comparator: Callable[[T, T], bool] = lambda x, y: x < y,
                   descending: bool = False) -> None:
    """
    Sorts data by keeping unsorted and sorted parts of the list, it pulls an 
    element from the unsorted portion and inserts it into its correct place in 
    the sorted portion

    :param data: list of data to sort
    :param comparator: lambda expression used for comparison
    :param descending: boolean to sort descending order
    :return: None
    """
    for i in range(1, len(data)):
        j = i-1
        temp = data[i]

        while j >= 0 and do_comparison(temp, data[j], comparator, descending):
            data[j+1] = data[j] 
            j -= 1
        
        # element = data.pop(i)
        # data.insert(j+1, element)
        data[j+1] = temp


def hybrid_merge_sort(data: List[T], *, threshold: int = 12,
                      comparator: Callable[[T, T], bool] = lambda x, y: x < y, descending: bool = False) -> None:
    """
    Splits up array into more manageable chunks until it is sorted

    :param data: list of data to sort
    :param comparator: lambda expression used for comparison
    :param descending: boolean to sort descending order
    :return: None
    """

    def merge(left, right):
        result = []
        i = 0
        j = 0

        while i < len(left) and j < len(right):
            if do_comparison(left[i], right[j], comparator, descending):
                result.append(left[i])
                i += 1
            else:
                result.append(right[j])
                j += 1
        
        result.extend(left[i:])
        result.extend(right[j:])

        return result

    def hybrid_merge_sort_inner(data):
        if len(data) <= 1:
            return data
        if len(data) <= threshold:
            insertion_sort(data, comparator=comparator, descending=descending)
            return data
        else:
            midpoint = len(data)//2
            left = hybrid_merge_sort_inner(data[:midpoint])
            right = hybrid_merge_sort_inner(data[midpoint:])

            return merge(left, right)

    data[:] = hybrid_merge_sort_inner(data)


def quicksort(data: List[T]) -> None:
    """
    Sorts a list in place using quicksort
    :param data: Data to sort
    """

    def quicksort_inner(first: int, last: int) -> None:
        """
        Sorts portion of list at indices in interval [first, last] using quicksort

        :param first: first index of portion of data to sort
        :param last: last index of portion of data to sort
        """
        # List must already be sorted in this case
        if first >= last:
            return

        left = first
        right = last

        # Need to start by getting median of 3 to use for pivot
        # We can do this by sorting the first, middle, and last elements
        midpoint = (right - left) // 2 + left
        if data[left] > data[right]:
            data[left], data[right] = data[right], data[left]
        if data[left] > data[midpoint]:
            data[left], data[midpoint] = data[midpoint], data[left]
        if data[midpoint] > data[right]:
            data[midpoint], data[right] = data[right], data[midpoint]
        # data[midpoint] now contains the median of first, last, and middle elements
        pivot = data[midpoint]
        # First and last elements are already on right side of pivot since they are sorted
        left += 1
        right -= 1

        # Move pointers until they cross
        while left <= right:
            # Move left and right pointers until they cross or reach values which could be swapped
            # Anything < pivot must move to left side, anything > pivot must move to right side
            #
            # Not allowing one pointer to stop moving when it reached the pivot (data[left/right] == pivot)
            # could cause one pointer to move all the way to one side in the pathological case of the pivot being
            # the min or max element, leading to infinitely calling the inner function on the same indices without
            # ever swapping
            while left <= right and data[left] < pivot:
                left += 1
            while left <= right and data[right] > pivot:
                right -= 1

            # Swap, but only if pointers haven't crossed
            if left <= right:
                data[left], data[right] = data[right], data[left]
                left += 1
                right -= 1

        quicksort_inner(first, left - 1)
        quicksort_inner(left, last)

    # Perform sort in the inner function
    quicksort_inner(0, len(data) - 1)


###########################################################
# DO NOT MODIFY
###########################################################
class Product:
    """
    Class that represents products.
    """
    __slots__ = ['price', 'rating', 'relevance']

    def __init__(self, price: float, rating: int, relevance: float) -> None:
        """
        Constructor for the Product class.

        :param price: The price of the product.
        :param rating: The rating of the product.
        :param relevance: A score representing how closely the product matches the user's search keywords. A higher value
        indicates a stronger match between the product and the search query.
        :return: None
        """
        self.price = price
        self.rating = rating
        self.relevance = relevance

    def __repr__(self) -> str:
        """
        Represent the Product as a string.

        :return: Representation of the product.
        """
        return str(self)

    def __str__(self) -> str:
        """
        Convert the Product to a string.

        :return: String representation of the product.
        """
        return f'<price: {self.price}, rating: {self.rating}, relevance: {self.relevance}>'

    def __eq__(self, other) -> bool:
        """
        Compare two Product objects for equality based on price and rating.

        :param other: The other Product to compare with.
        :return: True if products are equal, False otherwise.
        """
        return self.price == other.price and self.rating == other.rating and self.relevance == other.relevance


###########################################################
# MODIFY BELOW
###########################################################
def recommend_products(products: List[Product], sorted_by: str) -> List[Product]:
    """
    Selects to 30% of relevant products and sorts them based on sorting method 

    :param products: Products to sort
    :param sorted_by: Sort method to use
    :return: sorted products
    """

    hybrid_merge_sort(products, comparator=lambda x, y: x.relevance < y.relevance, descending=True)
    amount = int(len(products) * 0.3)
    products = products[:amount]

    if sorted_by == 'price_low_to_high':
        hybrid_merge_sort(products, comparator=lambda x, y: x.price < y.price if x.price != y.price else x.rating > y.rating)
    if sorted_by == 'price_high_to_low':
        hybrid_merge_sort(products, comparator=lambda x, y: x.price < y.price if x.price != y.price else x.rating < y.rating,
                          descending=True)
    if sorted_by == 'rating':
        hybrid_merge_sort(products, comparator=lambda x, y: x.rating < y.rating if x.rating != y.rating else x.price > y.price,
                          descending=True)

    return products
