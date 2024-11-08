"""
CSE331 Project 4 FS24
Circular Double-Ended Queue
solution.py
"""

from typing import TypeVar, List

T = TypeVar('T')


class CircularDeque:
    """
    Representation of a Circular Deque using an underlying python list
    """

    __slots__ = ['capacity', 'size', 'queue', 'front', 'back']

    def __init__(self, data: List[T] = None, front: int = 0, capacity: int = 4):
        """
        Initializes an instance of a CircularDeque
        :param data: starting data to add to the deque, for testing purposes
        :param front: where to begin the insertions, for testing purposes
        :param capacity: number of slots in the Deque
        """
        if data is None and front != 0:
            data = ['Start']  # front will get set to 0 by a front enqueue if the initial data is empty
        elif data is None:
            data = []

        self.capacity: int = capacity
        self.size: int = len(data)
        self.queue: List[T] = [None] * capacity
        self.back: int = (self.size + front - 1) % self.capacity if data else None
        self.front: int = front if data else None

        for index, value in enumerate(data):
            self.queue[(index + front) % capacity] = value

    def __str__(self) -> str:
        """
        Provides a string representation of a CircularDeque
        'F' indicates front value
        'B' indicates back value
        :return: the instance as a string
        """
        if self.size == 0:
            return "CircularDeque <empty>"

        str_list = ["CircularDeque <"]
        for i in range(self.capacity):
            str_list.append(f"{self.queue[i]}")
            if i == self.front:
                str_list.append('(F)')
            elif i == self.back:
                str_list.append('(B)')
            if i < self.capacity - 1:
                str_list.append(',')

        str_list.append(">")
        return "".join(str_list)

    __repr__ = __str__

    #
    # Your code goes here!
    #
    def __len__(self) -> int:
        """
        Gets the length of the deque
        :return: length 
        """
        return self.size

    def is_empty(self) -> bool:
        """
        Checks if the deque is empty
        :return: True is empty else False
        """
        return self.size == 0

    def front_element(self) -> T:
        """
        Gets the frontmost element of the deque
        :return: Front element
        """
        return self.queue[self.front] if self.front is not None else None

    def back_element(self) -> T:
        """
        Gets the backmost element of the deque
        :return: Last element
        """
        return self.queue[self.back] if self.back is not None else None

    def enqueue(self, value: T, front: bool = True) -> None:
        """
        Adds ane element to the deque
        :param value: Element to add
        :param front: If true adds to the front of the deque else adds to the back
        :return: None
        """
        self.size += 1
        if self.front is None or self.back is None:
            self.front = 0
            self.back = 0
            self.queue[0] = value
            return

        if front:
            self.front -= 1
            if self.front < 0:
                self.front = self.capacity-1
            
            self.queue[self.front] = value              
        else:
            self.back += 1
            if self.back > self.capacity-1:
                self.back = 0
            self.queue[self.back] = value

        if self.size == self.capacity:
            self.grow()

    def dequeue(self, front: bool = True) -> T:
        """
        Remove an item from the deque     
        :param front: If True removes from the front else removes from the back
        :return: Removed element
        """
        if self.front is None or self.back == None or self.size == 0:
            return None

        self.size -= 1        
        if front:
            item = self.queue[self.front]
            # self.queue[self.front] = None
            self.front += 1
            if self.front > self.capacity-1:
                self.front = 0
        else:
            item = self.queue[self.back]
            # self.queue[self.back] = None
            self.back -= 1
            if self.back < 0:
                self.back = self.capacity-1

        if self.size <= self.capacity/4 and self.capacity//2 >= 4:
            self.shrink()
        return item

    def grow(self) -> None:
        """
        Doubles the size of the deque remapping all existing values
        :return: None
        """
        self.capacity *= 2
        new_queue = [None] * self.capacity
        if self.back is not None and self.front is not None:
            if self.back > self.front:
                new_queue[:self.back-self.front+1] = self.queue[self.front:self.back+1]
            else:
                new_queue[:self.size] = self.queue[self.front:] + self.queue[:self.back+1]
            self.front = 0
            self.back = self.size-1

        self.queue = new_queue

    def shrink(self) -> None:
        """
        Cuts the size of the deque in half remapping all existing values
        :return: None
        """
        self.capacity //= 2
        self.capacity = max(self.capacity, 4)
        new_queue = [None] * self.capacity
        if self.back is not None and self.front is not None:
            if self.back > self.front: 
                new_queue[:self.back-self.front+1] = self.queue[self.front:self.back+1]
            else:
                new_queue[:self.size] = self.queue[self.front:] + self.queue[:self.back+1]
            self.front = 0
            self.back = self.size-1

        self.queue = new_queue


def get_winning_numbers(numbers: List[int], size: int) -> List[int]:
    """
    Gets winning lottery numbers given a list of numbers and the length of the sliding window buy finding the max element at each window
    :param numbers: List of numbers
    :param size: Size of the sliding window
    :return: List of winning lottery numbers
    """
    if not numbers:
        return []
    
    deque = CircularDeque(data=[])
    winning_numbers = []

    for i in range(len(numbers)):
        if not deque.is_empty() and deque.front_element() <= i-size:
            deque.dequeue()

        while not deque.is_empty() and numbers[deque.back_element()] < numbers[i]:
            deque.dequeue(front=False)

        deque.enqueue(i, front=False)

        if i >= size-1:
             winning_numbers.append(numbers[deque.front_element()])

    return winning_numbers

def get_winning_probability(winning_numbers: List[int]) -> int:
    """
    REturns the probability of the numbers winning by finding the largest non-adjacent sum
    :param winning_numbers: List of Winning numbers
    :return: Probability of the numbers winning
    """
    if not winning_numbers:
        return 0

    prev1, prev2 = 0, 0

    for num in winning_numbers:
        new_prev1 = max(prev1, prev2+num)
        prev2 = prev1
        prev1 = new_prev1

    return prev1