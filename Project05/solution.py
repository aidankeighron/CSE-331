"""
Project 5
CSE 331 FS24 
solution.py
"""
from collections import deque
import math
from typing import TypeVar, Generator, List, Tuple, Optional
from queue import SimpleQueue

# for more information on typehinting, check out https://docs.python.org/3/library/typing.html
T = TypeVar("T")  # represents generic type
# represents a Node object (forward-declare to use in Node __init__)
Node = TypeVar("Node")
# represents a custom type used in application
AVLWrappedDictionary = TypeVar("AVLWrappedDictionary")


class Node:
    """
    Implementation of an BST and AVL tree node.
    Do not modify.
    """
    # preallocate storage: see https://stackoverflow.com/questions/472000/usage-of-slots
    __slots__ = ["value", "parent", "left", "right", "height", "data"]

    def __init__(self, value: T, parent: Node = None,
                 left: Node = None, right: Node = None, data: str = None) -> None:
        """
        Construct an AVL tree node.

        :param value: value held by the node object
        :param parent: ref to parent node of which this node is a child
        :param left: ref to left child node of this node
        :param right: ref to right child node of this node
        :param data: Optional parameter to store data in Node, used in the application problem.
        """
        self.value = value
        self.parent, self.left, self.right = parent, left, right
        self.height = 0
        self.data = data

    def __repr__(self) -> str:
        """
        Represent the AVL tree node as a string.

        :return: string representation of the node.
        """
        return f"<{str(self.value)}>"

    def __str__(self) -> str:
        """
        Represent the AVL tree node as a string.

        :return: string representation of the node.
        """
        return repr(self)


####################################################################################################

class BinarySearchTree:
    """
    Implementation of an BSTree.
    Modify only below indicated line.
    """

    # preallocate storage: see https://stackoverflow.com/questions/472000/usage-of-slots
    __slots__ = ["origin", "size"]

    def __init__(self) -> None:
        """
        Construct an empty BST tree.
        """
        self.origin = None
        self.size = 0

    def __repr__(self) -> str:
        """
        Represent the BSTree as a string.

        :return: string representation of the BST tree
        """
        if self.origin is None:
            return "Empty BST Tree"

        lines = pretty_print_binary_tree(self.origin, 0, False, '-')[0]
        return "\n" + "\n".join((line.rstrip() for line in lines))

    def __str__(self) -> str:
        """
        Represent the BSTree as a string.

        :return: string representation of the BSTree
        """
        return repr(self)

    ########################################
    # Implement functions below this line. #
    ########################################

    def height(self, root: Node) -> int:
        """
        Gets the height of a subtree        

        :param root: subtree to get height of
        :return: height
        """
        if root is None:
          return -1
        return root.height

    def insert(self, root: Node, val: T) -> None:
        """
        Inserts a node into a subtree

        :param root: subtree to insert a node into
        :param val: node value to insert
        :return: None
        """
        def update_height(root: Node, height: int) -> None:
            if root is None:
                return
            root.height = max(height, root.height)
            update_height(root.parent, height+1)

        if root is None and self.origin is None:
            node = Node(val)
            self.origin = node
            self.size += 1
            return
            
        if root is None or root.value == val:
            return
        if val > root.value:
            if root.right:
                self.insert(root.right, val)
                return
            node = Node(val, root)
            root.right = node
        else:
            if root.left:
                self.insert(root.left, val)
                return
            node = Node(val, root)
            root.left = node
        # node.height = root.height+1
        update_height(root, 1)
        self.size += 1


    def remove(self, root: Node, val: T) -> Optional[Node]:
        """
        Removes a node from a subtree

        :param root: subtree to remove a node from
        :param val: value to remove from the subtree
        :return: subtree after removal
        """
        def update_height(root: Node) -> None:
            if root is None:
                return
            root.height = max(self.height(root.left)+1, self.height(root.right)+1)
            update_height(root.parent)

        if root is None:
            return root
        if root.value == val:
            self.size -= 1
            if root.left is None and root.right is None:
                if root.parent is None:
                    self.origin = None
                    return None
                elif root.parent.left is root:
                    root.parent.left = None
                else:
                    root.parent.right = None
                root.parent.height = 0
                update_height(root.parent)
                return None
            elif root.left is None:
                if root.parent is None:
                    self.origin = root.right
                    self.origin.parent = None
                if root.parent.left is root:
                    root.parent.left = root.right
                    root.right.parent = root.parent
                else:
                    root.parent.right = root.right
                    root.right.parent = root.parent
                update_height(root.parent)
                return root.right
            elif root.right is None:
                if root.parent is None:
                    self.origin = root.left
                    self.origin.parent = None
                elif root.parent.left is root:
                    root.parent.left = root.left
                    root.left.parent = root.parent
                else:
                    root.parent.right = root.left
                    root.left.parent = root.parent
                update_height(root.parent)
                return root.left
            else:
                self.size += 1
                successor = root.left
                while successor.right is not None:
                    successor = successor.right
                root.value, successor.value = successor.value, root.value
                return self.remove(root.left, successor.value)

        if val > root.value:
            return self.remove(root.right, val)
        else:
            return self.remove(root.left, val)

    def search(self, root: Node, val: T) -> Optional[Node]:
        """
        Searches for a node in a subtree

        :param root: subtree to search for a node in
        :param val: value to search for
        :return: if node exists return the node else return None
        """
        if root is None:
            return None
        if root.value == val:
            return root
        if val > root.value:
            if root.right is None:
                return root
            return self.search(root.right, val)
        else:
            if root.left is None:
                return root
            return self.search(root.left, val)



class AVLTree(BinarySearchTree):
    """
    Implementation of an AVL tree.
    Modify only below indicated line.
    """

    __slots__ = ["origin", "size"]

    def __init__(self) -> None:
        """
        Construct an empty AVL tree.
        """
        self.origin = None
        self.size = 0

    def __repr__(self) -> str:
        """
        Represent the AVL tree as a string.

        :return: string representation of the AVL tree
        """
        if self.origin is None:
            return "Empty AVL Tree"

        return super(AVLTree, self).__repr__()

    def __str__(self) -> str:
        """
        Represent the AVLTree as a string.

        :return: string representation of the BSTree
        """

        return repr(self)

    ########################################
    # Implement functions below this line. #
    ########################################

    def height(self, root: Node) -> int:
        """
        Height of the subtree

        :param root: subtree to get the height of
        :return: height
        """
        if root is None:
            return -1
        return root.height

    def left_rotate(self, root: Node) -> Optional[Node]:
        """
        Rotates root subtree to the right

        :param root: subtree to rotate
        :return: new root of the subtree
        """
        if root is None:
            return
        def update_height(root: Node) -> None:
            if root is None:
                return

            root.height = max(self.height(root.left)+1, self.height(root.right)+1)
            update_height(root.parent)

        def set_child(root, right, child):
            if right:
                root.right = child
            else:
                root.left = child
            if child is not None:
                child.parent = root
            update_height(root)

        right_left = root.right.left
        if root.parent != None:
            if root.parent.right == root:
                set_child(root.parent, True, root.right)
            elif root.parent.left == root:
                set_child(root.parent, False, root.right)
        else:
            self.origin = root.right
            self.origin.parent = None

        set_child(root.right, False, root)
        set_child(root, True, right_left)

        return root.parent

    def right_rotate(self, root: Node) -> Optional[Node]:
        """
        Rotates a subtree to the right

        :param root: subtree to rotate
        :return: new root node
        """
        if root is None:
            return
        
        def update_height(root: Node) -> None:
            if root is None:
                return
            root.height = max(self.height(root.left)+1, self.height(root.right)+1)
            update_height(root.parent)

        def set_child(root, right, child):
            if right:
                root.right = child
            else:
                root.left = child
            if child is not None:
                child.parent = root
            
            update_height(root)

        left_right = root.left.right
        if root.parent != None:
            if root.parent.left == root:
                set_child(root.parent, False, root.left)
            elif root.parent.right == root:
                set_child(root.parent, True, root.left)
        else:
            self.origin = root.left
            self.origin.parent = None

        set_child(root.left, True, root)
        set_child(root, False, left_right)
        
        return root.parent

    def balance_factor(self, root: Node) -> int:
        """
        gets the balance factor of a subtree

        :param root: subtree to get the balance factor of
        :return: balance factor
        """
        if root is None:
            return 0
        left = self.height(root.left)
        right = self.height(root.right)
        return left - right

    def rebalance(self, root: Node) -> Optional[Node]:
        """
        rebalance a subtree to ensure the balance factor is between -1 and 1

        :param root: subtree to balance
        :return: root of balanced subtree
        """
        if self.balance_factor(root) == -2:
            if self.balance_factor(root.right) == 1:
                self.right_rotate(root.right)
            return self.left_rotate(root)
        elif self.balance_factor(root) == 2:
            if self.balance_factor(root.left) == -1:
                self.left_rotate(root.left)
            return self.right_rotate(root)
        return root

    def insert(self, root: Node, val: T, data: str = None) -> Optional[Node]:
        """
        inserts a node into subtree making sure the tree is balanced

        :param root: subtree to insert into 
        :param val: value of inserted node
        :param data: data of inserted node
        :return: root of the subtree after insertion
        """
        def insert_node(root, value):
            def update_height(root: Node, height: int) -> None:
                if root is None:
                    return
                root.height = max(height, root.height)
                update_height(root.parent, height+1)

            if root is None and self.origin is None:
                node = Node(value, data=data)
                self.origin = node
                self.size += 1
                return
                
            if root is None or root.value == value:
                return
            if value > root.value:
                if root.right:
                    self.insert(root.right, value, data)
                    return
                node = Node(value, root, data=data)
                root.right = node
            else:
                if root.left:
                    self.insert(root.left, value, data)
                    return
                node = Node(value, root, data=data)
                root.left = node

            update_height(root, 1)
            self.size += 1

        insert_node(root, val)

        if root is None:
            root = self.origin
        root = self.rebalance(root)
        return root

    def remove(self, root: Node, val: T) -> Optional[Node]:
        """
        removes a node from a subtree making sure to keep it balanced

        :param root: subtree to remove node from
        :param val: value of the node to remove
        :return: subtree after removal
        """
        node = super().remove(root, val)
        if node is None:
            return root
        root = self.rebalance(root)
        return root

    def min(self, root: Node) -> Optional[Node]:
        """
        minimum value of the subtree

        :param root: subtree to find the min of 
        :return: min of the subtree
        """
        if root is None:
            return None
        while root.left:
            root = root.left
        return root

    def max(self, root: Node) -> Optional[Node]:
        """
        maximum value of the subtree

        :param root: subtree to find the max of 
        :return: max of the subtree
        """
        if root is None:
            return None
        while root.right:
            root = root.right
        return root

    def search(self, root: Node, val: T) -> Optional[Node]:
        """
        searches for a node within a subtree

        :param root: subtree to search for node in 
        :param val: value to search for  
        :return: the node if it exists in the tree else None
        """
        return super().search(root, val)

    def inorder(self, root: Node) -> Generator[Node, None, None]:
        """
        inorder of a subtree

        :param root: subtree to traverse 
        :return: generator for the traversal
        """
        if root is None:
            return StopIteration
        
        yield from self.inorder(root.left)
        yield root
        yield from self.inorder(root.right)

    def __iter__(self) -> Generator[Node, None, None]:
        """
        iterator for the entire tree
 
        :return: generator for the tree
        """
        return self.inorder(self.origin)

    def preorder(self, root: Node) -> Generator[Node, None, None]:
        """
        preorder of a subtree

        :param root: subtree to traverse 
        :return: generator for the traversal
        """
        if root is None:
            return StopIteration
        
        yield root
        yield from self.preorder(root.left)
        yield from self.preorder(root.right)

    def postorder(self, root: Node) -> Generator[Node, None, None]:
        """
        postorder of a subtree

        :param root: subtree to traverse 
        :return: generator for the traversal
        """
        if root is None:
            return StopIteration
        
        yield from self.postorder(root.left)
        yield from self.postorder(root.right)
        yield root

    def levelorder(self, root: Node) -> Generator[Node, None, None]:
        """
        levelorder of a subtree

        :param root: subtree to traverse 
        :return: generator for the traversal
        """
        queue = SimpleQueue()
        queue.put(root)
        while not queue.empty():
            new_queue = SimpleQueue()
            while not queue.empty():
                node = queue.get_nowait()

                if node is None:
                    continue

                yield node

                new_queue.put(node.left)
                new_queue.put(node.right)
        
            queue = new_queue
        return StopIteration
# Classifier
class KNNClassifier:

    ########################################################
    # DON'T MODIFY BELOW #
    ########################################################

    def __init__(self, k: int = 1):
        """
        KNN Classifier class that uses the k nearest neighbors algorithm to classify a data point
        :param k: Number of close neighbors to consider for classification
        :return: None
        """
        self.k = k
        self.tree = AVLTree()

       
    def floats_equal(self, f1:float, f2: float) -> bool:
        """
        Compares two floats using threshold to check if numbers are equal due to floating point error
        :param f1: First float
        :param f2: Second float
        :return: True if they are the same, false otherwise
        """
        return abs(f1 - f2) <= 1e-10
    
    ########################################
    # Implement functions below this line. #
    ######################################## 
    def train(self, data: List[Tuple[float, str]]) -> None:
        """
        trains the classifier by adding nodes into a tree

        :param data: list of node to add 
        :return: None
        """
        for val, d in data:
            self.tree.insert(self.tree.origin, val, data=d)
    
    def get_k_neighbors(self, value: float) -> List[Tuple[float, str]]:
        """
        gets the k nearest elements to the provided value removing ties

        :param value: value to compare with 
        :return: list of k nearest neighbors
        """
        nodes = []
        for node in self.tree:
            difference = abs(node.value - value)
            nodes.append((difference, node.value, node.data))

        if not nodes:
            return []

        # Sort by distance
        nodes.sort(key=lambda node: node[0])
        
        # Get k neighbors, handling ties
        neighbors = []
        prev_distance = None
        
        for i, (distance, val, data) in enumerate(nodes):
            if len(neighbors) == self.k:
                if i < len(nodes) and self.floats_equal(distance, nodes[i-1][0]):
                    neighbors.pop()
                    continue
                break
            
            if prev_distance is None and len(nodes) >= 2:
                prev_distance = nodes[1][0]

            if prev_distance is None or not self.floats_equal(distance, prev_distance):
                neighbors.append((val, data))
                prev_distance = distance

        return neighbors
    
    def calculate_best_fit(self, neighbors: List[Tuple[float, str]], value: float) -> str:
        """
        calculates the best fitting neighbor given a list of neighbors

        :param neighbors: neighbors to compare  
        :return: best fitting neighbor
        """
        if not neighbors:
            return None
        
        weights = {}
        for val, data in neighbors:
            weight = 1 / abs(value - val)
            weights[data] = (weights[data] if data in weights else 0) + weight

        return max(weights.items(), key=lambda node: node[1])[0]
    
    def classify(self, value: float) -> str:
        """
        finds the best fitting neighbor given a value to compare it against

        :param value: value to compare against 
        :return: best fitting neighbor
        """
        neighbors = self.get_k_neighbors(value)
        best_fit = self.calculate_best_fit(neighbors, value)
        return best_fit


########################################################
# DON'T MODIFY BELOW #
########################################################

def is_avl_tree(node):
    def is_avl_tree_inner(cur, high, low):
        # if node is None at any time, it is balanced and therefore True
        if cur is None:
            return True, -1
        if cur.value > high or cur.value < low:
            return False, -1
        is_avl_left, left_height = is_avl_tree_inner(cur.left, cur.value, low)
        is_avl_right, right_height = is_avl_tree_inner(cur.right, high, cur.value)
        cur_height = max(left_height, right_height) + 1
        return is_avl_left and is_avl_right and abs(left_height - right_height) < 2, cur_height

    # absolute difference between right and left subtree should be no greater than 1
    return is_avl_tree_inner(node, float('inf'), -float('inf'))[0]



_SVG_XML_TEMPLATE = """
<svg width="{width}" height="{height}" xmlns="http://www.w3.org/2000/svg">
<style>
    .value {{
        font: 300 16px monospace;
        text-align: center;
        dominant-baseline: middle;
        text-anchor: middle;
    }}
    .dict {{
        font: 300 16px monospace;
        dominant-baseline: middle;
    }}
    .node {{
        fill: lightgray;
        stroke-width: 1;
    }}
</style>
<g stroke="#000000">
{body}
</g>
</svg>
"""

_NNC_DICT_BOX_TEXT_TEMPLATE = """<text class="dict" y="{y}" xml:space="preserve">
    <tspan x="{label_x}" dy="1.2em">{label}</tspan>
    <tspan x="{bracket_x}" dy="1.2em">{{</tspan>
    {values}
    <tspan x="{bracket_x}" dy="1.2em">}}</tspan>
</text>
"""


def pretty_print_binary_tree(root: Node, curr_index: int, include_index: bool = False,
                             delimiter: str = "-", ) -> \
        Tuple[List[str], int, int, int]:
    """
    Taken from: https://github.com/joowani/binarytree

    Recursively walk down the binary tree and build a pretty-print string.
    In each recursive call, a "box" of characters visually representing the
    current (sub)tree is constructed line by line. Each line is padded with
    whitespaces to ensure all lines in the box have the same length. Then the
    box, its width, and start-end positions of its root node value repr string
    (required for drawing branches) are sent up to the parent call. The parent
    call then combines its left and right sub-boxes to build a larger box etc.
    :param root: Root node of the binary tree.
    :type root: binarytree.Node | None
    :param curr_index: Level-order_ index of the current node (root node is 0).
    :type curr_index: int
    :param include_index: If set to True, include the level-order_ node indexes using
        the following format: ``{index}{delimiter}{value}`` (default: False).
    :type include_index: bool
    :param delimiter: Delimiter character between the node index and the node
        value (default: '-').
    :type delimiter:
    :return: Box of characters visually representing the current subtree, width
        of the box, and start-end positions of the repr string of the new root
        node value.
    :rtype: ([str], int, int, int)
    .. _Level-order:
        https://en.wikipedia.org/wiki/Tree_traversal#Breadth-first_search
    """
    if root is None:
        return [], 0, 0, 0

    line1 = []
    line2 = []
    if include_index:
        node_repr = "{}{}{}".format(curr_index, delimiter, root.value)
    else:
        node_repr = f'{root.value},h={root.height},' \
                    f'⬆{str(root.parent.value) if root.parent else "None"}'

    new_root_width = gap_size = len(node_repr)

    # Get the left and right sub-boxes, their widths, and root repr positions
    l_box, l_box_width, l_root_start, l_root_end = pretty_print_binary_tree(
        root.left, 2 * curr_index + 1, include_index, delimiter
    )
    r_box, r_box_width, r_root_start, r_root_end = pretty_print_binary_tree(
        root.right, 2 * curr_index + 2, include_index, delimiter
    )

    # Draw the branch connecting the current root node to the left sub-box
    # Pad the line with whitespaces where necessary
    if l_box_width > 0:
        l_root = (l_root_start + l_root_end) // 2 + 1
        line1.append(" " * (l_root + 1))
        line1.append("_" * (l_box_width - l_root))
        line2.append(" " * l_root + "/")
        line2.append(" " * (l_box_width - l_root))
        new_root_start = l_box_width + 1
        gap_size += 1
    else:
        new_root_start = 0

    # Draw the representation of the current root node
    line1.append(node_repr)
    line2.append(" " * new_root_width)

    # Draw the branch connecting the current root node to the right sub-box
    # Pad the line with whitespaces where necessary
    if r_box_width > 0:
        r_root = (r_root_start + r_root_end) // 2
        line1.append("_" * r_root)
        line1.append(" " * (r_box_width - r_root + 1))
        line2.append(" " * r_root + "\\")
        line2.append(" " * (r_box_width - r_root))
        gap_size += 1
    new_root_end = new_root_start + new_root_width - 1

    # Combine the left and right sub-boxes with the branches drawn above
    gap = " " * gap_size
    new_box = ["".join(line1), "".join(line2)]
    for i in range(max(len(l_box), len(r_box))):
        l_line = l_box[i] if i < len(l_box) else " " * l_box_width
        r_line = r_box[i] if i < len(r_box) else " " * r_box_width
        new_box.append(l_line + gap + r_line)

    # Return the new box, its width and its root repr positions
    return new_box, len(new_box[0]), new_root_start, new_root_end


def svg(root: Node, node_radius: int = 16, nnc_mode=False) -> str:
    """
    Taken from: https://github.com/joowani/binarytree

    Generate SVG XML.
    :param root: Generate SVG for tree rooted at root
    :param node_radius: Node radius in pixels (default: 16).
    :type node_radius: int
    :return: Raw SVG XML.
    :rtype: str
    """
    tree_height = root.height
    scale = node_radius * 3
    xml = deque()
    nodes_for_nnc_visualization = []

    def scale_x(x: int, y: int) -> float:
        diff = tree_height - y
        x = 2 ** (diff + 1) * x + 2 ** diff - 1
        return 1 + node_radius + scale * x / 2

    def scale_y(y: int) -> float:
        return scale * (1 + y)

    def add_edge(parent_x: int, parent_y: int, node_x: int, node_y: int) -> None:
        xml.appendleft(
            '<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}"/>'.format(
                x1=scale_x(parent_x, parent_y),
                y1=scale_y(parent_y),
                x2=scale_x(node_x, node_y),
                y2=scale_y(node_y),
            )
        )

    def add_node(node_x: int, node_y: int, node: Node) -> None:
        x, y = scale_x(node_x, node_y), scale_y(node_y)
        xml.append(f'<circle class="node" cx="{x}" cy="{y}" r="{node_radius}"/>')

        if nnc_mode:
            nodes_for_nnc_visualization.append(node.value)
            xml.append(f'<text class="value" x="{x}" y="{y + 5}">key={node.value.key}</text>')
        else:
            xml.append(f'<text class="value" x="{x}" y="{y + 5}">{node.value}</text>')

    current_nodes = [root.left, root.right]
    has_more_nodes = True
    y = 1

    add_node(0, 0, root)

    while has_more_nodes:

        has_more_nodes = False
        next_nodes: List[Node] = []

        for x, node in enumerate(current_nodes):
            if node is None:
                next_nodes.append(None)
                next_nodes.append(None)
            else:
                if node.left is not None or node.right is not None:
                    has_more_nodes = True

                add_edge(x // 2, y - 1, x, y)
                add_node(x, y, node)

                next_nodes.append(node.left)
                next_nodes.append(node.right)

        current_nodes = next_nodes
        y += 1

    svg_width = scale * (2 ** tree_height)
    svg_height = scale * (2 + tree_height)
    if nnc_mode:

        line_height = 20
        box_spacing = 10
        box_margin = 5
        character_width = 10

        max_key_count = max(map(lambda obj: len(obj.dictionary), nodes_for_nnc_visualization))
        box_height = (max_key_count + 3) * line_height + box_margin

        def max_length_item_of_node_dict(node):
            # Check if dict is empty so max doesn't throw exception
            if len(node.dictionary) > 0:
                item_lengths = map(lambda pair: len(str(pair)), node.dictionary.items())
                return max(item_lengths)
            return 0

        max_value_length = max(map(max_length_item_of_node_dict, nodes_for_nnc_visualization))
        box_width = max(max_value_length * character_width, 110)

        boxes_per_row = svg_width // box_width
        rows_needed = math.ceil(len(nodes_for_nnc_visualization) / boxes_per_row)

        nodes_for_nnc_visualization.sort(key=lambda node: node.key)
        for index, node in enumerate(nodes_for_nnc_visualization):
            curr_row = index // boxes_per_row
            curr_column = index % boxes_per_row

            box_x = curr_column * (box_width + box_spacing)
            box_y = curr_row * (box_height + box_spacing) + svg_height
            box = f'<rect x="{box_x}" y="{box_y}" width="{box_width}" ' \
                  f'height="{box_height}" fill="white" />'
            xml.append(box)

            value_template = '<tspan x="{value_x}" dy="1.2em">{key}: {value}</tspan>'
            text_x = box_x + 10

            def item_pair_to_svg(pair):
                return value_template.format(key=pair[0], value=pair[1], value_x=text_x + 10)

            values = map(item_pair_to_svg, node.dictionary.items())
            text = _NNC_DICT_BOX_TEXT_TEMPLATE.format(
                y=box_y,
                label=f"key = {node.key}",
                label_x=text_x,
                bracket_x=text_x,
                values='\n'.join(values)
            )
            xml.append(text)

        svg_width = boxes_per_row * (box_width + box_spacing * 2)
        svg_height += rows_needed * (box_height + box_spacing * 2)

    return _SVG_XML_TEMPLATE.format(
        width=svg_width,
        height=svg_height,
        body="\n".join(xml),
    )