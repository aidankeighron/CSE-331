"""
Project 3 - Hash Table Tests
CSE 331 SS24
"""

import random
import unittest

from solution import HashTable, HashNode, Connections

random.seed(331)


class TestProjectHashTable(unittest.TestCase):

    def test_hash(self):
        # (1) Basic with no double hashing
        table1 = HashTable(capacity=16)

        self.assertEqual(4, table1._hash("Ian"))
        self.assertEqual(2, table1._hash("Max"))
        self.assertEqual(5, table1._hash("Yash"))
        self.assertEqual(0, table1._hash("Brandon"))

        # (2) Basic with double hashing - Inserting Mode Only
        table2 = HashTable(capacity=16)

        table2.table = [None, None, None, None, HashNode("Ian", 150, True),
                        None, None, None, HashNode("H", 100),
                        None, None, None, None, None, None, None]

        self.assertEqual(9, table2._hash("Andrew", inserting=True))
        self.assertEqual(5, table2._hash("Andy", inserting=True))
        self.assertEqual(15, table2._hash("Lukas", inserting=True))

        # (3) Larger with Inserting and not Inserting
        table3 = HashTable(capacity=16)

        table3.table = [None, None, None,
                        HashNode('class_ever', 1), HashNode(None, None, True),
                        HashNode(None, None, True), None, None, None,
                        None, HashNode(None, None, True), None,
                        None, None, HashNode('cse331', 100), None]

        # (3)
        # Should insert in the first available bin
        self.assertEqual(4, table3._hash("is_the", inserting=True))

        # Should search until the first None/unused bin
        self.assertEqual(15, table3._hash("is_the"))

        # Should insert in the first available bin
        self.assertEqual(5, table3._hash("yash", inserting=True))

        # Should search until the first None/unused bin
        self.assertEqual(7, table3._hash("yash"))

        self.assertEqual(3, table3._hash("class_ever"))

        # (4) Large Comprehensive (featuring lovely 331 TAs of the past and present)
        keys = ["Max", "Ian", "Andrew", "H", "Andy", "Olivia", "Lukas", "Sean", "Angelo", "Jacob", "Zach", "Bank",
                "Onsay", "Anna", "Zosha", "Scott", "Brandon", "Yash", "Sarah"]
        vals = [i * 10 for i in range(19)]

        table4 = HashTable(capacity=16)

        table4.table = [None, None, HashNode('Max', 0),
                        None, HashNode('Ian', 10),
                        HashNode(None, None, True), None, None, None,
                        None, HashNode(None, None, True), None,
                        None, None, HashNode(None, None, True), None]

        expected = [2, 2, 4, 4, 9, 9, 8, 8, 8, 8, 0, 0, 8, 8, 7, 7, 6, 6, 15, 15, 3, 3, 15, 15, 14, 7, 9, 9, 1, 1, 9,
                    9, 0, 0, 5, 8, 15, 15]

        for i, key in enumerate(keys):
            # inserts every key in inserting mode and normal mode
            # (4)
            self.assertEqual(expected[2 * i], table4._hash(key, inserting=True))
            self.assertEqual(expected[2 * i + 1], table4._hash(key))

    def test_insert(self):
        # This test is just to make sure that the hidden method does the proper amount of work!
        # (1) Insert Sanity Check
        table = HashTable()

        solution = [None, None, None, None, HashNode('is_the', 3005), None, HashNode('cse331', 100), None]

        table._insert('cse331', 100)
        table._insert('is_the', 3005)

        # (1)
        self.assertEqual(solution, table.table)

        solution = [None, None, None, HashNode('class_ever', 1), HashNode('is_the', 3005), None, None, None, None,
                    None, HashNode('best', 42), None, None, None, HashNode('cse331', 100), None]

        # (2) Another insertion
        table._insert('best', 42)
        table._insert('class_ever', 1)

        # (2)
        self.assertEqual(4, table.size)
        self.assertEqual(16, table.capacity)
        self.assertEqual(solution, table.table)

        solution = [None, None, None, HashNode('class_ever', 3), HashNode('is_the', 3005), None, None, None, None,
                    None, HashNode('best', 45), None, None, None, HashNode('cse331', 100), None]

        # (3) inserting into already inserted before
        # Assert that inserted node's value is overwritten and the node is not replaced with a new node
        old_node = table._get('best')
        table._insert('best', 45)
        new_node = table._get('best')
        self.assertIs(old_node, new_node)

        old_node = table._get('class_ever')
        table._insert('class_ever', 3)
        new_node = table._get('class_ever')
        self.assertIs(old_node, new_node)

        # (3)
        self.assertEqual(4, table.size)
        self.assertEqual(16, table.capacity)
        self.assertEqual(solution, table.table)

        solution = [None, None, None, HashNode('class_ever', 3), HashNode('is_the', 3005), None, None, None, None,
                    None, HashNode('best', 41), None, None, None, HashNode('cse331', 100), None]

        # (4) inserting into deleted (not requiring delete to work)
        table.table[10].key = None  # type: ignore
        table.table[10].value = None  # type: ignore
        table.table[10].deleted = True  # type: ignore
        table.size -= 1
        table._insert('best', 41)
        table._insert('class_ever', 3)

        # (4)
        self.assertEqual(4, table.size)
        self.assertEqual(16, table.capacity)
        self.assertEqual(solution, table.table)

    def test_get(self):
        # This test is just to make sure that the hidden method does the proper amount of work!
        # (1) Get Sanity Check
        table = HashTable(capacity=8)

        solution = [None, None, None, None, HashNode('is_the', 3005), None, HashNode('cse331', 100), None]
        table.table = solution  # set the table so insert does not need to work
        table.size = 2

        # (1)
        self.assertEqual(HashNode("is_the", 3005), table._get('is_the'))
        self.assertEqual(HashNode("cse331", 100), table._get('cse331'))
        self.assertIsNone(table._get('cse320'))

        # (2) Check if _hash function checks for deleted
        table.table[-2].key = None  # type: ignore
        table.table[-2].value = None  # type: ignore
        table.table[-2].deleted = True  # type: ignore

        # (2)
        self.assertIsNone(table._get('cse331'))

    def test_delete(self):
        # This test is just to make sure that the hidden method does the proper amount of work!
        # (1) Delete Sanity Check
        table = HashTable(capacity=16)

        pre_solution = [None, None, None, HashNode('class_ever', 1), HashNode('is_the', 3005), None, None, None, None,
                        None, HashNode('best', 42), None, None, None, HashNode('cse331', 100), None]

        post_solution = [None, None, None, HashNode('class_ever', 1), HashNode(None, None, True), None, None, None,
                         None, None, HashNode(None, None, True), None, None, None, HashNode('cse331', 100), None]

        table.table = pre_solution  # set the table so insert does not need to work
        table.size = 4

        delete = ['best', 'is_the']
        for k in delete:
            table._delete(k)

        # (1)
        self.assertEqual(post_solution, table.table)
        self.assertEqual(2, table.size)

    def test_len(self):
        # (1) Empty
        table = HashTable()
        self.assertEqual(0, len(table))

        # (2) Size = 1
        table.size = 1
        self.assertEqual(1, len(table))

        # (3) Size = 5
        table.size = 5
        self.assertEqual(5, len(table))

    def test_grow(self):
        sol_keys = "Adventure Time Come on grab your friends " \
                   "We'll go to very distant lands With Jake the Dog and Finn a Human " \
                   "The fun will never end".split()
        sol_vals = [i * 100 for i in range(len(sol_keys))]

        # (1) Test grow
        table = HashTable()
        sizes = [i + 1 for i in range(len(sol_keys))]
        capacities = [8] * 3 + [16] * 4 + [32] * 8 + [64] * 11
        for i, key in enumerate(sol_keys):
            table[key] = sol_vals[i]
            self.assertEqual(sizes[i], table.size)  # 1a
            self.assertEqual(capacities[i], table.capacity)  # 1b

    def test_setitem(self):
        # (1) Simple (No Grow)
        table = HashTable()

        solution = [None, None, None, None, HashNode('is_the', 3005), None, HashNode('cse331', 100), None]

        table["cse331"] = 100
        table["is_the"] = 3005

        # (1)
        self.assertEqual(2, table.size)
        self.assertEqual(8, table.capacity)
        self.assertEqual(solution, table.table)

        # (2) Make sure same key gets updated, doesn't create a new node
        table["cse331"] = 200
        solution[6].value = 200

        # (2)
        self.assertEqual(2, table.size)
        self.assertEqual(8, table.capacity)
        self.assertEqual(solution, table.table)

        # (3) Simple (Grow, builds on 1, 2)
        solution = [None, None, None, HashNode('class_ever', 1), HashNode('is_the', 3005), None, None, None, None,
                    None, HashNode('best', 42), None, None, None, HashNode('cse331', 200), None]

        table['best'] = 42
        table['class_ever'] = 1

        # (3)
        self.assertEqual(4, table.size)
        self.assertEqual(16, table.capacity)
        self.assertEqual(solution, table.table)

        # (4) Large Comprehensive
        table2 = HashTable()

        keys = ["Max", "Ian", "Andrew", "H", "Andy", "Olivia", "Lukas", "Sean", "Angelo", "Jacob", "Zach", "Bank",
                "Onsay", "Anna", "Zosha", "Scott", "Brandon", "Yash", "Sarah"]
        vals = [i * 10 for i in range(19)]

        solution = [None, None, None, None, HashNode("Ian", 10), None, None, None, HashNode("H", 30),
                    HashNode("Andrew", 20), None, None, None, None, None, None, HashNode("Olivia", 50), None,
                    HashNode("Zach", 100), None, None, HashNode("Yash", 170), None, None, HashNode("Lukas", 60),
                    HashNode("Scott", 150), None, None, None, None, HashNode("Onsay", 120), None,
                    HashNode("Brandon", 160), HashNode("Zosha", 140), None, None, HashNode("Bank", 110), None, None,
                    None, None, None, None, None, None, None, None, HashNode("Sarah", 180), None, None,
                    HashNode("Anna", 130), None, None, None, HashNode("Angelo", 80), HashNode("Sean", 70),
                    HashNode("Andy", 40), None, None, None, None, HashNode("Max", 0), None, HashNode("Jacob", 90)]

        for i, key in enumerate(keys):
            table2[key] = vals[i]

        # (4)
        self.assertEqual(19, table2.size)
        self.assertEqual(64, table2.capacity)
        self.assertEqual(solution, table2.table)

    def test_getitem(self):
        # (1) Basic
        table = HashTable(capacity=8)

        solution = [None, None, None, None, HashNode('is_the', 3005), None, HashNode('cse331', 100), None]
        table.table = solution  # set the table so insert does not need to work
        table.size = 2

        # (1)
        self.assertEqual(3005, table["is_the"])
        self.assertEqual(100, table["cse331"])

        # (2) Slightly Larger
        solution = [None, None, None, HashNode('class_ever', 1), HashNode('is_the', 3005), None, None, None, None,
                    None, HashNode('best', 42), None, None, None, HashNode('cse331', 100), None]

        table.table = solution  # set the table so insert does not need to work
        table.capacity = 16
        table.size = 4

        # (2)
        self.assertEqual(3005, table["is_the"])
        self.assertEqual(100, table["cse331"])
        self.assertEqual(42, table["best"])
        self.assertEqual(1, table["class_ever"])

        # (3) Large Comprehensive
        table2 = HashTable(capacity=64)

        keys = ["Max", "Ian", "Andrew", "H", "Andy", "Olivia", "Lukas", "Sean", "Angelo", "Jacob", "Zach", "Bank",
                "Onsay", "Anna", "Zosha", "Scott", "Brandon", "Yash", "Sarah"]
        vals = [i * 10 for i in range(19)]

        solution = [None, None, None, None, HashNode("Ian", 10), None, None, None, HashNode("H", 30),
                    HashNode("Andrew", 20), None, None, None, None, None, None, HashNode("Olivia", 50), None,
                    HashNode("Zach", 100), None, None, HashNode("Yash", 170), None, None, HashNode("Lukas", 60),
                    HashNode("Scott", 150), None, None, None, None, HashNode("Onsay", 120), None,
                    HashNode("Brandon", 160), HashNode("Zosha", 140), None, None, HashNode("Bank", 110), None, None,
                    None, None, None, None, None, None, None, None, HashNode("Sarah", 180), None, None,
                    HashNode("Anna", 130), None, None, None, HashNode("Angelo", 80), HashNode("Sean", 70),
                    HashNode("Andy", 40), None, None, None, None, HashNode("Max", 0), None, HashNode("Jacob", 90)]

        table2.table = solution  # set the table so insert does not need to work
        table2.size = 19

        for i, key in enumerate(keys):
            self.assertEqual(vals[i], table2[key])  # (3)

        # (4) KeyError Check
        with self.assertRaises(KeyError):
            abc = table2["Enbody"]

    def test_delitem(self):
        # (1) Basic
        table = HashTable(capacity=16)

        pre_solution = [None, None, None, HashNode('class_ever', 1), HashNode('is_the', 3005), None, None, None, None,
                        None, HashNode('best', 42), None, None, None, HashNode('cse331', 100), None]

        post_solution = [None, None, None, HashNode('class_ever', 1), HashNode(None, None, True), None, None, None,
                         None, None, HashNode(None, None, True), None, None, None, HashNode('cse331', 100), None]

        table.table = pre_solution  # set the table so insert does not need to work
        table.size = 4

        delete = ['best', 'is_the']
        for k in delete:
            del table[k]

        # (1)
        self.assertEqual(post_solution, table.table)
        self.assertEqual(2, table.size)

        # (2) Large Comprehensive
        table2 = HashTable(capacity=64)

        keys = ["Max", "Ian", "Andrew", "H", "Andy", "Olivia", "Lukas", "Sean", "Angelo", "Jacob", "Zach", "Bank",
                "Onsay", "Anna", "Zosha", "Scott", "Brandon", "Yash", "Sarah"]
        vals = [i * 10 for i in range(19)]

        pre_solution = [None, None, None, None, HashNode("Ian", 10), None, None, None, HashNode("H", 30),
                        HashNode("Andrew", 20), None, None, None, None, None, None, HashNode("Olivia", 50), None,
                        HashNode("Zach", 100), None, None, HashNode("Yash", 170), None, None, HashNode("Lukas", 60),
                        HashNode("Scott", 150), None, None, None, None, HashNode("Onsay", 120), None,
                        HashNode("Brandon", 160), HashNode("Zosha", 140), None, None, HashNode("Bank", 110), None, None,
                        None, None, None, None, None, None, None, None, HashNode("Sarah", 180), None, None,
                        HashNode("Anna", 130), None, None, None, HashNode("Angelo", 80), HashNode("Sean", 70),
                        HashNode("Andy", 40), None, None, None, None, HashNode("Max", 0), None, HashNode("Jacob", 90)]

        solution = [None, None, None, None, HashNode(None, None), None, None, None, HashNode(None, None),
                    HashNode(None, None), None, None, None, None, None, None, HashNode(None, None), None,
                    HashNode("Zach", 100), None, None, HashNode("Yash", 170), None, None, HashNode(None, None),
                    HashNode("Scott", 150), None, None, None, None, HashNode("Onsay", 120), None,
                    HashNode("Brandon", 160), HashNode("Zosha", 140), None, None, HashNode("Bank", 110), None, None,
                    None, None, None, None, None, None, None, None, HashNode("Sarah", 180), None, None,
                    HashNode("Anna", 130), None, None, None, HashNode(None, None), HashNode(None, None),
                    HashNode(None, None), None, None, None, None, HashNode(None, None), None, HashNode(None, None)]

        table2.table = pre_solution  # set the table so insert does not need to work
        table2.size = 19

        for i, key in enumerate(keys):
            if i < 10:
                del table2[key]

        # (2)
        self.assertEqual(solution, table2.table)
        self.assertEqual(9, table2.size)

        # (3) KeyError Check
        with self.assertRaises(KeyError):
            del table2["Enbody"]
        self.assertEqual(9, table2.size)

    def test_contains(self):
        # (1) Not in Table
        table = HashTable()
        self.assertEqual(False, 'key' in table)

        # (2) In Table
        table.table[5] = HashNode('key', 331)

        self.assertEqual(True, 'key' in table)
        self.assertEqual(False, 'new_key' in table)

    def test_update(self):
        # (1) Not in Table Already
        table = HashTable()

        table.update([("minecraft", 10), ("ghast", 15)])
        self.assertEqual(10, table["minecraft"])
        self.assertEqual(15, table["ghast"])
        self.assertEqual(2, table.size)

        # (2) Update Values in Table
        table.update([("minecraft", 31), ("ghast", 42)])
        self.assertEqual(31, table["minecraft"])
        self.assertEqual(42, table["ghast"])
        self.assertEqual(2, table.size)

        # (3) Update Values in Table and Add New Values
        table.update([("minecraft", 50), ("enderman", 12)])
        self.assertEqual(50, table["minecraft"])
        self.assertEqual(12, table["enderman"])
        self.assertEqual(42, table["ghast"])
        self.assertEqual(3, table.size)

        # (4) Do Nothing
        table.update()
        self.assertEqual(50, table["minecraft"])
        self.assertEqual(12, table["enderman"])
        self.assertEqual(42, table["ghast"])
        self.assertEqual(3, table.size)

    def test_keys_values_items(self):
        # (1) Basic
        table = HashTable()

        initial_keys = ['one', 'two', 'three']
        initial_values = [1, 2, 31]
        initial_items = [('one', 1), ('two', 2), ('three', 31)]

        for i in range(3):
            table[initial_keys[i]] = initial_values[i]

        keys = table.keys()
        values = table.values()
        items = table.items()

        # (1)
        self.assertEqual(set(initial_keys), set(keys))
        self.assertEqual(set(initial_values), set(values))
        self.assertEqual(set(initial_items), set(items))

        # (2) Large
        table2 = HashTable()
        initial_keys = ["Max", "Ian", "Andrew", "H", "Andy", "Olivia", "Lukas", "Sean", "Angelo", "Jacob", "Zach",
                        "Bank", "Onsay", "Anna", "Zosha", "Scott", "Brandon", "Yash", "Sarah"]
        initial_values = [i * 10 for i in range(19)]
        initial_items = []

        for i, key in enumerate(initial_keys):
            table2[key] = initial_values[i]
            initial_items.append((key, initial_values[i]))

        keys = table2.keys()
        values = table2.values()
        items = table2.items()

        # (2)
        self.assertEqual(set(initial_keys), set(keys))
        self.assertEqual(set(initial_values), set(values))
        self.assertEqual(set(initial_items), set(items))

        # (3) Make sure deleted nodes aren't included
        table3 = HashTable()
        initial_keys = ["CSE", "331", "is", "super", "fun"]
        initial_values = [1, 2, 3, 4, 5]
        initial_items = []

        for i, key in enumerate(initial_keys):
            table3[key] = initial_values[i]
            initial_items.append((key, initial_values[i]))

        keys = table3.keys()
        values = table3.values()
        items = table3.items()

        # (3)
        self.assertEqual(set(initial_keys), set(keys))
        self.assertEqual(set(initial_values), set(values))
        self.assertEqual(set(initial_items), set(items))

        del table3["fun"]
        del table3["super"]
        for _ in range(2):
            initial_keys.pop()
            initial_values.pop()
            initial_items.pop()

        keys = table3.keys()
        values = table3.values()
        items = table3.items()

        # (3)
        self.assertEqual(set(initial_keys), set(keys))
        self.assertEqual(set(initial_values), set(values))
        self.assertEqual(set(initial_items), set(items))

    def test_clear(self):
        # (1) Table with contents
        table = HashTable()

        table['table'] = 1
        table['will'] = 2
        table['be'] = 3
        table['cleared'] = 4

        self.assertEqual(4, table.size)

        table.clear()

        self.assertEqual(0, table.size)
        for node in table.table:
            self.assertIsNone(node)

        # (2) Empty Table
        table.clear()

        self.assertEqual(0, table.size)
        for node in table.table:
            self.assertIsNone(node)

        # (3) Reused Table
        table['one'] = 1

        table.clear()

        self.assertEqual(0, table.size)
        for node in table.table:
            self.assertIsNone(node)

    def test_setitem_and_delitem(self):
        # (1) Delete, then insert again (from basic delitem)
        table = HashTable(capacity=16)

        pre_solution = [None, None, None, HashNode('class_ever', 1), HashNode('is_the', 3005), None, None, None, None,
                        None, HashNode('best', 42), None, None, None, HashNode('cse331', 100), None]

        table.table = pre_solution
        table.size = 4

        delete = ['best', 'is_the']
        for k in delete:
            del table[k]

        table['best'] = 42
        table['is_the'] = 3005

        # (1)
        self.assertEqual(pre_solution, table.table)
        self.assertEqual(4, table.size)

        # (2) Populate, delete all (using clear), then repopulate,
        # then delete again (using delitem), then repopulate again, check if table is the same as original populate
        table = HashTable(capacity=64)
        for i in range(10):
            table[str(i)] = i

        pre_solution = table.table
        table.clear()

        for i in range(10):
            table[str(i)] = i

        # (2)a Using clear
        self.assertEqual(pre_solution, table.table)
        self.assertEqual(10, table.size)

        for i in range(10):
            del table[str(i)]

        for i in range(10):
            table[str(i)] = i

        # (2)b Using del
        self.assertEqual(pre_solution, table.table)
        self.assertEqual(10, table.size)

    def test_comprehensive(self):
        table = HashTable()

        sol_keys = "Adventure Time Come on grab your friends " \
                   "We'll go to very distant lands With Jake the Dog and Finn a Human " \
                   "The fun will never end".split()
        sol_vals = [i * 100 for i in range(len(sol_keys))]

        solution_a = [None, HashNode('the', 1500), HashNode('go', 800), HashNode('and', 1700), None,
                      None, HashNode('Dog', 1600), HashNode('your', 500), None, None,
                      HashNode('Come', 200), None, None, None, HashNode('very', 1000), None,
                      HashNode('never', 2400), None, None, None, HashNode('grab', 400), None, None,
                      None, None, None, None, HashNode('Time', 100), None, HashNode('fun', 2200),
                      None, None, None, HashNode('a', 1900), None, HashNode('Finn', 1800), None,
                      None, None, HashNode('Jake', 1400), None, HashNode('on', 300), None,
                      HashNode('distant', 1100), HashNode('Human', 2000), None, None,
                      HashNode('friends', 600), HashNode('The', 2100), None,
                      HashNode('Adventure', 0), HashNode('to', 900), HashNode('will', 2300), None,
                      None, None, HashNode('With', 1300), None, None, None, HashNode('end', 2500),
                      None, HashNode('lands', 1200), HashNode('We\'ll', 700)]

        solution_b = [None, HashNode('the', 1500), HashNode(None, None), HashNode('and', 1700),
                      None, None, HashNode('Dog', 1600), HashNode(None, None), None, None,
                      HashNode(None, None), None, None, None, HashNode('very', 1000), None,
                      HashNode('never', 2400), None, None, None, HashNode(None, None), None, None,
                      None, None, None, None, HashNode(None, None), None, HashNode('fun', 2200),
                      None, None, None, HashNode('a', 1900), None, HashNode('Finn', 1800), None,
                      None, None, HashNode('Jake', 1400), None, HashNode(None, None), None,
                      HashNode('distant', 1100), HashNode('Human', 2000), None, None,
                      HashNode(None, None), HashNode('The', 2100), None, HashNode(None, None),
                      HashNode(None, None), HashNode('will', 2300), None, None, None,
                      HashNode('With', 1300), None, None, None, HashNode('end', 2500), None,
                      HashNode('lands', 1200), HashNode(None, None)]

        solution_c = [None, HashNode('the', 1500), HashNode('go', 800), HashNode('and', 1700), None,
                      None, HashNode('Dog', 1600), HashNode('your', 500), None, None,
                      HashNode('Come', 200), None, None, None, HashNode('very', 1000), None,
                      HashNode('never', 2400), None, None, None, HashNode('grab', 400), None, None,
                      None, None, None, None, HashNode('Time', 100), None, HashNode('fun', 2200),
                      None, None, None, HashNode('a', 1900), None, HashNode('Finn', 1337), None,
                      None, None, HashNode('Jake', 100), None, HashNode('on', 300), None,
                      HashNode('distant', 1100), HashNode('Human', 2000), None, None,
                      HashNode('friends', 600), HashNode('The', 2100), None,
                      HashNode('Adventure', 0), HashNode('to', 900), HashNode('will', 2300), None,
                      None, None, HashNode('With', 1300), None, None, None, HashNode('end', 2500),
                      None, HashNode('lands', 1200), HashNode("We'll", 700)]

        # (1) Insertions/Grow
        sizes = [i + 1 for i in range(len(sol_keys))]
        capacities = [8] * 3 + [16] * 4 + [32] * 8 + [64] * 11
        for i, key in enumerate(sol_keys):
            table[key] = sol_vals[i]
            self.assertEqual(sizes[i], table.size)  # 1a
            self.assertEqual(capacities[i], table.capacity)  # 1b

        self.assertEqual(solution_a, table.table)  # 1c

        # (2) Get
        for i, key in enumerate(sol_keys):
            self.assertEqual(sol_vals[i], table[key])  # 2a

        with self.assertRaises(KeyError):
            _ = table["Owen"]  # 2b

        # (3) Delete
        for i, key in enumerate(sol_keys):
            if i < 10:
                del table[key]

        self.assertEqual(solution_b, table.table)  # 3a
        self.assertEqual(16, table.size)  # 3b

        with self.assertRaises(KeyError):
            del table["Owen"]  # 3c
        self.assertEqual(16, table.size)  # 3d

        # (4) Clear
        table.clear()

        self.assertEqual(0, table.size)  # 4a
        for node in table.table:
            self.assertEqual(None, node)  # 4b

        table = HashTable()
        for i, key in enumerate(sol_keys):
            table[key] = sol_vals[i]

        # (5) Keys/Vals/Items
        keys = table.keys()
        values = table.values()
        items = table.items()

        self.assertIsInstance(keys, list)  # 5a
        self.assertIsInstance(values, list)  # 5b
        self.assertIsInstance(items, list)  # 5c

        # (6) Contains
        for i, key in enumerate(sol_keys):
            self.assertEqual(True, key in table)  # 6a
        self.assertEqual(False, "Ofria" in table)  # 6b

        # (7) Update
        table.update([("Finn", 1337), ("Jake", 100)])
        self.assertEqual(solution_c, table.table)

        # (8) Delete and Contains
        for i, key in enumerate(sol_keys):
            del table[key]
            self.assertEqual(False, key in table)  # 8a

        # (9) Insert and delete with conflicts
        table = HashTable()
        table["Brandon"] = 1
        # _hash_1 conflicts, must search multiple spots
        table["Lukas"] = 1

        del table["Brandon"]

        # (10) Insert where key already exists, but must search past deleted entry
        table["Lukas"] = 2
        # Delete should work if insert went into right spot
        # If _hash was only called once with inserting=True instead
        # of searching with inserting=False first, this will probably cause problems
        del table["Lukas"]


class TestConnections(unittest.TestCase):

    def test_add_contact(self):
        connections = Connections()
        connections.add_connection("Isaac Newton", "Leonardo da Vinci")
        connections.add_connection("Isaac Newton", "Michelangelo")

        self.assertEqual(connections.contacts["Isaac Newton"], ["Leonardo da Vinci", "Michelangelo"])
        self.assertTrue("Michelangelo" not in connections.contacts)
        self.assertTrue("Leonardo da Vinci" not in connections.contacts)

        connections.add_connection("Leonardo da Vinci", "Isaac Newton")
        self.assertEqual(connections.contacts["Leonardo da Vinci"], ["Isaac Newton"])

        connections.add_connection("Leonardo da Vinci", "Leonardo da Vinci")
        self.assertEqual(connections.contacts["Leonardo da Vinci"], ["Isaac Newton"])

        expected = ['Fibonacci']
        connections.add_connection('Pascal', 'Fibonacci')
        n0 = 0
        n1 = 1
        for i in range(100):
            connections.add_connection('Pascal', 'Fibonacci' + str(n0 + n1))
            expected.append('Fibonacci' + str(n0 + n1))
            temp = n1
            n1 = n1 + n0
            n0 = temp
            self.assertEqual(connections.contacts['Pascal'], expected)

   

    def test_simple_connections(self):
        connections = Connections()
        connections.add_connection("Isaac Newton", "Leonardo da Vinci")
        connections.add_connection("Isaac Newton", "Michelangelo")
        connections.add_connection("Leonardo da Vinci", "Galileo Galilei")
        connections.add_connection("Galileo Galilei", "Johannes Kepler")
        connections.add_connection("Johannes Kepler", "Nicolaus Copernicus")
        # Direct connection
        self.assertTrue(connections.check_if_related("Isaac Newton", "Leonardo da Vinci", 1))
        # No direct connection with limit 1
        self.assertFalse(connections.check_if_related("Isaac Newton", "Galileo Galilei", 1))
        # Same person
        self.assertTrue(connections.check_if_related("Isaac Newton", "Isaac Newton", 0))
        # No connection
        self.assertFalse(connections.check_if_related("Isaac Newton", "Pythagoras", 2))

    def test_complex_connections(self):
        connections = Connections()
        connections.add_connection("Isaac Newton", "Leonardo da Vinci")
        connections.add_connection("Isaac Newton", "Michelangelo")
        connections.add_connection('Isaac Newton', 'Gottfried Leibniz')
        connections.add_connection("Leonardo da Vinci", "Galileo Galilei")
        connections.add_connection("Leonardo da Vinci", "Johannes Kepler")
        connections.add_connection("Galileo Galilei", "Isaac Newton")
        connections.add_connection("Galileo Galilei", "Johannes Kepler")
        connections.add_connection("Johannes Kepler", "Nicolaus Copernicus")
        connections.add_connection("Johannes Kepler", "Leonardo da Vinci")
        connections.add_connection("Johannes Kepler", "Isaac Newton")
        connections.add_connection("Johannes Kepler", "Galileo Galilei")
        connections.add_connection('Johannes Kepler', 'Joseph Lagrange')
        connections.add_connection('Joseph Lagrange', 'Pierre Laplace')
        connections.add_connection('Joseph Lagrange', 'James Bernoulli')
        # Indirect connection within 4 steps
        self.assertTrue(connections.check_if_related("Isaac Newton", "Pierre Laplace", 4))
        self.assertFalse(connections.check_if_related('Isaac Newton', 'Pierre Laplace', 3))

        # Indirect connection within 3 steps
        self.assertTrue(connections.check_if_related("Isaac Newton", "Nicolaus Copernicus", 3))
        self.assertFalse(connections.check_if_related("Isaac Newton", "Nicolaus Copernicus", 2))

        connections = Connections()
        for i in range(2, 50):
            connections.add_connection(str(i), str(i + 1))
            connections.add_connection(str(i), str(i + 2))
            self.assertTrue(connections.check_if_related('2', str(i+1), int(i/2)))
            self.assertTrue(connections.check_if_related('2', str(i+2), int(i/1.5)))

    # def test_cyclic_connections(self):
    #     connections = Connections()
    #     # Cyclic connections with no end
    #     connections.add_connection("Benoit Mandelbrot", "Gottfried Leibniz")
    #     connections.add_connection('Gottfried Leibniz', 'Karl Weierstrass')
    #     connections.add_connection('Karl Weierstrass', 'Benoit Mandelbrot')
    #     self.assertFalse(connections.check_if_related('Benoit Mandelbrot', 'Georg Cantor', float('inf')))
   

if __name__ == '__main__':
    unittest.main()