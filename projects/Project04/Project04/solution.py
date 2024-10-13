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
        INSERT DOCSTRINGS HERE!
        """
        return self.size

    def is_empty(self) -> bool:
        """
        INSERT DOCSTRINGS HERE!
        """
        return self.size == 0

    def front_element(self) -> T:
        """
        INSERT DOCSTRINGS HERE!
        """
        return self.queue[self.front] if self.front is not None else None

    def back_element(self) -> T:
        """
        INSERT DOCSTRINGS HERE!
        """
        return self.queue[self.back] if self.back is not None else None

    def enqueue(self, value: T, front: bool = True) -> None:
        """
        INSERT DOCSTRINGS HERE!
        """
        if self.size+1 == self.capacity:
            self.grow()

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

    def dequeue(self, front: bool = True) -> T:
        """
        INSERT DOCSTRINGS HERE!
        """
        if self.size-1 <= self.capacity//4 and self.capacity//2 >= 4:
            self.shrink()

        if self.front is None or self.back == None or self.size == 0:
            return None

        self.size -= 1        
        if front:
            item = self.queue[self.front]
            self.front += 1
            if self.front > self.capacity-1:
                self.front = 0
            return item
        else:
            item = self.queue[self.back]
            self.back -= 1
            if self.back < 0:
                self.back = self.capacity-1
            return item

    def grow(self) -> None:
        """
        INSERT DOCSTRINGS HERE!
        """
        self.capacity *= 2
        new_queue = [None] * self.capacity
        if self.back is not None and self.front is not None:
            if self.back > self.front:
                new_queue[:self.front+self.back+1] = self.queue[self.front:self.back+1]
            else:
                new_queue[:self.size] = self.queue[self.front:] + self.queue[:self.back+1]
            self.front = 0
            self.back = self.size-1

        self.queue = new_queue

    def shrink(self) -> None:
        """
        INSERT DOCSTRINGS HERE!
        """
        self.capacity //= 2
        self.capacity = max(self.capacity, 4)
        new_queue = [None] * self.capacity
        if self.back is not None and self.front is not None:
            if self.back > self.front:
                new_queue[:self.front+self.back+1] = self.queue[self.front:self.back+1]
            else:
                new_queue[:self.size] = self.queue[self.front:] + self.queue[:self.back+1]
            self.front = 0
            self.back = self.size-1

        self.queue = new_queue


def get_winning_numbers(numbers: List[int], size: int) -> List[int]:
    """
    INSERT DOCSTRINGS HERE!
    """
    pass
    


def get_winning_probability(winning_numbers: List[int]) -> int:
    """
    INSERT DOCSTRINGS HERE!
    """
    pass

