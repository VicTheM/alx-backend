#!/usr/bin/env python3
"""Defines a class that implements a LFU cache"""

from base_caching import BaseCaching


class LFUCache(BaseCaching):
    """
    LFU -> Least Frequently Used

    This class implements a cache algorithm that evicts
    the most idle iem, that is the item that has lowest
    frequency of use. if two items have same use frequency,
    the one that was used most recently will be kept while
    the one that was used long ago will be deleted

    we will be using another dictionary to store how refuently
    an item is used.
    """

    def __init__(self):
        """Initialization function for every new object"""
        super().__init__()
        self.frequency = {}

    def put(self, key, item):
        """Inserts data into memory"""
        if key is not None and item is not None:
            old = None
            if len(self.cache_data) == BaseCaching.MAX_ITEMS:
                # Updating a key
                # When an already existing value is updated, it maintains
                # its position in time, therefore, it is not the most recently
                # used value
                if key in self.cache_data:
                    old = key
                else:
                    # LFU
                    # We could sort frequency by value for speed, but
                    # let us just leave it as O(n) time complexity
                    # Assign a relatively high value
                    lfu_freq = [100000000]
                    lfu_keys = [None]

                    for k, v in self.frequency.items():
                        if v < lfu_freq[0]:
                            lfu_freq[0] = v
                            lfu_keys[0] = k
                        elif v == lfu_freq[0]:
                            lfu_freq.append(v)
                            lfu_keys.append(v)

                    if len(lfu_freq) == 1:
                        old = lfu_keys[0]
                    else:
                        # LRU
                        for k in list(self.cache_data):
                            if k in lfu_keys:
                                old = k
                                break
                    print("DISCARD: {}".format(old))
                    del self.cache_data[old]
                    del self.frequency[old]
            self.cache_data[key] = item
            self.frequency[key] = self.frequency[key] + 1 if old == key else 1

    def get(self, key):
        """Retrieves data from cache memory"""
        if key is None or key not in self.cache_data:
            return None
        data = self.cache_data.get(key)

        # Re-write it so the use time can be updated
        del self.cache_data[key]
        self.cache_data[key] = data

        # Increase the frequency count
        self.frequency[key] += 1
        return data
