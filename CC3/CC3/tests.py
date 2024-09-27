import unittest
from solution import DoublyLinkedListNode, DoublyLinkedList, LRUCache


# Unit Tests
class TestLRUCache(unittest.TestCase):
    def test_basic_operations(self):
        cache = LRUCache(2)
        cache.insert_key_value_pair(1, 1)
        cache.insert_key_value_pair(2, 2)
        self.assertEqual(cache.get_value_from_key(1), 1)
        cache.insert_key_value_pair(3, 3)
        self.assertEqual(cache.get_value_from_key(2), None)
        cache.insert_key_value_pair(4, 4)
        self.assertEqual(cache.get_value_from_key(1), None)
        self.assertEqual(cache.get_value_from_key(3), 3)
        self.assertEqual(cache.get_value_from_key(4), 4)

    def test_basic_operations_2(self):
        lru_cache = LRUCache(3)
        lru_cache.insert_key_value_pair("b", 2)
        lru_cache.insert_key_value_pair("a", 1)
        lru_cache.insert_key_value_pair("c", 3)
        self.assertEqual(lru_cache.get_most_recent_key(), "c")
        self.assertEqual(lru_cache.get_value_from_key("a"), 1)
        self.assertEqual(lru_cache.get_most_recent_key(), "a")
        lru_cache.insert_key_value_pair("d", 4)
        self.assertEqual(lru_cache.get_value_from_key("b"), None)
        lru_cache.insert_key_value_pair("a", 5)
        self.assertEqual(lru_cache.get_value_from_key("a"), 5)

    def test_most_recent_key(self):
        cache = LRUCache(2)
        cache.insert_key_value_pair(1, 1)
        self.assertEqual(cache.get_most_recent_key(), 1)
        cache.insert_key_value_pair(2, 2)
        self.assertEqual(cache.get_most_recent_key(), 2)
        cache.get_value_from_key(1)
        self.assertEqual(cache.get_most_recent_key(), 1)

    def test_eviction(self):
        cache = LRUCache(1)
        cache.insert_key_value_pair(1, 1)
        cache.insert_key_value_pair(2, 2)
        self.assertEqual(cache.get_value_from_key(1), None)
        self.assertEqual(cache.get_value_from_key(2), 2)

    def test_update_value(self):
        cache = LRUCache(2)
        cache.insert_key_value_pair(1, 1)
        cache.insert_key_value_pair(1, 10)
        self.assertEqual(cache.get_value_from_key(1), 10)


if __name__ == '__main__':
    unittest.main()
