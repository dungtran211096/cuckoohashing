# -*- coding: utf-8 -*-
"""This module contains the MyHash class."""

from numbers import Number
from random import randint
#TODO run linter/make sure style is fine
#TODO peer review (Rohan)?
#TODO choose better default value? (or make it variable)
class MyHash(object):
    """Custom hash map which handles collisions using Cuckoo Hashing."""
    def __init__(self, size):
        """Initialize hash table of given size."""
        self._assert_valid_size(size)
        self.size = size
        self.nitems = 0
        self.array = [(None, None)] * int(size)

        self._num_hashes = 8
        self._max_path_size = size
        self._random_nums = self._get_new_random_nums()

    def set(self, key, value):
        """Set key and value and return True on success, False on failure."""
        self._assert_valid_key(key)
        result = self._set_helper(key, value, 0)
        if result is not True:
            # we couldn't find a free slot after maximum number of iterations
            self._rehash(*result)
        self.nitems += 1
        return True

    def _set_helper(self, key, value, num_iters):
        """
        Recursively try to set key to value in the dictionary using cuckoo
        hashing to resolve conflicts, and return True on success and the 
        unset key and value on failure.
        """
        if num_iters > self._max_path_size:
            return key, value
        else:
            array_indices = self._get_hashes(key)
            for i in array_indices:
                slot_key, slot_val = self.array[i]
                if slot_key is None or slot_key == key: # slot was not taken
                    self.array[i] = key, value
                    return True    
            # slot was taken, push out first slot
            (slot_key, slot_val), self.array[array_indices[0]] = \
                                    self.array[array_indices[0]], (key, value)
            return self._set_helper(slot_key, slot_val, num_iters + 1)

    def _rehash(self, unset_key, unset_value):
        """
        Generate new hash functions and try to rehash all values. Keeps on
        generating new hashes until a working set is found.
        """
        self._random_nums = self._get_new_random_nums()
        result = self._set_helper(unset_key, unset_value, 0)
        if result is not True:
            self._rehash(*result)
        for index, (key, value) in enumerate(self.array):
            if key is not None and index not in self._get_hashes(key):
                self.array[index] = (None, None)
                result = self._set_helper(key, value, 0)
                if result is not True:
                    self._rehash(*result)

    def get(self, key):
        """
        Return value associated with input key if it has been set, None
        otherwise.
        """
        array_index = self._find_pair(key)
        if array_index == "not found":
            return None
        else:
            return self.array[array_index][1]

    #TODO: maybe sacrifice conciseness for readability here?
    def delete(self, key):
        """
        Delete key from hash map and return the associated value on success,
        or None on failure.
        """
        array_index = self._find_pair(key)
        if array_index == "not found":
            return None
        else:
            self.nitems -= 1
            (key, val), self.array[array_index] = \
                                        self.array[array_index], (None, None)
            return val

    def _find_pair(self, key):
        """Return the index of key in the array or "not found" if not found."""
        indices = self._get_hashes(key)
        for i in indices:
            slot_key, slot_val = self.array[i]
            if slot_key == key:
                return i
        return "not found"

    def load(self):
        """Return the current load of the hash map."""
        return float(self.nitems) / self.size

    @classmethod
    def _assert_valid_key(cls, key):
        """Raise TypeError if the input is not a valid key."""
        if not isinstance(key, str):
            raise TypeError("Keys must be strings.")

    def _assert_valid_size(self, size):
        """Raise appropriate error if input is not a natural number."""
        if not isinstance(size, Number):
            raise TypeError("Size must be a valid integer")
        elif size < 0 or int(size) != size:
            raise ValueError("Size must be non negative")

    def _get_hash(self, string):
        """Return the hash of the input string."""
        return hash(string) % self.size

    def _is_full(self):
        """Return True if the hash map is full, False otherwise."""
        return self.nitems == self.size

    #TODO: better hash function?
    def _get_hashes(self, string):
        """Return a list of each hash applied to the input string."""
        return [self._get_hash(string + str(i)) for i in self._random_nums]

    def _get_new_random_nums(self):
        """Generate new random numbers to be used in the hash functions."""
        return [randint(-1000, 1000) for _ in range(self._num_hashes)]