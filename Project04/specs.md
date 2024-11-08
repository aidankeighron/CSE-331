# Project 4: Circular Double-Ended Queues (Deque)

**Due: Friday October 25th @ 9:00pm pm EST.**
**Please note that this is the only deadline, this is not a soft deadline.**
**Anything after the deadline will be graded with late penalty, please see syllabus for late penalty grade policy.**

\*\*_This is not a team project, do not copy someone else’s work._\*\*

_![CircularDeque.png](img/CircularDeque.png)_

## Assignment Overview

In a typical FIFO (First in First out) queue, elements are added to one end of the underlying structure and removed from the opposite. These are natural for storing sequences of instructions: Imagine that instructions are added to the queue when first processed, and removed when completed. The first instruction processed will also be the first completed - we add it to the front, and remove it from the back.

A deque is a [double-ended queue](https://en.wikipedia.org/wiki/Double-ended_queue), meaning elements can be added or removed from either end of the queue. This generalizes the behavior described above to account for more complex usage scenarios. The ability to add or remove from both ends of the deque allows the structure to be used as both a **FIFO queue and a LIFO stack**, simultaneously.

This structure is useful for storing undo operations, where more recent undoes are pushed and popped from the top of the deque and old/expired undoes are removed from the back of the deque. Trains, consisting of sequences of cars, can also be thought of as deques: cars can be added or removed from either end, but never the middle.

A circular queue is a queue of fixed size with end-to-end connections. This is a way to save memory as deleted elements in the queue can simply be overwritten. In the picture above at index 0, element 1 has been removed (dequeued) from the queue but the value remains. If two new values are enqueued, then that 1 will be overwritten. After this, the circular queue will have reached capacity, and needs to grow.

Circular queues are useful in situations with limited memory. Consider a router in an internet network. A package (a set of bits sent across the network) is sent to this router and it joins the router's processing queue. This router can only hold so many packets before it has to start dropping some. A circular queue would be useful here, as it optimizes memory usage.

A circular deque is a combination of a deque and a circular queue. It sets a max size and can grow and shrink like a circular queue, and it can enqueue/dequeue from both ends.

# Assignment Notes

1. **Manual grading is 30% of the points on this project. Submitted program is checked for its run time for all its functions and space complexity for its add, remove, and the application problem. Space complexity is only required for each project's add, remove and application problem. For these functions where the space complexity is checked, manual grade is split 50-50 for run time and space complexity. Be sure to review the rubric and adhere to complexity requirements!**
   Stacks and Queue ADTs add, remove methods by design already allocate O(N) space.
2. Docstrings (the multi-line comments beneath each function header) are NOT provided and will need to be completed for full credit.
3. Testcases are your friend: before asking about the form of input/output or what happens in a particular edge case, check to see if the testcases answer your question for you. By showing the expected output in response to each input, they supplement the specs provided here.
4. Don't be afraid to go to D2L Course Tools for tutorial videos on how to debug, it will help you figure out where you're going wrong far more quickly than ad-hoc print statements!

# Tips

- The use of [modulo (%)](https://docs.python.org/3/reference/expressions.html#binary-arithmetic-operations) is highly recommended.
- Understand what [amortized runtime](https://medium.com/@satorusasozaki/amortized-time-in-the-time-complexity-of-an-algorithm-6dd9a5d38045) is (also explained below).
- Enqueue and Dequeue both have basic tests which test their functionality in conditions where shrink and grow will not be called. This allows you to test your enqueue and dequeue functions without having to implement grow/shrink.
- Although the API lists enqueue/dequeue first, **it is common to implement grow/shrink and then enqueue/dequeue or grow->enqueue then shrink->dequeue**. The test cases are designed to allow you to implement these functions independently in the order which best suits you.

# Rules:

- The use of Python's Queues library is **NOT ALLOWED** and any use of it will result in a 0 on this project.
- The use of .pop() is **PROHIBITED.**
  - Any function using .pop() will be deducted all points for test cases and manual grading.
  - .pop(x) has a runtime of _O(n-x)_, where _n_ is the length of the python list .pop(x) is called on - in most situations, this will violate time complexity.
- Changing function signatures is not allowed and will result in all points lost for that particular function.
- Docstrings (the multi-line comments beneath each function header) are NOT provided and will need to be completed for full credit..
- Use of the **nonlocal** keyword will result in a 0 on the function is used on.
  - You should never need to use this keyword in this project and if you are using it in a function in this class, you're doing something wrong.

# Assignment Specifications

---

"There's a term for people who don't read the project details: unemployed" -Dr. Owen.

#### class CircularDeque:

_DO NOT MODIFY the following attributes/functions._

- **Attributes**
  - **capacity: int:** the total amount of items that can be placed in your circular deque. Capacity grows and shrinks dynamically, but the capacity is never less than 4. It will always be greater than or equal to **size**.
  - **size: int:** the number of items currently in your circular deque.
  - **queue: list\[T\]:** the underlying structure holding the data of your circular deque. Many elements may be **None** if your current **size** is less than **capacity**. This grows and shrinks dynamically.
  - **front: int:** an index indicating the location of the first element in the circular deque.
  - **back: int:** an index indicating the location of the last element in your circular deque.
- **\_\_init\_\_(self, data: list\[T\], front: int, capacity: int) -> None**
  - Constructs a circular deque.
  - **data: list\[T\]:** a list containing all data to be inserted into the circular deque.
  - **front: int:** an index to offset the front pointer to test the circular behavior of the list without growing.
  - **capacity: int:** the capacity of the circular deque.
  - **Returns:** None.
- **\_\_str\_\_(self) -> str** and **\_\_repr\_\_(self) -> str**
  - Represents the circular deque as a string.
  - **Returns:** str.

_IMPLEMENT the following functions_.

- **\_\_len\_\_(self) -> int**
  - Returns the length/size of the circular deque - this is the number of items currently in the circular deque, and will not necessarily be equal to the **capacity**.
  - This is a [magic method](https://www.tutorialsteacher.com/python/magic-methods-in-python) and can be called with **len(object_to_measure)**.
  - Time complexity: _O(1)_
  - **Returns:** int representing length of the circular deque.
- **is_empty(self) -> bool**
  - Returns a boolean indicating if the circular deque is empty.
  - Time complexity: _O(1)_
  - **Returns:** True if empty, False otherwise.
- **front_element(self) -> T**

  - Returns the first element in the circular deque.
  - Time complexity: _O(1)_

  - **Returns:** the first element if it exists, otherwise None.

- **back_element(self) -> T**
  - Returns the last element in the circular deque.
  - Time complexity: _O(1)_
  - **Returns:** the last element if it exists, otherwise None.
- **enqueue(self, value: T, front: bool = True) -> None:**
  - Add a value to either the front or back of the circular deque based off the parameter **front**.
  - If **front** is true, add the value to the front. Otherwise, add it to the back.
  - Call **grow()** if the size of the list has reached capacity.
  - **param value: T:** value to add into the circular deque.
  - **param value front:** where to add value T.
  - Time complexity: _O(1)\*_
  - Space complexity: _O(1)\*_
  - **Returns:** None
  - (Shouldn't use more than constant time/auxiliary space when **grow() is not called**)
- **dequeue(self, front: bool = True) -> T:**
  - Remove an item from the queue.
  - Removes the front item by default, remove the back item if False is passed in.
  - Calls **shrink()** If the current size is less than or equal to 1/4 the current capacity, and 1/2 the current capacity is greater than or equal to 4, halves the capacity.
  - **param front:** Whether to remove the front or back item from the dequeue.
  - Hint: You shouldn't delete the value from the dequeue (by setting it to None) as that spot will merely be overwritten when you enqueue on that spot so it's more efficient to only adjust the back/front pointer instead.
  - Time complexity: _O(1)\*_
  - Space complexity: _O(1)\*_
  - **Returns:** removed item, None if empty.
  - (Shouldn't use more than constant time/auxiliary space when **shrink() is not called**)
- **grow(self) -> None**
  - Doubles the capacity of CD by creating a new underlying python list with double the capacity of the old one and copies the values over from the current list.
  - The new copied list will be 'unrolled' s.t. the front element will be at index 0 and the tail element will be at index \[size - 1\].
  - Time complexity: _O(N)_
  - Space complexity: _O(N)_
  - **Returns:** None
- **shrink(self) -> None**
  - Cuts the capacity of the queue in half using the same idea as grow. Copy over contents of the old list to a new list with half the capacity.
  - The new copied list will be 'unrolled' s.t. the front element will be at index 0 and the tail element will be at index \[size - 1\].
  - Will never have a capacity lower than 4, **DO NOT** shrink when shrinking would result in a capacity < 4.
  - Time complexity: _O(N)_
  - Space complexity: _O(N)_
  - **Returns:** None

**\*[Amortized](https://medium.com/@satorusasozaki/amortized-time-in-the-time-complexity-of-an-algorithm-6dd9a5d38045)**. _Amortized Time Complexity_ means 'the time complexity a majority of the time'. Suppose a function has amortized time complexity _O(f(n))_ - this implies that the majority of the time the function falls into the complexity class _O(f(n)),_ however, there may exist situations where the complexity exceeds _O(f(n))._ The same logic defines the concept of _Amortized Space Complexity_.

Example: enqueue(self, value: T, front: bool)has an amortized time complexity of _O(1)_: In the majority of situations, enqueueing an element occurs through a constant number of operations. However, when the Circular Deque is at capacity, grow(self) is called - this is an _O(n)_ operation, therefore in this particular scenario, enqueue exceeds its amortized bound.

## Application: Winning Numbers

![](img/lottery.jpg)<br>

While practicing for interviews, you receive a call from a close friend who informs you that they have liquidated all of their assets into the form of lottery tickets. It is a surprise that your friend has made such a rash decision, however, you are determined to help them discover if their investment was a smart decision or a bust. The way the winning numbers are determined is with a sliding window through all the possible numbers on the lottery ticket and extracting the max number from each of the windows at each iteration step. Because of this, knowing how the sliding window technique works is essential for completing this application problem,
so read up on this link https://www.geeksforgeeks.org/window-sliding-technique/.

Your task is to write an algorithm that helps your friend calculate the winning numbers on each of his lottery tickets so that he does not have to do it by hand. The function should take in a list of integers that will represent all the numbers available on the lottery ticket. The function will also take in an integer that represents the size of the sliding window. Your function should return a list of integers that represents the max number from each of the windows
of the sliding window at each iteration step.

- **get_winning_numbers(numbers: List[int], size: int) -> List[int]:**.
  - Takes in a list of numbers and a sliding window size and returns a list containing the maximum value of the sliding window at each iteration step.
  - **param numbers**: A list of numbers that the sliding window will move through.
  - **param size**: The size of the sliding window.
  - **return**: A list containing the max number within the sliding window at each iteration step.
  - **Note**: The sliding window will only move one to the right at a time and the size of the window will be 1 <= size <= len(numbers).
  - Time Complexity: _O(N)_ where n is the total number of numbers in the input list.
  - Space Complexity: _O(N)_

**Your solution should contain usage of the Circular Deque that you implemented. Otherwise you will lose manual grading points on get_winning_numbers() method.**

### Examples

```
        numbers = [1, 3, -1, -3, 5, 3, 6, 7]
        size = 3
        output = get_winning_numbers(numbers, size)
        # output should be [3, 3, 5, 5, 6, 7]

        Explanation:
        The brackets around the numbers represent the window that each iteration is on. For the first
        iteration the window is on [1 3 -1] and the max of that window is 3. It then moves onto [3 -1 -3]
        by sliding the window one to the right, and the max of this window is 3 as well. It continues this
        pattern to produce [3, 3, 5, 5, 6, 7].

                Window                Max
       [1  3  -1] -3  5  3  6  7       3
        1 [3  -1  -3] 5  3  6  7       3
        1  3 [-1  -3  5] 3  6  7       5
        1  3  -1 [-3  5  3] 6  7       5
        1  3  -1  -3 [5  3  6] 7       6
        1  3  -1  -3  5 [3  6  7]      7
```

```
        numbers = [5, 7, 2, 4, -10, -2, 3, 22, 30, 102, -13, 20]
        size = 4
        output = get_winning_numbers(numbers, size)
        # output should be [7, 7, 4, 4, 22, 30, 102, 102, 102]

        Explanation:
                          Window                           Max
       [5  7  2  4] -10  -2  3  22  30  102  -13  20        7
        5 [7  2  4  -10] -2  3  22  30  102  -13  20        7
        5  7 [2  4  -10  -2] 3  22  30  102  -13  20        4
        5  7  2 [4  -10  -2  3] 22  30  102  -13  20        4
        5  7  2  4 [-10  -2  3  22] 30  102  -13  20        22
        5  7  2  4  -10 [-2  3  22  30] 102  -13  20        30
        5  7  2  4  -10  -2 [3  22  30  102] -13  20        102
        5  7  2  4  -10  -2  3 [22  30  102  -13] 20        102
        5  7  2  4  -10  -2  3  22 [30  102  -13  20]       102
```

```
        numbers = [2, 3, 9, 2, 8, 10, 3, 1, 0, 8]
        size = 2
        output = get_winning_numbers(numbers, size)
        # output should be [3, 9, 9, 8, 10, 10, 3, 1, 8]

        Explanation:

                   Window                  Max
       [2  3] 9  2  8  10  3  1  0  8       3
        2 [3  9] 2  8  10  3  1  0  8       9
        2  3 [9  2] 8  10  3  1  0  8       9
        2  3  9 [2  8] 10  3  1  0  8       8
        2  3  9  2 [8  10] 3  1  0  8       10
        2  3  9  2  8 [10  3] 1  0  8       10
        2  3  9  2  8  10 [3  1] 0  8       3
        2  3  9  2  8  10  3 [1  0] 8       1
        2  3  9  2  8  10  3  1  [0  8]     8
```

We aren't done yet! Your friend was very impressed with your work on the algorithm that generates the winning numbers, so he now wants you to develop another algorithm for 30% stake in his lottery ticket investments. This algorithm will find the likelihood that a ticket with winning numbers, n, will be chosen as the winner.

This algorithm will take an input list of n winning numbers and will calculate the probability of the numbers winning by finding the
largest sum of the numbers where no two numbers can be adjacent to each other. So, for example, if you had a list of [1, 2, 1, 3] you could
aggregate the first 1, but then you couldn't aggregate the 2. If you take the 2, you cannot aggregate either 1 that is next to it.

- **get_winning_probability(winning_numbers: List[int]) -> int:**.
  - Takes in a list of winning numbers and returns the probability of the numbers winning by finding the largest sum of non-adjacent numbers.
  - **param winning_numbers**: A list of winning numbers that the algorithm will be applied on.
  - **return**: An integer representing the probability of the numbers winning.
  - **Note**: An empty list can be passed in and 0 should be returned in this case.
  - **Note**: There will be no negative numbers passed in.
  - Time Complexity: _O(N)_ where n is the total number of numbers in the input list.
  - Space Complexity: _O(N)_

`Note:`
- **`You do not necessarily need to use a Deque for this problem. Think of a way to keep track of different values you need to get the result of the largest sum at the end.`**

### Examples

```
        winning_numbers = [1, 3, 5, 2, 7]
        output = get_winning_probability(winning_numbers)
        # output should be 13

        Explanation:
        You add 1, 5, and 7 here. This is the maximum combination that picks numbers that are not adjacent to
        one another.
```

```
        winning_numbers = [1, 2, 3, 1]
        output = get_winning_probability(winning_numbers)
        # output should be 4
        You add 1 and 3 here.
```

```
        winning_numbers = [2, 7, 9, 3, 1]
        output = get_winning_probability(winning_numbers)
        # output should be 12
        You add 2, 9, and 1 here.
```

## **Submission**

#### **Deliverables**

Follow the same instructions as you did in earlier projects.

**USING D2L TO DOWNLOAD PROJECT'S STARTER PACKAGE:**

1. Download the starter package from D2L under Projects content.
2. Work on your project as long as you want then upload your solution.py to Codio.
3. Click **Submit** button on Guide when you are done!
4. Mark your work **Complete**.

**Grading**
The following 100-point rubric will be used to determine your grade on Project5:

- Tests (70)
  - 00 - test_len(): \_\_/1
  - 01 - test_is_empty: \_\_/1
  - 02 - test_front_element: \_\_/2
  - 03 - test_back_element: \_\_/2
  - 04 - test_front_enqueue_basic: \_\_/1
  - 05 - test_back_enqueue_basic: \_\_/1
  - 06 - test_front_enqueue: \_\_/6
  - 07 - test_back_enqueue: \_\_/6
  - 08 - test_front_dequeue_basic: \_\_/1
  - 09 - test_back_dequeue_basic: \_\_/1
  - 10 - test_front_dequeue: \_\_/6
  - 11 - test_back_dequeue: \_\_/6
  - 12 - test_grow: \_\_/4
  - 13 - test_shrink: \_\_/4
  - 14 - test_winning_numbers: \_\_/14
  - 15 - test_winning_probability: \_\_/14
  - 16 - test_grow_additional: \_\_/0
  - 17 - test_shrink_additional: \_\_/0
- Manual (30)

  - M0 - len(): \_\_/1
  - M1 - is_empty: \_\_/1
  - M2 - front_element: \_\_/1
  - M3 - back_element: \_\_/1
  - M4 - front_enqueue: \_\_/2 ( run time and space complexity checked)
  - M5 - back_enqueue: \_\_/2 ( run time and space complexity checked)
  - M6 - front_dequeue: \_\_/2 ( run time and space complexity checked)
  - M7 - back_dequeue: \_\_/2 ( run time and space complexity checked)
  - M8 - grow: \_\_/2 ( run time and space complexity checked)
  - M9 - shrink: \_\_/2 ( run time and space complexity checked)
  - M10 - winning_numbers: \_\_/8 ( run time and space complexity checked)
  - M11 - winning_probability: \_\_/6 ( run time and space complexity checked)

- **Manual (30 points)**
  - Time complexity must be met for each function.
    \*Time and Space complexity of on add, remove and application problem and points are **divided equally** for each function. If you fail to meet time **or** space complexity in a given function, you receive half of the manual points for that function.
  - Loss of 1 point per missing docstring (max 5 point loss)
  - Loss of 2 points per changed function signature (max 20 point loss)
  - Loss of complexity and loss of testcase points for the required functions in this project. You may not use any additional data structures such as dictionaries, and sets!
  - You must actually use the underlying **File** in the provided skeleton for the application problem. The testcases check for this, but attempting to get around the checks will result in a zero.
- **Important reminder**
  Note students can not use Chegg or similar sites, see syllabus for details, use of outside resources for the application problem is strictly forbidden, use of outside resources is limited to max of 2 functions in a project.

  - **DOCSTRING** is not provided for this project. Please use Project 1 as a template for your DOCSTRING .
    To learn more on what is a DOCSTRING visit the following website: [What is Docstring?](https://peps.python.org/pep-0257/)
    - One point per function that misses DOCSTRING.
    - Up to 5 points of deductions.

#### Authors

This project was created by Nate Gu, contributions from Jacob Caurdy, Andrew Haas, Khushi Vora, and Matt Kight
