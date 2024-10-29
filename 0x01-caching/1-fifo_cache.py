#!/usr/bin/env python3
"""Defines a class that implements a FIFO cache"""

from base_caching import BaseCaching


class FIFOCache(BaseCaching):
    """When the memory is full, this cache removes
    the data that has stayed longest in memory: That
    is a First-in First-out algorithm."""
    
    def __init__(self):
        """Initialization function for every new object"""
        super().__init__()

    def put(self, key, item):
        """Inserts data into memory"""
        if key is not None and item is not None:
            if len(self.cache_data) == BaseCaching.MAX_ITEMS:
                # Remove an item to put another
                old = list(self.cache_data)[0]
                del self.cache_data[old]
                print("DISCARD: {}".format(old))
            self.cache_data[key] = item

    def get(self, key):
        """Retrieves data from cache memory"""
        if key is None or key not in self.cache_data:
            return None
        return self.cache_data.get(key)
