#!/usr/bin/env python3
"""Defines a class that implements a LRU cache"""

from base_caching import BaseCaching


class LRUCache(BaseCaching):
    """
    LRU -> Least Reently Used
    This class implements a cache algorithm that evicts
    the item that has the greatest time since it was last
    used. we may say it considers this data relatively
    obsolete

    I will be using annother array of same size as the max
    number of items that may be in memory to track their use
    time. This will result in a space complexity of O(n), bad?

    Another implenmentation is to delete and re-write each data
    as they are used, so they will be considered most recently
    used. this will be slower because or read and write is performed
    every time an item is queried. I will ise this anyway
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
                    old = list(self.cache_data)[0]
                    print("DISCARD: {}".format(old))
                del self.cache_data[old]
            self.cache_data[key] = item

    def get(self, key):
        """Retrieves data from cache memory"""
        if key is None or key not in self.cache_data:
            return None
        data = self.cache_data.get(key)
        
        # Re-write it so the use time can be updated
        del self.cache_data[key]
        self.cache_data[key] = data
        return data
