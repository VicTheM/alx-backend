#!/usr/bin/env python3
"""Defines a class that implements a LIFO cache"""

from base_caching import BaseCaching


class LIFOCache(BaseCaching):
    """When the memory is full, this cache removes
    the data that entered memory most recently: meaning
    oldest data persists over new comers, this is a LIFO
    algorithm."""
    
    def __init__(self):
        """Initialization function for every new object"""
        super().__init__()

    def put(self, key, item):
        """Inserts data into memory"""
        if key is not None and item is not None:
            if len(self.cache_data) == BaseCaching.MAX_ITEMS:
                # Remove an item to put another or update an item
                if key in self.cache_data:
                    old = key
                else:
                    old = list(self.cache_data)[-1]
                    print("DISCARD: {}".format(old))
                del self.cache_data[old]
            self.cache_data[key] = item

    def get(self, key):
        """Retrieves data from cache memory"""
        if key is None or key not in self.cache_data:
            return None
        return self.cache_data.get(key)
