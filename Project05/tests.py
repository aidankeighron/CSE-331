"""
Project 5
CSE 331 FS24 
tests.py
"""
import unittest
import random
import types
from solution import Node, AVLTree, BinarySearchTree, KNNClassifier


class BSTTests(unittest.TestCase):

    def test_insert_bst(self):
        """
        (1) Test inserting to empty tree
        final structure:
            1
        """
        bst = BinarySearchTree()
        bst.insert(bst.origin, 1)
        self.assertEqual(1, bst.size)
        self.assertEqual(1, bst.origin.value)
        self.assertEqual(0, bst.origin.height)
        self.assertEqual(None, bst.origin.left)
        self.assertEqual(None, bst.origin.right)

        """
        (2) Test inserting to cause imbalance tree on left
        final structure:
               10
              /
             5
            /
           1
          /
        -1
        """
        bst = BinarySearchTree()
        for value in [10, 5, 1, -1]:
            bst.insert(bst.origin, value)
        self.assertEqual(4, bst.size)
        self.assertEqual(10, bst.origin.value)
        self.assertEqual(3, bst.origin.height)
        self.assertEqual(5, bst.origin.left.value)
        self.assertEqual(2, bst.origin.left.height)
        self.assertEqual(1, bst.origin.left.left.value)
        self.assertEqual(1, bst.origin.left.left.height)
        self.assertEqual(-1, bst.origin.left.left.left.value)
        self.assertEqual(0, bst.origin.left.left.left.height)
        self.assertEqual(None, bst.origin.right)
        """
        (3) Test inserting to cause imbalance tree on left
        final structure:
             10
            /  \
           1    12
                 \
                  13
                   \
                   14
                    \
                    15
        """
        bst = BinarySearchTree()
        for value in [10, 12, 13, 14, 15, 1]:
            bst.insert(bst.origin, value)
        self.assertEqual(6, bst.size)
        self.assertEqual(10, bst.origin.value)
        self.assertEqual(4, bst.origin.height)
        self.assertEqual(1, bst.origin.left.value)
        self.assertEqual(0, bst.origin.left.height)

        self.assertEqual(12, bst.origin.right.value)
        self.assertEqual(3, bst.origin.right.height)
        self.assertEqual(13, bst.origin.right.right.value)
        self.assertEqual(2, bst.origin.right.right.height)
        self.assertEqual(14, bst.origin.right.right.right.value)
        self.assertEqual(1, bst.origin.right.right.right.height)
        self.assertEqual(15, bst.origin.right.right.right.right.value)
        self.assertEqual(0, bst.origin.right.right.right.right.height)

        """
        (4) Test inserting to complex tree (no rotating)
        final structure:
                        10
                    /        \
                  7           19
                /             / \
               4            13   35
              /  \           \   /   
             1    6          17 25
        """
        bst = BinarySearchTree()
        for value in [10, 7, 4, 19, 35, 25, 13, 17, 1, 6]:
            bst.insert(bst.origin, value)

        self.assertEqual(10, bst.size)
        # Height 3
        self.assertEqual(10, bst.origin.value)
        self.assertEqual(3, bst.origin.height)

        # Height 2
        self.assertEqual(7, bst.origin.left.value)
        self.assertEqual(2, bst.origin.left.height)
        self.assertEqual(19, bst.origin.right.value)
        self.assertEqual(2, bst.origin.right.height)

        # Height 1
        self.assertEqual(4, bst.origin.left.left.value)
        self.assertEqual(1, bst.origin.left.left.height)
        self.assertEqual(13, bst.origin.right.left.value)
        self.assertEqual(1, bst.origin.right.left.height)
        self.assertEqual(35, bst.origin.right.right.value)
        self.assertEqual(1, bst.origin.right.right.height)

        # Height 0
        self.assertEqual(1, bst.origin.left.left.left.value)
        self.assertEqual(0, bst.origin.left.left.left.height)
        self.assertEqual(6, bst.origin.left.left.right.value)
        self.assertEqual(0, bst.origin.left.left.right.height)
        self.assertEqual(17, bst.origin.right.left.right.value)
        self.assertEqual(0, bst.origin.right.left.right.height)
        self.assertEqual(25, bst.origin.right.right.left.value)
        self.assertEqual(0, bst.origin.right.right.left.height)

    def test_remove_bst(self):
        # visualize this testcase with https://www.cs.usfca.edu/~galles/visualization/AVLtree.html
        # ensure empty tree is properly handled
        bst = BinarySearchTree()
        self.assertIsNone(bst.remove(bst.origin, 0))

        """
        (1) test removal all left side (not trigger rotation)
        initial structure:
            2
           / \
          1   3
         /     \
        0       4
        final structure (removing 1, 0):
            2
             \
              3
               \
                4
        """
        bst = BinarySearchTree()
        for value in [2, 1, 3, 0, 4]:
            bst.insert(bst.origin, value)
        self.assertEqual(5, bst.size)

        bst.remove(bst.origin, 1)  # one child removal
        self.assertEqual(0, bst.origin.left.value)

        bst.remove(bst.origin, 0)  # zero child removal, will need rebalancing
        self.assertEqual(3, bst.size)
        self.assertEqual(2, bst.origin.value)
        self.assertEqual(2, bst.origin.height)
        self.assertEqual(3, bst.origin.right.value)
        self.assertEqual(1, bst.origin.right.height)
        self.assertEqual(4, bst.origin.right.right.value)
        self.assertEqual(0, bst.origin.right.right.height)
        self.assertIsNone(bst.origin.left)

        """
        (2) test removal all right side (not trigger rotation)
        initial structure:
            3
           / \
          2   4
         /     \
        1       5
        final structure (removing 4, 5):
            3
           /
          2   
         /     
        1       
        """
        bst = BinarySearchTree()
        for value in [3, 2, 4, 1, 5]:
            bst.insert(bst.origin, value)

        bst.remove(bst.origin, 4)  # one child removal
        self.assertEqual(5, bst.origin.right.value)

        bst.remove(bst.origin, 5)  # zero child removal, will need rebalancing
        self.assertEqual(3, bst.size)
        self.assertEqual(3, bst.origin.value)
        self.assertEqual(2, bst.origin.height)
        self.assertEqual(2, bst.origin.left.value)
        self.assertEqual(1, bst.origin.left.height)
        self.assertEqual(1, bst.origin.left.left.value)
        self.assertEqual(0, bst.origin.left.left.height)
        self.assertIsNone(bst.origin.right)

        """
        (3) test simple 2-child removal
        initial structure:
          2
         / \
        1   3
        final structure (removing 2):
         1 
          \
           3
        """
        bst = BinarySearchTree()
        for value in [2, 1, 3]:
            bst.insert(bst.origin, value)

        # two child removal (predecessor is in the left subtree)
        bst.remove(bst.origin, 2)
        self.assertEqual(2, bst.size)
        self.assertEqual(1, bst.origin.value)
        self.assertEqual(1, bst.origin.height)
        self.assertEqual(3, bst.origin.right.value)
        self.assertEqual(0, bst.origin.right.height)
        self.assertIsNone(bst.origin.left)

        """
        (4) Removing from a tree with a single node:
           5
        final structure (removing 5):
           Nothing
        """
        bst = BinarySearchTree()
        bst.insert(bst.origin, 5)

        bst.remove(bst.origin, 5)
        self.assertEqual(0, bst.size)
        self.assertIsNone(bst.origin)

        """
        (5) test compounded 2-child removal
        initial structure:
              4
           /     \
          2       6
         / \     / \
        1   3   5   7
        intermediate structure (removing 2, 6):
            4
           / \
          1   5
           \   \
            3   7
        final structure (removing 4)
            3
           / \
          1   5
               \
                7        
        """
        bst = BinarySearchTree()
        for i in [4, 2, 6, 1, 3, 5, 7]:
            bst.insert(bst.origin, i)
        bst.remove(bst.origin, 2)  # two child removal
        self.assertEqual(1, bst.origin.left.value)

        bst.remove(bst.origin, 6)  # two child removal
        self.assertEqual(5, bst.origin.right.value)

        bst.remove(bst.origin, 4)  # two child removal
        self.assertEqual(4, bst.size)
        self.assertEqual(3, bst.origin.value)
        self.assertEqual(2, bst.origin.height)
        self.assertEqual(1, bst.origin.left.value)
        self.assertEqual(0, bst.origin.left.height)
        self.assertEqual(5, bst.origin.right.value)
        self.assertEqual(1, bst.origin.right.height)
        self.assertEqual(7, bst.origin.right.right.value)
        self.assertEqual(0, bst.origin.right.right.height)

        """
        (6) test removal of intermediate node with 1 children
        Initial structure:
                4
               / \
              3   6
             /   / \
            2   5   7
           / 
          0   
        Final structure (removing 3):
                4
               / \
              2   6
             /   / \
            0   5   7          
        """
        bst = BinarySearchTree()
        for i in [4, 6, 3, 2, 0, 5, 7]:
            bst.insert(bst.origin, i)
        bst.remove(bst.origin, 3)

        self.assertEqual(6, bst.size)
        self.assertEqual(4, bst.origin.value)
        self.assertEqual(2, bst.origin.height)

        self.assertEqual(2, bst.origin.left.value)
        self.assertEqual(1, bst.origin.left.height)
        self.assertEqual(4, bst.origin.left.parent.value)

        self.assertEqual(0, bst.origin.left.left.value)
        self.assertEqual(0, bst.origin.left.left.height)
        self.assertEqual(2, bst.origin.left.left.parent.value)

        self.assertEqual(6, bst.origin.right.value)
        self.assertEqual(1, bst.origin.right.height)
        self.assertEqual(4, bst.origin.right.parent.value)

        self.assertEqual(5, bst.origin.right.left.value)
        self.assertEqual(0, bst.origin.right.left.height)
        self.assertEqual(6, bst.origin.right.left.parent.value)

        self.assertEqual(7, bst.origin.right.right.value)
        self.assertEqual(0, bst.origin.right.right.height)
        self.assertEqual(6, bst.origin.right.right.parent.value)

        """
        (7) test removal of intermediate node with 2 children
        Initial structure:
                 7  
               /   \
              4     9
             / \   / \
            2  5   8  10
           / \  \        
          1   3  6
        Final structure (removing 4):
                  7  
               /    \
              3      9
             / \    / \
            2   5   8  10
           /     \
          1       6
        """
        bst = BinarySearchTree()
        for i in [7, 4, 9, 2, 5, 8, 10, 1, 3, 6]:
            bst.insert(bst.origin, i)
        a = str(bst)
        bst.remove(bst.origin, 4)

        self.assertEqual(9, bst.size)
        self.assertEqual(7, bst.origin.value)
        self.assertEqual(3, bst.origin.height)

        self.assertEqual(3, bst.origin.left.value)
        self.assertEqual(2, bst.origin.left.height)
        self.assertEqual(7, bst.origin.left.parent.value)

        self.assertEqual(2, bst.origin.left.left.value)
        self.assertEqual(1, bst.origin.left.left.height)
        self.assertEqual(3, bst.origin.left.left.parent.value)

        self.assertEqual(1, bst.origin.left.left.left.value)
        self.assertEqual(0, bst.origin.left.left.left.height)
        self.assertEqual(2, bst.origin.left.left.left.parent.value)

        self.assertEqual(5, bst.origin.left.right.value)
        self.assertEqual(1, bst.origin.left.right.height)
        self.assertEqual(3, bst.origin.left.right.parent.value)

        self.assertEqual(6, bst.origin.left.right.right.value)
        self.assertEqual(0, bst.origin.left.right.right.height)
        self.assertEqual(5, bst.origin.left.right.right.parent.value)

        self.assertEqual(9, bst.origin.right.value)
        self.assertEqual(1, bst.origin.right.height)
        self.assertEqual(7, bst.origin.right.parent.value)

        self.assertEqual(8, bst.origin.right.left.value)
        self.assertEqual(0, bst.origin.right.left.height)
        self.assertEqual(9, bst.origin.right.left.parent.value)

        self.assertEqual(10, bst.origin.right.right.value)
        self.assertEqual(0, bst.origin.right.right.height)
        self.assertEqual(9, bst.origin.right.right.parent.value)

    def test_search(self):

        # ensure empty tree is properly handled
        bst = BinarySearchTree()
        self.assertIsNone(bst.search(bst.origin, 0))

        """
        (1) search small basic tree
        tree structure
          1
         / \
        0   3
           / \
          2   4
        """
        bst = BinarySearchTree()
        numbers = [1, 0, 3, 2, 4]
        for num in numbers:
            bst.insert(bst.origin, num)
        # search existing numbers
        for num in numbers:
            node = bst.search(bst.origin, num)
            self.assertIsInstance(node, Node)
            self.assertEqual(num, node.value)
        # search non-existing numbers and ensure parent of where value would go is returned
        pairs = [(-1, 0), (0.5, 0), (5, 4), (2.5, 2),
                 (3.5, 4), (-1e5, 0), (1e5, 4)]
        for target, closest in pairs:
            node = bst.search(bst.origin, target)
            self.assertIsInstance(node, Node)
            self.assertEqual(closest, node.value)

        """(2) search large random tree"""
        random.seed(331)
        bst = BinarySearchTree()
        numbers = {random.randint(-1000, 1000) for _ in range(1000)}
        for num in numbers:
            bst.insert(bst.origin, num)
        for num in numbers:
            # search existing number
            node = bst.search(bst.origin, num)
            self.assertIsInstance(node, Node)
            self.assertEqual(num, node.value)

            # if this node is a leaf, search non-existing numbers around it
            # to ensure it is returned as the parent of where new insertions would go
            if node.left is None and node.right is None:
                node = bst.search(bst.origin, num + 0.1)
                self.assertIsInstance(node, Node)
                self.assertEqual(num, node.value)
                node = bst.search(bst.origin, num - 0.1)
                self.assertIsInstance(node, Node)
                self.assertEqual(num, node.value)


class AVLTreeTests(unittest.TestCase):

    def test_rotate(self):

        # ensure empty tree is properly handled
        avl = AVLTree()
        self.assertIsNone(avl.right_rotate(avl.origin))
        self.assertIsNone(avl.left_rotate(avl.origin))

        """
        (1) test basic right
        initial structure:
            3
           /
          2
         /
        1
        final structure:
          2
         / \
        1   3
        """
        avl.origin = Node(3)
        avl.origin.left = Node(2, parent=avl.origin)
        avl.origin.left.left = Node(1, parent=avl.origin.left)
        avl.size = 3
        node = avl.right_rotate(avl.origin)
        self.assertIsInstance(node, Node)
        self.assertEqual(2, node.value)

        # root has no parent
        self.assertEqual(2, avl.origin.value)
        self.assertIsNone(avl.origin.parent)

        # root left value and parent
        self.assertEqual(1, avl.origin.left.value)
        self.assertEqual(avl.origin, avl.origin.left.parent)

        # left leaf should have no children
        self.assertIsNone(avl.origin.left.left)
        self.assertIsNone(avl.origin.left.right)

        # root right value and parent
        self.assertEqual(3, avl.origin.right.value)
        self.assertEqual(avl.origin, avl.origin.right.parent)

        # right leaf should have no children
        self.assertIsNone(avl.origin.right.right)
        self.assertIsNone(avl.origin.right.left)

        """
        (2) test basic left
        initial structure:
        1
         \
          2
           \
            3
        final structure:
          2
         / \
        1   3
        """
        avl = AVLTree()
        avl.origin = Node(1)
        avl.origin.right = Node(2, parent=avl.origin)
        avl.origin.right.right = Node(3, parent=avl.origin.right)
        avl.size = 3

        node = avl.left_rotate(avl.origin)
        self.assertIsInstance(node, Node)
        self.assertEqual(2, node.value)

        # root has no parent
        self.assertEqual(2, avl.origin.value)
        self.assertIsNone(avl.origin.parent)

        # root left value and parent
        self.assertEqual(1, avl.origin.left.value)
        self.assertEqual(avl.origin, avl.origin.left.parent)

        # left leaf should have no children
        self.assertIsNone(avl.origin.left.left)
        self.assertIsNone(avl.origin.left.right)

        # root right value and parent
        self.assertEqual(3, avl.origin.right.value)
        self.assertEqual(avl.origin, avl.origin.right.parent)

        # right leaf should have no children
        self.assertIsNone(avl.origin.right.right)
        self.assertIsNone(avl.origin.right.left)

        """
        (3) test intermediate right, rotating at origin
        initial structure:
              7
             / \
            3   10
           / \
          2   4
         /
        1 
        final structure:
            3
           / \
          2   7
         /   / \
        1   4   10
        """
        avl = AVLTree()
        avl.origin = Node(7)
        avl.origin.left = Node(3, parent=avl.origin)
        avl.origin.left.left = Node(2, parent=avl.origin.left)
        avl.origin.left.left.left = Node(1, parent=avl.origin.left.left)
        avl.origin.left.right = Node(4, parent=avl.origin.left)
        avl.origin.right = Node(10, parent=avl.origin)

        node = avl.right_rotate(avl.origin)
        self.assertIsInstance(node, Node)
        self.assertEqual(3, node.value)

        self.assertEqual(3, avl.origin.value)
        self.assertIsNone(avl.origin.parent)

        self.assertEqual(2, avl.origin.left.value)
        self.assertEqual(avl.origin, avl.origin.left.parent)
        self.assertIsNone(avl.origin.left.right)

        self.assertEqual(1, avl.origin.left.left.value)
        self.assertEqual(avl.origin.left, avl.origin.left.left.parent)
        self.assertIsNone(avl.origin.left.left.left)
        self.assertIsNone(avl.origin.left.left.right)

        self.assertEqual(7, avl.origin.right.value)
        self.assertEqual(avl.origin, avl.origin.right.parent)

        self.assertEqual(4, avl.origin.right.left.value)
        self.assertEqual(avl.origin.right, avl.origin.right.left.parent)
        self.assertIsNone(avl.origin.right.left.left)
        self.assertIsNone(avl.origin.right.left.right)

        self.assertEqual(10, avl.origin.right.right.value)
        self.assertEqual(avl.origin.right, avl.origin.right.right.parent)
        self.assertIsNone(avl.origin.right.right.left)
        self.assertIsNone(avl.origin.right.right.right)

        """
        (4) test intermediate left, rotating at origin
        initial structure:
          7
         /  \
        3   10
           /   \
          9    11
                 \
                  12
        final structure:
        	10
           /  \
          7   11
         / \    \
        3   9    12
        """
        avl = AVLTree()
        avl.origin = Node(7)
        avl.origin.left = Node(3, parent=avl.origin)
        avl.origin.right = Node(10, parent=avl.origin)
        avl.origin.right.left = Node(9, parent=avl.origin.right)
        avl.origin.right.right = Node(11, parent=avl.origin.right)
        avl.origin.right.right.right = Node(12, parent=avl.origin.right.right)

        node = avl.left_rotate(avl.origin)
        self.assertIsInstance(node, Node)
        self.assertEqual(10, node.value)

        self.assertEqual(10, avl.origin.value)
        self.assertIsNone(avl.origin.parent)
        # assert node10.value == 10 and not node10.parent

        self.assertEqual(7, avl.origin.left.value)
        self.assertEqual(avl.origin, avl.origin.left.parent)
        # assert node7.value == 7 and node7.parent == node10

        self.assertEqual(3, avl.origin.left.left.value)
        self.assertEqual(avl.origin.left, avl.origin.left.left.parent)
        self.assertIsNone(avl.origin.left.left.left)
        self.assertIsNone(avl.origin.left.left.right)
        # assert node3.value == 3 and node3.parent == node7 and not (
        #     node3.left or node3.right)

        self.assertEqual(9, avl.origin.left.right.value)
        self.assertEqual(avl.origin.left, avl.origin.left.right.parent)
        self.assertIsNone(avl.origin.left.right.left)
        self.assertIsNone(avl.origin.left.right.right)
        # assert node9.value == 9 and node9.parent == node7 and not (
        #     node9.left or node9.right)

        self.assertEqual(11, avl.origin.right.value)
        self.assertEqual(avl.origin, avl.origin.right.parent)
        self.assertIsNone(avl.origin.right.left)
        # assert node11.value == 11 and node11.parent == node10 and not node11.left

        self.assertEqual(12, avl.origin.right.right.value)
        self.assertEqual(avl.origin.right, avl.origin.right.right.parent)
        self.assertIsNone(avl.origin.right.right.left)
        self.assertIsNone(avl.origin.right.right.right)
        # assert node12.value == 12 and node12.parent == node11 and not (
        #     node12.left or node12.right)

        """
        (5) test advanced right, rotating not at origin
        initial structure:
        		10
        	   /  \
        	  5	   11
        	 / \     \
        	3	7    12
           / \
          2   4
         /
        1
        final structure:
              10
             /  \
            3    11
           / \     \
          2   5     12
         /   / \
        1   4   7
        """
        avl = AVLTree()
        avl.origin = Node(10)
        avl.origin.right = Node(11, parent=avl.origin)
        avl.origin.right.right = Node(12, parent=avl.origin.right)
        avl.origin.left = Node(5, parent=avl.origin)
        avl.origin.left.right = Node(7, parent=avl.origin.left)
        avl.origin.left.left = Node(3, parent=avl.origin.left)
        avl.origin.left.left.right = Node(4, parent=avl.origin.left.left)
        avl.origin.left.left.left = Node(2, parent=avl.origin.left.left)
        avl.origin.left.left.left.left = Node(
            1, parent=avl.origin.left.left.left)

        node = avl.right_rotate(avl.origin.left)
        self.assertIsInstance(node, Node)
        self.assertEqual(3, node.value)

        self.assertEqual(10, avl.origin.value)
        self.assertIsNone(avl.origin.parent)

        self.assertEqual(3, avl.origin.left.value)
        self.assertEqual(avl.origin, avl.origin.left.parent)

        self.assertEqual(2, avl.origin.left.left.value)
        self.assertEqual(avl.origin.left, avl.origin.left.left.parent)
        self.assertIsNone(avl.origin.left.left.right)

        self.assertEqual(5, avl.origin.left.right.value)
        self.assertEqual(avl.origin.left, avl.origin.left.right.parent)

        self.assertEqual(1, avl.origin.left.left.left.value)
        self.assertEqual(avl.origin.left.left,
                         avl.origin.left.left.left.parent)
        self.assertIsNone(avl.origin.left.left.left.left)
        self.assertIsNone(avl.origin.left.left.left.right)

        self.assertEqual(4, avl.origin.left.right.left.value)
        self.assertEqual(avl.origin.left.right,
                         avl.origin.left.right.left.parent)
        self.assertIsNone(avl.origin.left.right.left.left)
        self.assertIsNone(avl.origin.left.right.left.right)

        self.assertEqual(7, avl.origin.left.right.right.value)
        self.assertEqual(avl.origin.left.right,
                         avl.origin.left.right.right.parent)
        self.assertIsNone(avl.origin.left.right.right.left)
        self.assertIsNone(avl.origin.left.right.right.right)

        self.assertEqual(11, avl.origin.right.value)
        self.assertEqual(avl.origin, avl.origin.right.parent)
        self.assertIsNone(avl.origin.right.left)

        self.assertEqual(12, avl.origin.right.right.value)
        self.assertEqual(avl.origin.right, avl.origin.right.right.parent)
        self.assertIsNone(avl.origin.right.right.left)
        self.assertIsNone(avl.origin.right.right.right)

        """
        (6) test advanced left, rotating not at origin
        initial structure:
        	3
           / \
          2   10
         /   /  \
        1   5   12
               /  \
              11   13
                     \
                      14
        final structure:
        	3
           / \
          2   12
         /   /  \
        1   10   13
           /  \    \
          5   11   14
        """
        avl = AVLTree()
        avl.origin = Node(3)
        avl.origin.left = Node(2, parent=avl.origin)
        avl.origin.left.left = Node(1, parent=avl.origin.left)
        avl.origin.right = Node(10, parent=avl.origin)
        avl.origin.right.left = Node(5, parent=avl.origin.right)
        avl.origin.right.right = Node(12, parent=avl.origin.right)
        avl.origin.right.right.left = Node(11, parent=avl.origin.right.right)
        avl.origin.right.right.right = Node(13, parent=avl.origin.right.right)
        avl.origin.right.right.right.right = Node(
            14, parent=avl.origin.right.right.right)

        node = avl.left_rotate(avl.origin.right)
        self.assertIsInstance(node, Node)
        self.assertEqual(12, node.value)

        self.assertEqual(3, avl.origin.value)
        self.assertIsNone(avl.origin.parent)

        self.assertEqual(2, avl.origin.left.value)
        self.assertEqual(avl.origin, avl.origin.left.parent)
        self.assertIsNone(avl.origin.left.right)

        self.assertEqual(1, avl.origin.left.left.value)
        self.assertEqual(avl.origin.left, avl.origin.left.left.parent)
        self.assertIsNone(avl.origin.left.left.left)
        self.assertIsNone(avl.origin.left.left.right)

        self.assertEqual(12, avl.origin.right.value)
        self.assertEqual(avl.origin, avl.origin.right.parent)

        self.assertEqual(10, avl.origin.right.left.value)
        self.assertEqual(avl.origin.right, avl.origin.right.left.parent)

        self.assertEqual(5, avl.origin.right.left.left.value)
        self.assertEqual(avl.origin.right.left,
                         avl.origin.right.left.left.parent)
        self.assertIsNone(avl.origin.right.left.left.left)
        self.assertIsNone(avl.origin.right.left.left.right)

        self.assertEqual(11, avl.origin.right.left.right.value)
        self.assertEqual(avl.origin.right.left,
                         avl.origin.right.left.right.parent)
        self.assertIsNone(avl.origin.right.left.right.left)
        self.assertIsNone(avl.origin.right.left.right.right)

        self.assertEqual(13, avl.origin.right.right.value)
        self.assertEqual(avl.origin.right, avl.origin.right.right.parent)
        self.assertIsNone(avl.origin.right.right.left)

        self.assertEqual(14, avl.origin.right.right.right.value)
        self.assertEqual(avl.origin.right.right,
                         avl.origin.right.right.right.parent)
        self.assertIsNone(avl.origin.right.right.right.left)
        self.assertIsNone(avl.origin.right.right.right.right)

    def test_balance_factor(self):

        # ensure empty tree is properly handled
        avl = AVLTree()
        self.assertEqual(0, avl.balance_factor(avl.origin))

        """
        (1) test on balanced tree
        structure:
          2
         / \
        1   3
        """
        avl.origin = Node(2)
        avl.origin.height = 1
        avl.origin.left = Node(1, parent=avl.origin)
        avl.origin.left.height = 0
        avl.origin.right = Node(3, parent=avl.origin)
        avl.origin.right.height = 0
        avl.size = 3

        self.assertEqual(0, avl.balance_factor(avl.origin))
        self.assertEqual(0, avl.balance_factor(avl.origin.left))
        self.assertEqual(0, avl.balance_factor(avl.origin.right))

        """
        (2) test on unbalanced left
        structure:
            3
           /
          2
         /
        1
        """
        avl = AVLTree()
        avl.origin = Node(3)
        avl.origin.height = 2
        avl.origin.left = Node(2, parent=avl.origin)
        avl.origin.left.height = 1
        avl.origin.left.left = Node(1, parent=avl.origin.left)
        avl.origin.left.left.height = 0
        avl.size = 3

        self.assertEqual(2, avl.balance_factor(avl.origin))
        self.assertEqual(1, avl.balance_factor(avl.origin.left))
        self.assertEqual(0, avl.balance_factor(avl.origin.left.left))

        """
        (2) test on unbalanced right
        structure:
        1
         \
          2
           \
            3
        """
        avl = AVLTree()
        avl.origin = Node(1)
        avl.origin.height = 2
        avl.origin.right = Node(2, parent=avl.origin)
        avl.origin.right.height = 1
        avl.origin.right.right = Node(3, parent=avl.origin.right)
        avl.origin.right.right.height = 0
        avl.size = 3

        self.assertEqual(-2, avl.balance_factor(avl.origin))
        self.assertEqual(-1, avl.balance_factor(avl.origin.right))
        self.assertEqual(0, avl.balance_factor(avl.origin.right.right))

    def test_rebalance(self):

        # ensure empty tree is properly handled
        avl = AVLTree()
        self.assertIsNone(avl.rebalance(avl.origin))

        """
        (1) test balanced tree (do nothing)
        initial and final structure:
          2
         / \
        1   3
        since pointers are already tested in rotation testcase, only check values and heights
        """
        avl.origin = Node(2)
        avl.origin.height = 1
        avl.origin.left = Node(1, parent=avl.origin)
        avl.origin.left.height = 0
        avl.origin.right = Node(3, parent=avl.origin)
        avl.origin.right.height = 0
        avl.size = 3

        node = avl.rebalance(avl.origin)
        self.assertIsInstance(node, Node)
        self.assertEqual(2, node.value)

        self.assertEqual(2, avl.origin.value)
        self.assertEqual(1, avl.origin.height)
        self.assertEqual(1, avl.origin.left.value)
        self.assertEqual(0, avl.origin.left.height)
        self.assertEqual(3, avl.origin.right.value)
        self.assertEqual(0, avl.origin.right.height)

        """
        (2) test left-left rebalance
        initial structure:
            4
           /
          2
         / \
        1   3
        final structure:
          2
         / \
        1   4
           /
          3
        """
        avl = AVLTree()
        avl.origin = Node(4)
        avl.origin.height = 2
        avl.origin.left = Node(2, parent=avl.origin)
        avl.origin.left.height = 1
        avl.origin.left.left = Node(1, parent=avl.origin.left)
        avl.origin.left.left.height = 0
        avl.origin.left.right = Node(3, parent=avl.origin.left)
        avl.origin.left.right.height = 0
        avl.size = 4

        node = avl.rebalance(avl.origin)
        self.assertIsInstance(node, Node)
        self.assertEqual(2, node.value)

        self.assertEqual(2, avl.origin.value)
        self.assertEqual(2, avl.origin.height)
        self.assertEqual(1, avl.origin.left.value)
        self.assertEqual(0, avl.origin.left.height)
        self.assertEqual(4, avl.origin.right.value)
        self.assertEqual(1, avl.origin.right.height)
        self.assertEqual(3, avl.origin.right.left.value)
        self.assertEqual(0, avl.origin.right.left.height)

        """
        (2) test right-right rebalance
        initial structure:
        1
         \
          3
         /  \
        2    4
        final structure:
          3
         / \
        1   4
         \
          2
        """
        avl = AVLTree()
        avl.origin = Node(1)
        avl.origin.height = 2
        avl.origin.right = Node(3, parent=avl.origin)
        avl.origin.right.height = 1
        avl.origin.right.right = Node(4, parent=avl.origin.right)
        avl.origin.right.right.height = 0
        avl.origin.right.left = Node(2, parent=avl.origin.right)
        avl.origin.right.left.height = 0
        avl.size = 4

        node = avl.rebalance(avl.origin)
        self.assertIsInstance(node, Node)
        self.assertEqual(3, node.value)

        self.assertEqual(3, avl.origin.value)
        self.assertEqual(2, avl.origin.height)
        self.assertEqual(1, avl.origin.left.value)
        self.assertEqual(1, avl.origin.left.height)
        self.assertEqual(4, avl.origin.right.value)
        self.assertEqual(0, avl.origin.right.height)
        self.assertEqual(2, avl.origin.left.right.value)
        self.assertEqual(0, avl.origin.left.right.height)

        """
        (4) test left-right rebalance
        initial structure:
            5
           / \
          2   6
         / \
        1   3
             \
              4
        intermediate structure:
              5
             / \
            3   6
           / \
          2   4
         /
        1
        final structure:
            3 
           / \
          2   5
         /   / \
        1   4   6
        """
        avl = AVLTree()
        avl.origin = Node(5)
        avl.origin.height = 3
        avl.origin.left = Node(2, parent=avl.origin)
        avl.origin.left.height = 2
        avl.origin.right = Node(6, parent=avl.origin)
        avl.origin.right.height = 0
        avl.origin.left.left = Node(1, parent=avl.origin.left)
        avl.origin.left.left.height = 0
        avl.origin.left.right = Node(3, parent=avl.origin.left)
        avl.origin.left.right.height = 1
        avl.origin.left.right.right = Node(4, parent=avl.origin.left.right)
        avl.origin.left.right.right.height = 0

        node = avl.rebalance(avl.origin)
        self.assertIsInstance(node, Node)
        self.assertEqual(3, node.value)

        self.assertEqual(3, avl.origin.value)
        self.assertEqual(2, avl.origin.height)
        self.assertEqual(2, avl.origin.left.value)
        self.assertEqual(1, avl.origin.left.height)
        self.assertEqual(5, avl.origin.right.value)
        self.assertEqual(1, avl.origin.right.height)
        self.assertEqual(1, avl.origin.left.left.value)
        self.assertEqual(0, avl.origin.left.left.height)
        self.assertEqual(4, avl.origin.right.left.value)
        self.assertEqual(0, avl.origin.right.left.height)
        self.assertEqual(6, avl.origin.right.right.value)
        self.assertEqual(0, avl.origin.right.right.height)

        """
        (5) test right-left rebalance
        initial structure:
          2
         / \
        1   5
           / \
          4   6
         /
        3
        intermediate structure:
          2
         / \
        1   4
           / \
          3   5
               \
                6
        final structure:
            4 
           / \
          2   5
         / \   \
        1   3   6
        """
        avl = AVLTree()
        avl.origin = Node(2)
        avl.origin.height = 3
        avl.origin.left = Node(1, parent=avl.origin)
        avl.origin.left.height = 0
        avl.origin.right = Node(5, parent=avl.origin)
        avl.origin.right.height = 2
        avl.origin.right.left = Node(4, parent=avl.origin.right)
        avl.origin.right.left.height = 1
        avl.origin.right.right = Node(6, parent=avl.origin.right)
        avl.origin.right.right.height = 0
        avl.origin.right.left.left = Node(3, parent=avl.origin.right.left)
        avl.origin.right.left.left.height = 0

        node = avl.rebalance(avl.origin)
        self.assertIsInstance(node, Node)
        self.assertEqual(4, node.value)

        self.assertEqual(4, avl.origin.value)
        self.assertEqual(2, avl.origin.height)
        self.assertEqual(2, avl.origin.left.value)
        self.assertEqual(1, avl.origin.left.height)
        self.assertEqual(5, avl.origin.right.value)
        self.assertEqual(1, avl.origin.right.height)
        self.assertEqual(1, avl.origin.left.left.value)
        self.assertEqual(0, avl.origin.left.left.height)
        self.assertEqual(3, avl.origin.left.right.value)
        self.assertEqual(0, avl.origin.left.right.height)
        self.assertEqual(6, avl.origin.right.right.value)
        self.assertEqual(0, avl.origin.right.right.height)

    def test_insert(self):

        # visualize this testcase with https://www.cs.usfca.edu/~galles/visualization/AVLtree.html
        avl = AVLTree()
        """
        (1) test insertion causing right-right rotation
        final structure
          1
         / \
        0   3
           / \
          2   4
        """
        for value in range(5):
            node = avl.insert(avl.origin, value)
            self.assertIsInstance(node, Node)

        self.assertEqual(5, avl.size)
        self.assertEqual(1, avl.origin.value)
        self.assertEqual(2, avl.origin.height)
        self.assertEqual(0, avl.origin.left.value)
        self.assertEqual(0, avl.origin.left.height)
        self.assertEqual(3, avl.origin.right.value)
        self.assertEqual(1, avl.origin.right.height)
        self.assertEqual(2, avl.origin.right.left.value)
        self.assertEqual(0, avl.origin.right.left.height)
        self.assertEqual(4, avl.origin.right.right.value)
        self.assertEqual(0, avl.origin.right.right.height)

        """
        (2) test insertion with a value already existing in the tree.
        """
        for value in range(4, -1, -1):
            node = avl.insert(avl.origin, value)
            self.assertIsInstance(node, Node)
        self.assertEqual(5, avl.size)
        self.assertEqual(1, avl.origin.value)
        self.assertEqual(2, avl.origin.height)
        self.assertEqual(0, avl.origin.left.value)
        self.assertEqual(0, avl.origin.left.height)
        self.assertEqual(3, avl.origin.right.value)
        self.assertEqual(1, avl.origin.right.height)
        self.assertEqual(2, avl.origin.right.left.value)
        self.assertEqual(0, avl.origin.right.left.height)
        self.assertEqual(4, avl.origin.right.right.value)
        self.assertEqual(0, avl.origin.right.right.height)
        self.assertIsNone(avl.origin.left.left)
        self.assertIsNone(avl.origin.left.right)
        self.assertIsNone(avl.origin.right.left.left)
        self.assertIsNone(avl.origin.right.left.right)
        self.assertIsNone(avl.origin.right.right.left)
        self.assertIsNone(avl.origin.right.right.right)

        """
        (3) test insertion causing left-left rotation
        final structure
            3
           / \
          1   4
         / \
        0   2
        """
        avl = AVLTree()
        for value in range(4, -1, -1):
            node = avl.insert(avl.origin, value)
            self.assertIsInstance(node, Node)
        self.assertEqual(5, avl.size)
        self.assertEqual(3, avl.origin.value)
        self.assertEqual(2, avl.origin.height)
        self.assertEqual(1, avl.origin.left.value)
        self.assertEqual(1, avl.origin.left.height)
        self.assertEqual(4, avl.origin.right.value)
        self.assertEqual(0, avl.origin.right.height)
        self.assertEqual(0, avl.origin.left.left.value)
        self.assertEqual(0, avl.origin.left.left.height)
        self.assertEqual(2, avl.origin.left.right.value)
        self.assertEqual(0, avl.origin.left.right.height)

        """
        (4) test insertion (with duplicates) causing left-right rotation
        initial structure:
            5
           / \
          2   6
         / \
        1   3
             \
              4
        final structure:
            3 
           / \
          2   5
         /   / \
        1   4   6
        """
        avl = AVLTree()
        for value in [5, 2, 6, 1, 3] * 2 + [4]:
            node = avl.insert(avl.origin, value)
            self.assertIsInstance(node, Node)
        self.assertEqual(3, avl.origin.value)
        self.assertEqual(2, avl.origin.height)
        self.assertEqual(2, avl.origin.left.value)
        self.assertEqual(1, avl.origin.left.height)
        self.assertEqual(5, avl.origin.right.value)
        self.assertEqual(1, avl.origin.right.height)
        self.assertEqual(1, avl.origin.left.left.value)
        self.assertEqual(0, avl.origin.left.left.height)
        self.assertEqual(4, avl.origin.right.left.value)
        self.assertEqual(0, avl.origin.right.left.height)
        self.assertEqual(6, avl.origin.right.right.value)
        self.assertEqual(0, avl.origin.right.right.height)

        """
        (5) test insertion (with duplicates) causing right-left rotation
        initial structure:
          2
         / \
        1   5
           / \
          4   6
         /
        3
        final structure:
            4 
           / \
          2   5
         / \   \
        1   3   6
        """
        avl = AVLTree()
        for value in [2, 1, 5, 4, 6] * 2 + [3]:
            node = avl.insert(avl.origin, value)
            self.assertIsInstance(node, Node)
        self.assertEqual(4, avl.origin.value)
        self.assertEqual(2, avl.origin.height)
        self.assertEqual(2, avl.origin.left.value)
        self.assertEqual(1, avl.origin.left.height)
        self.assertEqual(5, avl.origin.right.value)
        self.assertEqual(1, avl.origin.right.height)
        self.assertEqual(1, avl.origin.left.left.value)
        self.assertEqual(0, avl.origin.left.left.height)
        self.assertEqual(3, avl.origin.left.right.value)
        self.assertEqual(0, avl.origin.left.right.height)
        self.assertEqual(6, avl.origin.right.right.value)
        self.assertEqual(0, avl.origin.right.right.height)

    def test_remove(self):

        # visualize this testcase with https://www.cs.usfca.edu/~galles/visualization/AVLtree.html
        # ensure empty tree is properly handled
        avl = AVLTree()
        self.assertIsNone(avl.remove(avl.origin, 0))

        """
        (1) test removal causing right-right rotation
        initial structure:
            2
           / \
          1   3
         /     \
        0       4
        final structure (removing 1, 0):
          3 
         / \
        2   4
        """
        avl = AVLTree()
        for value in [2, 1, 3, 0, 4]:
            avl.insert(avl.origin, value)

        avl.remove(avl.origin, 1)  # one child removal
        self.assertEqual(0, avl.origin.left.value)

        avl.remove(avl.origin, 0)  # zero child removal, will need rebalancing
        self.assertEqual(3, avl.size)
        self.assertEqual(3, avl.origin.value)
        self.assertEqual(1, avl.origin.height)
        self.assertEqual(2, avl.origin.left.value)
        self.assertEqual(0, avl.origin.left.height)
        self.assertEqual(4, avl.origin.right.value)
        self.assertEqual(0, avl.origin.right.height)

        """
        (2) test removal causing left-left rotation
        initial structure:
            3
           / \
          2   4
         /     \
        1       5
        final structure (removing 4, 5):
          2 
         / \
        1   3
        """
        avl = AVLTree()
        for value in [3, 2, 4, 1, 5]:
            avl.insert(avl.origin, value)

        avl.remove(avl.origin, 4)  # one child removal
        self.assertEqual(5, avl.origin.right.value)

        avl.remove(avl.origin, 5)  # zero child removal, will need rebalancing
        self.assertEqual(3, avl.size)
        self.assertEqual(2, avl.origin.value)
        self.assertEqual(1, avl.origin.height)
        self.assertEqual(1, avl.origin.left.value)
        self.assertEqual(0, avl.origin.left.height)
        self.assertEqual(3, avl.origin.right.value)
        self.assertEqual(0, avl.origin.right.height)

        """
        (3) test removal causing left-right rotation
        initial structure:
              5
             / \
            2   6
           / \   \
          1   3   7
         /     \
        0       4
        final structure (removing 1, 6):
            3 
           / \
          2   5
         /   / \
        0   4   7
        """
        avl = AVLTree()
        for value in [5, 2, 6, 1, 3, 7, 0, 4]:
            avl.insert(avl.origin, value)

        avl.remove(avl.origin, 1)  # one child removal
        self.assertEqual(0, avl.origin.left.left.value)

        avl.remove(avl.origin, 6)  # one child removal, will need rebalancing

        self.assertEqual(6, avl.size)
        self.assertEqual(3, avl.origin.value)
        self.assertEqual(2, avl.origin.height)
        self.assertEqual(2, avl.origin.left.value)
        self.assertEqual(1, avl.origin.left.height)
        self.assertEqual(5, avl.origin.right.value)
        self.assertEqual(1, avl.origin.right.height)
        self.assertEqual(0, avl.origin.left.left.value)
        self.assertEqual(0, avl.origin.left.left.height)
        self.assertEqual(4, avl.origin.right.left.value)
        self.assertEqual(0, avl.origin.right.left.height)
        self.assertEqual(7, avl.origin.right.right.value)
        self.assertEqual(0, avl.origin.right.right.height)

        """
        (4) test removal causing right-left rotation
        initial structure:
            2
           / \
          1   5
         /   / \
        0   4   6
           /     \
          3       7
        final structure (removing 6, 1):
            4 
           / \
          2   5
         / \   \
        0   3   7
        """
        avl = AVLTree()
        for value in [2, 1, 5, 0, 4, 6, 3, 7]:
            avl.insert(avl.origin, value)

        avl.remove(avl.origin, 6)  # one child removal
        self.assertEqual(7, avl.origin.right.right.value)

        avl.remove(avl.origin, 1)  # one child removal, will need rebalancing
        self.assertEqual(6, avl.size)
        self.assertEqual(4, avl.origin.value)
        self.assertEqual(2, avl.origin.height)
        self.assertEqual(2, avl.origin.left.value)
        self.assertEqual(1, avl.origin.left.height)
        self.assertEqual(5, avl.origin.right.value)
        self.assertEqual(1, avl.origin.right.height)
        self.assertEqual(7, avl.origin.right.right.value)
        self.assertEqual(0, avl.origin.right.right.height)
        self.assertEqual(0, avl.origin.left.left.value)
        self.assertEqual(0, avl.origin.left.left.height)
        self.assertEqual(3, avl.origin.left.right.value)
        self.assertEqual(0, avl.origin.left.right.height)

        """
        (5) test simple 2-child removal
        initial structure:
          2
         / \
        1   3
        final structure (removing 2):
         1 
          \
           3
        """
        avl = AVLTree()
        for value in [2, 1, 3]:
            avl.insert(avl.origin, value)
        avl.remove(avl.origin, 2)  # two child removal
        self.assertEqual(2, avl.size)
        self.assertEqual(1, avl.origin.value)
        self.assertEqual(1, avl.origin.height)
        self.assertEqual(3, avl.origin.right.value)
        self.assertEqual(0, avl.origin.right.height)

        """
        (5) test compounded 2-child removal
        initial structure:
              4
           /     \
          2       6
         / \     / \
        1   3   5   7
        intermediate structure (removing 2, 6):
            4
           / \
          1   5
           \   \
            3   7
        final structure (removing 4)
            3
           / \
          1   5
               \
                7        
        """
        avl = AVLTree()
        for value in [4, 2, 6, 1, 3, 5, 7]:
            avl.insert(avl.origin, value)

        avl.remove(avl.origin, 2)  # two child removal
        self.assertEqual(1, avl.origin.left.value)

        avl.remove(avl.origin, 6)  # two child removal
        self.assertEqual(5, avl.origin.right.value)

        avl.remove(avl.origin, 4)  # two child removal
        self.assertEqual(4, avl.size)
        self.assertEqual(3, avl.origin.value)
        self.assertEqual(2, avl.origin.height)
        self.assertEqual(1, avl.origin.left.value)
        self.assertEqual(0, avl.origin.left.height)
        self.assertEqual(5, avl.origin.right.value)
        self.assertEqual(1, avl.origin.right.height)
        self.assertEqual(7, avl.origin.right.right.value)
        self.assertEqual(0, avl.origin.right.right.height)

        """
        (6) Removing from a tree with a single node:
           5
        final structure (removing 5):
           Nothing
        """
        avl = AVLTree()
        avl.insert(avl.origin, 5)

        avl.remove(avl.origin, 5)
        self.assertEqual(0, avl.size)
        self.assertIsNone(avl.origin)

    def test_min(self):

        # ensure empty tree is properly handled
        avl = AVLTree()
        self.assertIsNone(avl.min(avl.origin))

        """(1) small sequential tree"""
        for i in range(10):
            avl.insert(avl.origin, i)
        min_node = avl.min(avl.origin)
        self.assertIsInstance(min_node, Node)
        self.assertEqual(0, min_node.value)

        """(2) large sequential tree"""
        avl = AVLTree()
        for i in range(-100, 101):
            avl.insert(avl.origin, i)
        min_node = avl.min(avl.origin)
        self.assertIsInstance(min_node, Node)
        self.assertEqual(-100, min_node.value)

        """(3) large random tree"""
        random.seed(331)
        avl = AVLTree()
        numbers = [random.randint(-1000, 1000) for _ in range(1000)]
        for num in numbers:
            avl.insert(avl.origin, num)
        min_node = avl.min(avl.origin)
        self.assertIsInstance(min_node, Node)
        self.assertEqual(min(numbers), min_node.value)

    def test_max(self):

        # ensure empty tree is properly handled
        avl = AVLTree()
        self.assertIsNone(avl.max(avl.origin))

        """(1) small sequential tree"""
        for i in range(10):
            avl.insert(avl.origin, i)
        max_node = avl.max(avl.origin)
        self.assertIsInstance(max_node, Node)
        self.assertEqual(9, max_node.value)

        """(2) large sequential tree"""
        avl = AVLTree()
        for i in range(-100, 101):
            avl.insert(avl.origin, i)
        max_node = avl.max(avl.origin)
        self.assertIsInstance(max_node, Node)
        self.assertEqual(100, max_node.value)

        """(3) large random tree"""
        random.seed(331)
        avl = AVLTree()
        numbers = [random.randint(-1000, 1000) for _ in range(1000)]
        for num in numbers:
            avl.insert(avl.origin, num)
        max_node = avl.max(avl.origin)
        self.assertIsInstance(max_node, Node)
        self.assertEqual(max(numbers), max_node.value)

    def test_search(self):

        # ensure empty tree is properly handled
        avl = AVLTree()
        self.assertIsNone(avl.search(avl.origin, 0))

        """
        (1) search small basic tree
        tree structure
          1
         / \
        0   3
           / \
          2   4
        """
        avl = AVLTree()
        numbers = [1, 0, 3, 2, 4]
        for num in numbers:
            avl.insert(avl.origin, num)
        # search existing numbers
        for num in numbers:
            node = avl.search(avl.origin, num)
            self.assertIsInstance(node, Node)
            self.assertEqual(num, node.value)
        # search non-existing numbers and ensure parent of where value would go is returned
        pairs = [(-1, 0), (0.5, 0), (5, 4), (2.5, 2),
                 (3.5, 4), (-1e5, 0), (1e5, 4)]
        for target, closest in pairs:
            node = avl.search(avl.origin, target)
            self.assertIsInstance(node, Node)
            self.assertEqual(closest, node.value)

        """(2) search large random tree"""
        random.seed(331)
        avl = AVLTree()
        numbers = {random.randint(-1000, 1000) for _ in range(1000)}
        for num in numbers:
            avl.insert(avl.origin, num)
        for num in numbers:
            # search existing number
            node = avl.search(avl.origin, num)
            self.assertIsInstance(node, Node)
            self.assertEqual(num, node.value)

            # if this node is a leaf, search non-existing numbers around it
            # to ensure it is returned as the parent of where new insertions would go
            if node.left is None and node.right is None:
                node = avl.search(avl.origin, num + 0.1)
                self.assertIsInstance(node, Node)
                self.assertEqual(num, node.value)
                node = avl.search(avl.origin, num - 0.1)
                self.assertIsInstance(node, Node)
                self.assertEqual(num, node.value)

    def test_inorder(self):

        # note: Python generators will raise a StopIteration exception when there are no items
        # left to yield, and we test for this exception to ensure each traversal yields the correct
        # number of items: https://docs.python.org/3/library/exceptions.html#StopIteration

        # ensure empty tree is properly handled and returns a StopIteration
        avl = AVLTree()
        with self.assertRaises(StopIteration):
            next(avl.inorder(avl.origin))

        """(1) small sequential tree"""
        for i in range(10):
            avl.insert(avl.origin, i)
        generator = avl.inorder(avl.origin)
        self.assertIsInstance(generator, types.GeneratorType)
        expected = list(range(10))
        print(avl)
        for num in expected:
            node = next(generator)
            print(node, "C")
            self.assertIsInstance(node, Node)
            self.assertEqual(num, node.value)
        with self.assertRaises(StopIteration):
            next(generator)

        """(2) large sequential tree"""
        avl = AVLTree()
        for i in range(-100, 101):
            avl.insert(avl.origin, i)
        generator = avl.inorder(avl.origin)
        self.assertIsInstance(generator, types.GeneratorType)
        expected = list(range(-100, 101))
        for num in expected:
            node = next(generator)
            self.assertIsInstance(node, Node)
            self.assertEqual(num, node.value)
        with self.assertRaises(StopIteration):
            next(generator)

        """(3) large random tree of unique numbers"""
        random.seed(331)
        avl = AVLTree()
        numbers = {random.randint(-1000, 1000) for _ in range(80)}
        for num in numbers:
            avl.insert(avl.origin, num)
        generator = avl.inorder(avl.origin)
        self.assertIsInstance(generator, types.GeneratorType)
        expected = sorted(numbers)
        for num in expected:
            node = next(generator)
            self.assertIsInstance(node, Node)
            self.assertEqual(num, node.value)
        with self.assertRaises(StopIteration):
            next(generator)

        """(4) Testing tree is iterable. Hint: Implement the __iter__ function."""
        for expected_val, actual in zip(expected, avl):
            self.assertEqual(expected_val, actual.value)

    def test_preorder(self):

        # note: Python generators will raise a StopIteration exception when there are no items
        # left to yield, and we test for this exception to ensure each traversal yields the correct
        # number of items: https://docs.python.org/3/library/exceptions.html#StopIteration

        # ensure empty tree is properly handled and returns a StopIteration
        avl = AVLTree()
        with self.assertRaises(StopIteration):
            next(avl.preorder(avl.origin))

        """(1) small sequential tree"""
        for i in range(10):
            avl.insert(avl.origin, i)
        generator = avl.preorder(avl.origin)
        self.assertIsInstance(generator, types.GeneratorType)
        expected = [3, 1, 0, 2, 7, 5, 4, 6, 8, 9]
        # avl.visualize("test2.svg")
        for num in expected:
            node = next(generator)
            self.assertIsInstance(node, Node)
            self.assertEqual(num, node.value)
        with self.assertRaises(StopIteration):
            next(generator)

        """(2) large sequential tree"""
        avl = AVLTree()
        for i in range(-20, 21):
            avl.insert(avl.origin, i)
        generator = avl.preorder(avl.origin)
        self.assertIsInstance(generator, types.GeneratorType)
        expected = [-5, -13, -17, -19, -20, -18, -15, -16, -14, -9, -11,
                    -12, -10, -7, -8, -6, 11, 3, -1, -3, -4, -2, 1, 0, 2,
                    7, 5, 4, 6, 9, 8, 10, 15, 13, 12, 14, 17, 16, 19, 18,
                    20]
        for num in expected:
            node = next(generator)
            self.assertIsInstance(node, Node)
            self.assertEqual(num, node.value)
        with self.assertRaises(StopIteration):
            next(generator)

        """(3) large random tree of unique numbers"""
        random.seed(331)
        avl = AVLTree()
        numbers = {random.randint(-1000, 1000) for _ in range(80)}
        for num in numbers:
            avl.insert(avl.origin, num)
        generator = avl.preorder(avl.origin)
        self.assertIsInstance(generator, types.GeneratorType)
        expected = [527, 33, -493, -834, -933, -954, -918, -655, -720,
                    -789, -705, -650, -529, -165, -343, -422, -434,
                    -359, -312, -324, -269, -113, -142, -148, -116, -43,
                    -89, -26, 327, 220, 108, 77, 44, 101, 193, 113,
                    194, 274, 251, 224, 268, 294, 283, 316, 454, 362, 358,
                    333, 360, 431, 411, 446, 486, 485, 498, 503,
                    711, 574, 565, 529, 571, 675, 641, 687, 832, 776, 733,
                    720, 775, 784, 782, 802, 914, 860, 843, 888,
                    966, 944, 975]
        for num in expected:
            node = next(generator)
            self.assertIsInstance(node, Node)
            self.assertEqual(num, node.value)
        with self.assertRaises(StopIteration):
            next(generator)

    def test_postorder(self):

        # note: Python generators will raise a StopIteration exception when there are no items
        # left to yield, and we test for this exception to ensure each traversal yields the correct
        # number of items: https://docs.python.org/3/library/exceptions.html#StopIteration

        # ensure empty tree is properly handled and returns a StopIteration
        avl = AVLTree()
        with self.assertRaises(StopIteration):
            next(avl.postorder(avl.origin))

        """(1) small sequential tree"""
        for i in range(10):
            avl.insert(avl.origin, i)
        generator = avl.postorder(avl.origin)
        self.assertIsInstance(generator, types.GeneratorType)
        expected = [0, 2, 1, 4, 6, 5, 9, 8, 7, 3]
        for num in expected:
            node = next(generator)
            self.assertIsInstance(node, Node)
            self.assertEqual(num, node.value)
        with self.assertRaises(StopIteration):
            next(generator)

        """(2) large sequential tree"""
        avl = AVLTree()
        for i in range(-20, 20):
            avl.insert(avl.origin, i)
        generator = avl.postorder(avl.origin)
        self.assertIsInstance(generator, types.GeneratorType)
        expected = [-20, -18, -19, -16, -14, -15, -17, -12, -10, -11, -8, -6, -7, -9,
                    -13, -4, -2, -3, 0, 2, 1, -1, 4, 6, 5, 8, 10, 9, 7, 3, 12, 14, 13,
                    16, 19, 18, 17, 15, 11, -5]
        for num in expected:
            node = next(generator)
            self.assertIsInstance(node, Node)
            self.assertEqual(num, node.value)
        with self.assertRaises(StopIteration):
            next(generator)

        """(3) large random tree of unique numbers"""
        random.seed(331)
        avl = AVLTree()
        numbers = {random.randint(-1000, 1000) for _ in range(80)}
        for num in numbers:
            avl.insert(avl.origin, num)
        generator = avl.postorder(avl.origin)
        self.assertIsInstance(generator, types.GeneratorType)
        expected = [-954, -918, -933, -789, -705, -720, -529, -650, -655, -834, -434, -359, -422, -324, -269, -312,
                    -343, -148, -116, -142, -89, -26, -43, -113, -
                    165, -493, 44, 101, 77, 113, 194, 193, 108, 224,
                    268, 251, 283, 316, 294, 274, 220, 333, 360, 358, 411, 446, 431, 362, 485, 503, 498, 486, 454,
                    327, 33, 529, 571, 565, 641, 687, 675, 574, 720, 775, 733, 782, 802, 784, 776, 843, 888, 860,
                    944, 975, 966, 914, 832, 711, 527]
        for num in expected:
            node = next(generator)
            self.assertIsInstance(node, Node)
            self.assertEqual(num, node.value)
        with self.assertRaises(StopIteration):
            next(generator)

    def test_levelorder(self):

        # note: Python generators will raise a StopIteration exception when there are no items
        # left to yield, and we test for this exception to ensure each traversal yields the correct
        # number of items: https://docs.python.org/3/library/exceptions.html#StopIteration

        # ensure empty tree is properly handled and returns a StopIteration
        avl = AVLTree()
        with self.assertRaises(StopIteration):
            next(avl.levelorder(avl.origin))

        """(1) small sequential tree"""
        for i in range(10):
            avl.insert(avl.origin, i)
        generator = avl.levelorder(avl.origin)
        self.assertIsInstance(generator, types.GeneratorType)
        expected = [3, 1, 7, 0, 2, 5, 8, 4, 6, 9]
        for num in expected:
            node = next(generator)
            self.assertIsInstance(node, Node)
            self.assertEqual(num, node.value)
        with self.assertRaises(StopIteration):
            next(generator)

        """(2) large sequential tree"""
        avl = AVLTree()
        for i in range(-20, 20):
            avl.insert(avl.origin, i)
        generator = avl.levelorder(avl.origin)
        self.assertIsInstance(generator, types.GeneratorType)
        expected = [-5, -13, 11, -17, -9, 3, 15, -19, -15, -11, -7, -1, 7, 13, 17, -20, -18,
                    -16, -14, -12, -10, -8, -6, -3, 1, 5, 9, 12, 14, 16, 18, -4, -2, 0, 2,
                    4, 6, 8, 10, 19]
        for num in expected:
            node = next(generator)
            self.assertIsInstance(node, Node)
            self.assertEqual(num, node.value)
        with self.assertRaises(StopIteration):
            next(generator)

        """(3) large random tree of unique numbers"""
        random.seed(331)
        avl = AVLTree()
        numbers = {random.randint(-1000, 1000) for _ in range(80)}
        for num in numbers:
            avl.insert(avl.origin, num)
        generator = avl.levelorder(avl.origin)
        self.assertIsInstance(generator, types.GeneratorType)
        expected = [527, 33, 711, -493, 327, 574, 832, -834, -165, 220, 454,
                    565, 675, 776, 914, -933, -655, -343, -113, 108, 274,
                    362, 486, 529, 571, 641, 687, 733, 784, 860, 966, -954,
                    -918, -720, -650, -422, -312, -142, -43, 77, 193, 251,
                    294, 358, 431, 485, 498, 720, 775, 782, 802, 843, 888,
                    944, 975, -789, -705, -529, -434, -359, -324, -269, -148,
                    -116, -89, -26, 44, 101, 113, 194, 224, 268, 283, 316, 333,
                    360, 411, 446, 503]
        for num in expected:
            node = next(generator)
            self.assertIsInstance(node, Node)
            self.assertEqual(num, node.value)
        with self.assertRaises(StopIteration):
            next(generator)

    def test_AVL_comprehensive(self):

        # visualize some of test in this testcase with https://www.cs.usfca.edu/~galles/visualization/AVLtree.html
        # ensure empty tree is properly handled
        """
        First part, inserting and removing without rotation

        insert without any rotation (inserting 5, 0, 10):
          5
         / \
        1   10
        """

        def check_node_properties(current: Node, value: int = 0, height: int = 0, balance: int = 0):
            if value is None:
                self.assertIsNone(current)
                return
            self.assertEqual(value, current.value)
            self.assertEqual(height, current.height)
            self.assertEqual(balance, avl.balance_factor(current))

        avl = AVLTree()
        avl.insert(avl.origin, 5)
        avl.insert(avl.origin, 1)
        avl.insert(avl.origin, 10)
        self.assertEqual(3, avl.size)
        self.assertEqual(1, avl.min(avl.origin).value)
        self.assertEqual(10, avl.max(avl.origin).value)
        # Properties of all nodes
        check_node_properties(avl.origin, value=5, height=1, balance=0)
        check_node_properties(avl.origin.left, value=1, height=0, balance=0)
        check_node_properties(avl.origin.right, value=10, height=0, balance=0)
        """
        Current AVL tree:
          5
         / \
        1   10
        After Removing 5:
          1
           \
            10
        """
        avl.remove(avl.origin, 5)
        self.assertEqual(2, avl.size)
        self.assertEqual(1, avl.min(avl.origin).value)
        self.assertEqual(10, avl.max(avl.origin).value)
        # Properties of all nodes
        check_node_properties(avl.origin, value=1, height=1, balance=-1)
        check_node_properties(avl.origin.left, value=None)
        check_node_properties(avl.origin.right, value=10, height=0, balance=0)
        """
        Current AVL tree:
          1
            \
            10
        After inserting 0, 20:
          1
         /  \
        0   10
              \
               20
        """
        avl.insert(avl.origin, 0)
        avl.insert(avl.origin, 20)
        self.assertEqual(4, avl.size)
        self.assertEqual(0, avl.min(avl.origin).value)
        self.assertEqual(20, avl.max(avl.origin).value)
        # Properties of all nodes
        check_node_properties(avl.origin, value=1, height=2, balance=-1)
        check_node_properties(avl.origin.left, value=0, height=0, balance=0)
        check_node_properties(avl.origin.right, value=10, height=1, balance=-1)
        check_node_properties(avl.origin.right.right,
                              value=20, height=0, balance=0)

        """
        Current AVL tree:
          1
         /  \
        0   10
              \
               20
        After removing 20, inserting -20 and inserting 5
             1
            /  \
           0   10
          /   /
        -20  5
        """
        avl.remove(avl.origin, 20)
        avl.insert(avl.origin, -20)
        avl.insert(avl.origin, 5)
        self.assertEqual(5, avl.size)
        self.assertEqual(-20, avl.min(avl.origin).value)
        self.assertEqual(10, avl.max(avl.origin).value)
        # Properties of all nodes
        check_node_properties(avl.origin, value=1, height=2, balance=0)
        check_node_properties(avl.origin.left, value=0, height=1, balance=1)
        check_node_properties(avl.origin.left.left,
                              value=-20, height=0, balance=0)
        check_node_properties(avl.origin.right, value=10, height=1, balance=1)
        check_node_properties(avl.origin.right.left,
                              value=5, height=0, balance=0)

        """
        Second part, inserting and removing with rotation

        inserting 5, 10:
          5
           \
            10
        """
        avl = AVLTree()
        avl.insert(avl.origin, 5)
        avl.insert(avl.origin, 10)
        self.assertEqual(2, avl.size)
        self.assertEqual(5, avl.min(avl.origin).value)
        self.assertEqual(10, avl.max(avl.origin).value)
        # Properties of all nodes
        check_node_properties(avl.origin, value=5, height=1, balance=-1)
        check_node_properties(avl.origin.right, value=10, height=0, balance=0)
        """
        Current AVL tree:
          5
           \
            10
        After inserting 8, 9, 12
           8
         /   \
        5    10
            /  \
           9   12
        """
        avl.insert(avl.origin, 8)
        avl.insert(avl.origin, 9)
        avl.insert(avl.origin, 12)
        self.assertEqual(5, avl.size)
        self.assertEqual(5, avl.min(avl.origin).value)
        self.assertEqual(12, avl.max(avl.origin).value)
        # Properties of all nodes
        check_node_properties(avl.origin, value=8, height=2, balance=-1)
        check_node_properties(avl.origin.right, value=10, height=1, balance=0)
        check_node_properties(avl.origin.right.left,
                              value=9, height=0, balance=0)
        check_node_properties(avl.origin.right.right,
                              value=12, height=0, balance=0)
        check_node_properties(avl.origin.left, value=5, height=0, balance=0)

        """
        Current AVL tree:
           8
         /   \
        5    10
            /  \
           9   12
        After inserting 3, 1, 2
               8
           /       \
          3        10
         /  \     /   \
        1    5   9    12
          \
           2
        """
        avl.insert(avl.origin, 3)
        avl.insert(avl.origin, 1)
        avl.insert(avl.origin, 2)
        self.assertEqual(8, avl.size)
        self.assertEqual(1, avl.min(avl.origin).value)
        self.assertEqual(12, avl.max(avl.origin).value)
        # Properties of all nodes
        check_node_properties(avl.origin, value=8, height=3, balance=1)
        check_node_properties(avl.origin.right, value=10, height=1, balance=0)
        check_node_properties(avl.origin.right.left,
                              value=9, height=0, balance=0)
        check_node_properties(avl.origin.right.right,
                              value=12, height=0, balance=0)
        check_node_properties(avl.origin.left, value=3, height=2, balance=1)
        check_node_properties(avl.origin.left.left,
                              value=1, height=1, balance=-1)
        check_node_properties(avl.origin.left.left.right,
                              value=2, height=0, balance=0)
        check_node_properties(avl.origin.left.right,
                              value=5, height=0, balance=0)
        """
        Current AVL tree:
               8
           /       \
          3        10
         /  \     /   \
        1    5   9    12
          \
           2
        After removing 5
               8
           /       \
          2        10
         /  \     /   \
        1    3   9    12
        """
        avl.remove(avl.origin, 5)
        self.assertEqual(7, avl.size)
        self.assertEqual(1, avl.min(avl.origin).value)
        self.assertEqual(12, avl.max(avl.origin).value)
        # Properties of all nodes
        check_node_properties(avl.origin, value=8, height=2, balance=0)
        check_node_properties(avl.origin.right, value=10, height=1, balance=0)
        check_node_properties(avl.origin.right.left,
                              value=9, height=0, balance=0)
        check_node_properties(avl.origin.right.right,
                              value=12, height=0, balance=0)
        check_node_properties(avl.origin.left, value=2, height=1, balance=0)
        check_node_properties(avl.origin.left.left,
                              value=1, height=0, balance=0)
        check_node_properties(avl.origin.left.right,
                              value=3, height=0, balance=0)
        """
        Current AVL tree:
              8
           /     \
          2      10
         /  \   /   \
        1    3 9    12
        After inserting 5, 13, 0, 7, 20
               8
            /       \
           2         10
          /  \      /   \
         1    5     9    13
        /    / \        /  \
        0   3   7     12    20
        """
        avl.insert(avl.origin, 5)
        avl.insert(avl.origin, 13)
        avl.insert(avl.origin, 0)
        avl.insert(avl.origin, 7)
        avl.insert(avl.origin, 20)
        self.assertEqual(12, avl.size)
        self.assertEqual(0, avl.min(avl.origin).value)
        self.assertEqual(20, avl.max(avl.origin).value)
        # Properties of all nodes
        check_node_properties(avl.origin, value=8, height=3, balance=0)

        check_node_properties(avl.origin.right, value=10, height=2, balance=-1)
        check_node_properties(avl.origin.right.left,
                              value=9, height=0, balance=0)
        check_node_properties(avl.origin.right.right,
                              value=13, height=1, balance=0)
        check_node_properties(avl.origin.right.right.right,
                              value=20, height=0, balance=0)
        check_node_properties(avl.origin.right.right.left,
                              value=12, height=0, balance=0)

        check_node_properties(avl.origin.left, value=2, height=2, balance=0)
        check_node_properties(avl.origin.left.left,
                              value=1, height=1, balance=1)
        check_node_properties(avl.origin.left.left.left,
                              value=0, height=0, balance=0)
        check_node_properties(avl.origin.left.right,
                              value=5, height=1, balance=-0)
        check_node_properties(avl.origin.left.right.right,
                              value=7, height=0, balance=0)
        check_node_properties(avl.origin.left.right.left,
                              value=3, height=0, balance=0)

        """
        Current AVL tree:
               8
            /       \
           2         10
          /  \      /   \
         1    5     9    13
        /    / \        /  \
        0   3   7     12    20
        After removing 1, 9
               8
            /       \
           2         13
          /  \      /   \
         0    5   10     20
             / \     \    
             3   7    12
        """
        avl.remove(avl.origin, 1)
        avl.remove(avl.origin, 9)
        self.assertEqual(10, avl.size)
        self.assertEqual(0, avl.min(avl.origin).value)
        self.assertEqual(20, avl.max(avl.origin).value)
        # Properties of all nodes
        check_node_properties(avl.origin, value=8, height=3, balance=0)

        check_node_properties(avl.origin.right, value=13, height=2, balance=1)
        check_node_properties(avl.origin.right.left,
                              value=10, height=1, balance=-1)
        check_node_properties(avl.origin.right.left.right,
                              value=12, height=0, balance=0)
        check_node_properties(avl.origin.right.right,
                              value=20, height=0, balance=0)

        check_node_properties(avl.origin.left, value=2, height=2, balance=-1)
        check_node_properties(avl.origin.left.left,
                              value=0, height=0, balance=0)
        check_node_properties(avl.origin.left.right,
                              value=5, height=1, balance=-0)
        check_node_properties(avl.origin.left.right.right,
                              value=7, height=0, balance=0)
        check_node_properties(avl.origin.left.right.left,
                              value=3, height=0, balance=0)

#     def test_knn(self):
#         """
#         Testing specs examples
#         """
#         data = [(0.1, "L"), (0.2, "L"), (0.6, "W"), (0.7, "W"), (0.5, "W")]
#         classifier = KNNClassifier(k=2)
#         classifier.train(data)
#         self.assertEqual(classifier.classify(0.55),"W")

#         data = [(0.1, "L"), (0.2, "L"), (0.6, "W"), (0.7, "W")]
#         classifier = KNNClassifier()
#         classifier.train(data)
#         self.assertIsNone(classifier.classify(0.4))

#         data = [(0.1, "L"), (0.2, "L"), (0.6, "W"), (0.7, "W"), (0.5, "L")]
#         classifier = KNNClassifier()
#         classifier.train(data)
#         self.assertEqual(classifier.classify(0.4), "L")

#         # Testing 1 closest neighbor
#         data = [(0.18, "night"), (0.21, "night"), (0.29, "night"), (0.46, "night"),
#         (0.49, "night"), (0.51, "day"), (0.53, "day"),
#         (0.97, "day"), (0.98, "day"), (0.99, "day")]
#         classifier = KNNClassifier()
#         classifier.train(data)
#         test_predictions = [0.1, 0.2, 0.5, 0.8, 0.9]
#         expected = ["night", "night", "day", "day", "day"]
#         actual = [classifier.classify(i) for i in test_predictions]
#         self.assertEqual(expected, actual)

#         # Testing 2 closest neighbors
#         classifier = KNNClassifier(k=2)
#         classifier.train(data)
#         test_predictions = [0.1, 0.2, 0.5, 0.8, 0.9]
#         expected = ["night", "night", "day", "day", "day"]
#         actual = [classifier.classify(i) for i in test_predictions]
#         self.assertEqual(expected, actual)

#         # Testing 3 closest neighbors, weights make a difference here. Even if there are more neighbors for one classification.
#         classifier = KNNClassifier(k=3)
#         classifier.train(data)
#         test_predictions = [0.1, 0.2, 0.5, 0.8, 0.9]
#         expected = ["night", "night", "day", "day", "day"]
#         actual = [classifier.classify(i) for i in test_predictions]
#         self.assertEqual(expected, actual)

#         # Changing weights to affect classification
#         data[2] = (0.43, "night")
#         classifier = KNNClassifier(k=3)
#         classifier.train(data)
#         test_predictions = [0.1, 0.2, 0.5, 0.8, 0.9]
#         expected = ["night", "night", "night", "day", "day"]
#         actual = [classifier.classify(i) for i in test_predictions]
#         self.assertEqual(expected, actual)
    
#         #Test tied weights/distances
#         points = [i/10 for i in range(0,11) if i != 5]
#         labels = ["day"] * 5 + ["night"]*5
#         data = zip(points, labels)
#         classifier = KNNClassifier()
#         classifier.train(data)
#         self.assertIsNone(classifier.classify(0.5))

#         classifier = KNNClassifier(k=3)
#         classifier.train(data)
#         self.assertIsNone(classifier.classify(0.5))

#         classifier = KNNClassifier(k=4)
#         classifier.train(data)
#         self.assertIsNone(classifier.classify(0.5))

#         # Test from previous projects
#         random.seed(331)
#         night_images = [(random.random() / 2, "night") for _ in range(50)]
#         day_images = [(random.random() / 2 + 0.5, "day") for _ in range(50)]
#         data = night_images + day_images

#         classifier = KNNClassifier()
#         classifier.train(data)
#         test_images = [0.1, 0.2, 0.3, 0.4, 0.6, 0.7, 0.8, 0.9]
#         expected = ["night"] * 4 + ["day"] * 4
#         actual = [classifier.classify(image) for image in test_images]
#         self.assertEqual(expected, actual)


if __name__ == '__main__':
    unittest.main(verbosity=2)
