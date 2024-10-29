#!/usr/bin/env python3
"""Defines a class that implements a LIFO cache"""

from base_caching import BaseCaching


class MRUCache(BaseCaching):
    """
    MRU -> Most Recently Used

    This class implements a caching system that discards the
    most recently used item when the list is full. it can be
    used for scenarios where other items must be accessed after
    an item is used once before it can be used again

    we could use a list to track when an item is used. this will
    add one layer to the memory space and also there will be looking
    up or array when we want to make o choice on which to discard

    on the other hand, we can re-write an item when it is requested,
    this will update the last time it was used using inbuilt dictonary
    in python. the only downside is having to delete, and re-write every
    time an item is requested
    """

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
        # Update the last used time
        data = self.cache_data.get(key)
        del self.cache_data[key]
        self.cache_data[key] = data

        return data
