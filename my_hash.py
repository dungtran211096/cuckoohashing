# -*- coding: utf-8 -*-
"""This module contains the MyHash class."""

from numbers import Number
from random import randint
#TODO run linter/make sure style is fine
#TODO peer review (Rohan)?
#TODO choose better default value?
class MyHash(object):
    """Custom hash map which handles collisions using Cuckoo Hashing."""
    def __init__(self, size):
        """Initialize hash table of given size."""
        self._assert_valid_size(size)
        self.size = size
        self.nitems = 0
        self.array = [(None, None)] * int(size)

        self._num_hashes = 3
        self._max_path_size = 100
        self._random_nums = self._get_random_nums()

    #TODO: should be able to re set a value with same key
    def set(self, key, value):
        """Set key and value and return True on success, False on failure."""
        self._assert_valid_key(key)
        result = self._set_helper(key, value, 0)
        if result is False:
            # we couldn't find a free slot after maximum number of iterations
            self._rehash()
        return True

    def _set_helper(self, key, value, num_iters):
        if num_iters > self._max_path_size:
            return False
        else:
            array_indices = self._get_hashes(key)
            for i in array_indices:
                slot_key, slot_val = self.array[i]
                if slot_key is None or slot_key == key: # slot was not taken
                    self.array[i] = key, value
                    return True    
            # slot was taken, push out first slot
            (slot_key, slot_val), self.array[array_indices[0]] = self.array[arra_indices[0]], (key, value)
            self._set_helper(slot_key, slot_val, num_iters + 1)

    def _rehash(self):
        self.hashes = self._get_new_hashes()
        for key, value in array:
            if key is not None:
                self.set(key, value)

    def get(self, key):
        """
        Return value associated with input key if it has been set, None
        otherwise.
        """
        index = self._get_hash(key)
        if self._already_defined(index):
            return self.array[index]
        else: # no value was set for given key
            return None

    #TODO: maybe sacrifice conciseness for readability here?
    def delete(self, key):
        """
        Delete key from hash map and return the associated value on success,
        or None on failure.
        """
        index = self._get_hash(key)
        value, self.array[index] = self.array[index], None
        self.nitems = self.nitems - 1 if value is not None else self.nitems
        return value

    def load(self):
        """Return the current load of the hash map."""
        return float(self.nitems) / self.size

    def _already_defined(self, index):
        """Return True if hash map is already defined at given index, else False."""
        return self.array[index] is not None

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
        return [self._get_hash(string + str(i)) for i in self._random_nums]

    def _get_random_nums(self):
        return [randint(-1000, 1000) for _ in range(self._num_hashes)]
