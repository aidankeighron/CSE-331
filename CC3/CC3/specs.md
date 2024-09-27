## LRU Cache

### Problem Statement

Implement a class `LRUCache` for a Least Recently Used (LRU) cache. The class should support the following methods:

- `insert_key_value_pair(key, value)`: Inserts a key-value pair into the cache.
- `get_value_from_key(key)`: Retrieves the value associated with the provided key.
- `get_most_recent_key()`: Retrieves the most recently used key (either recently inserted or retrieved).

All these methods should run in **O(1)** time complexity.

Additionally, the `LRUCache` class should have a `max_size` attribute, which represents the maximum number of key-value pairs the cache can hold. This value should be passed as an argument when creating an instance of the cache.

When inserting a new key-value pair and the cache has reached its capacity, the least recently used key-value pair should be evicted. Note that if the key already exists, its value should be updated, and this should not trigger an eviction.

If a key that does not exist is queried using `get_value_from_key`, the method should return `None`.

### Method Details

1. **`insert_key_value_pair(key, value)`**:
   - Inserts or updates the given key-value pair in the cache.
   - If the cache is at maximum capacity, it evicts the least recently used key-value pair.

2. **`get_value_from_key(key)`**:
   - Returns the value associated with the given key, or `None` if the key does not exist.

3. **`get_most_recent_key()`**:
   - Returns the most recently used key in the cache.

### Constraints

- The cache should handle keys and values of any data type.
- All operations should have a **O(1)** time complexity.
