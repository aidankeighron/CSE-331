import unittest


class DoublyLinkedListNode:
    """
    A class representing a node in a doubly linked list.

    Attributes:
    - key: The key of the node.
    - value: The value associated with the key.
    - prev: The previous node in the list.
    - next: The next node in the list.
    """

    def __init__(self, key=None, value=None):
        """
        Initializes a DoublyLinkedListNode with the given key and value.
        """
        self.key = key
        self.value = value
        self.prev = None
        self.next = None


class DoublyLinkedList:
    """
    A class representing a doubly linked list to manage the order of key-value pairs in the LRUCache.

    Attributes:
    - head: The first node in the list.
    - tail: The last node in the list.
    """

    def __init__(self):
        """
        Initializes an empty doubly linked list.
        """
        self.head = None
        self.tail = None

    def remove_node(self, node):
        """
        Removes the given node from the list.

        Parameters:
        - node: The node to be removed from the list.
        """
        if node.prev:
            node.prev.next = node.next
        if node.next:
            node.next.prev = node.prev
        if node == self.head:
            self.head = node.next
        if node == self.tail:
            self.tail = node.prev
        node.prev = None
        node.next = None

    def add_node_to_head(self, node):
        """
        Adds the given node to the head of the list.

        Parameters:
        - node: The node to be added at the head.
        """
        node.next = self.head
        node.prev = None
        if self.head:
            self.head.prev = node
        self.head = node
        if not self.tail:
            self.tail = node

    def move_node_to_head(self, node):
        """
        Moves the given node to the head of the list.

        Parameters:
        - node: The node to be moved to the head.
        """
        self.remove_node(node)
        self.add_node_to_head(node)

    def remove_tail_node(self):
        """
        Removes the tail node from the list and returns it.

        Returns:
        - The removed tail node.
        """
        if not self.tail:
            return None
        node = self.tail
        self.remove_node(node)
        return node


class LRUCache:
    """
    A class representing a Least Recently Used (LRU) Cache.

    Attributes:
    - cache: A dictionary storing the key-value pairs.
    - max_size: The maximum size of the cache.
    - current_size: The current size of the cache.
    - list_of_most_recent: A doubly linked list to track the order of the key-value pairs.
    """

    def __init__(self, max_size):
        """
        Initializes an LRUCache with a given maximum size.

        Parameters:
        - max_size: The maximum number of items that can be stored in the cache.
        """
        self.cache = {}
        self.max_size = max_size
        self.current_size = 0
        self.list_of_most_recent = DoublyLinkedList()

    def insert_key_value_pair(self, key, value):
        """
        Inserts or updates the key-value pair in the cache. If the cache is at capacity,
        the least recently used item is evicted.

        Parameters:
        - key: The key of the item to be inserted.
        - value: The value associated with the key.
        """
        if key in self.cache:
            self.replace_key(key, value)
            return

        self.current_size += 1
        if self.current_size > self.max_size:
            self.evict_least_recent()
            self.current_size -= 1
        
        node = DoublyLinkedListNode(key, value)
        self.cache[key] = node
        self.update_most_recent(node)


    def get_value_from_key(self, key):
        """
        Retrieves the value associated with the given key.

        Parameters:
        - key: The key to look for in the cache.

        Returns:
        - The value associated with the key, or None if the key is not found.
        """
        if key in self.cache:
            self.update_most_recent(self.cache[key])
            return self.cache[key].value
        else:
            return None

    def get_most_recent_key(self):
        """
        Retrieves the most recently used key.

        Returns:
        - The most recently used key.
        """
        return self.list_of_most_recent.head.key


    #HELPER FUNCTIONS ....
    def evict_least_recent(self):
        """
        Evicts the least recently used item from the cache.
        """
        key_to_remove = self.list_of_most_recent.tail.key
        self.list_of_most_recent.remove_tail_node()
        del self.cache[key_to_remove]

    def replace_key(self, key, value):
        """
        Replaces the value of the given key in the cache.

        Parameters:
        - key: The key to update.
        - value: The new value to associate with the key.
        """
        self.cache[key].value = value

    def update_most_recent(self, node):
        """
        Updates the given node to be the most recently used.

        Parameters:
        - node: The node to be moved to the head of the list.
        """
        self.list_of_most_recent.move_node_to_head(node)
