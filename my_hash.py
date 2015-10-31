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
        return self._set(key, value, increment_nitems=True)

    def _set(self, key, value, increment_nitems):
        """Add key value pair and return True on success, False on failure."""
        self._assert_valid_key(key)
        set_result = self._set_helper(key, value, 0)
        if set_result is not True:
            # the set did not succeed, so we rehash the table with new hashes
            self._rehash(*set_result)
        self.nitems += 1
        return True

    def _set_helper(self, key, value, num_iters):
        """
        Recursively try to add key value pair to dictionary in under
        _max_path_size number of steps, and return True on success and the 
        unset key and value on failure.
        """
        if num_iters > self._max_path_size:
            return key, value
        else:
            array_indices = self._get_hashes(key)
            if self._add_to_free_slot(key, value, array_indices) == "success":
                return True
            else: 
                # set the array at the first hash of the key to key value pair
                # and recursively re set the pair that was bumped out
                (slot_key, slot_val), self.array[array_indices[0]] = \
                                        self.array[array_indices[0]], (key, value)
                return self._set_helper(slot_key, slot_val, num_iters + 1)

    def _add_to_free_slot(self, key, value, array_indices):
        """Attempt to add key value without moving any previous pairs."""
        for i in array_indices:
            slot_key, slot_val = self.array[i]
            # Check if slot is empty or if given key has already been set
            # to allow overwriting of keys
            if slot_key is None or slot_key == key:
                self.array[i] = key, value
                return "success"  
        return "failure"  

    def _rehash(self, unset_key, unset_value):
        """
        Take a key value pair not yet in the dictionary and generate new 
        hash functions until all key value pairs including the input can be
        added to the table without collisions.
        """
        self._random_nums = self._get_new_random_nums()
        self._set(unset_key, unset_value, increment_nitems=False)
        for index, (key, value) in enumerate(self.array):
            if key is not None and index not in self._get_hashes(key):
                self.array[index] = (None, None)
                self._set(key, value, increment_nitems=False)

    def get(self, key):
        """
        Return value associated with input key if it has been set, None
        otherwise.
        """
        array_index = self._find_array_index(key)
        return None if array_index == "not found" else self.array[array_index][1]

    def delete(self, key):
        """
        Delete key from hash map and return the associated value on success,
        and None on failure.
        """
        array_index = self._find_array_index(key)
        if array_index == "not found":
            return None
        else:
            self.nitems -= 1
            (_, val), self.array[array_index] = \
                                        self.array[array_index], (None, None)
            return val

    def _find_array_index(self, key):
        """Return the index of key in the array or "not found" if not found."""
        indices = self._get_hashes(key)
        matches = filter(lambda i: self.array[i][0] == key, indices)
        return matches[0] if matches else "not found"

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