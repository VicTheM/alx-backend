#!/usr/bin/env python3
"""This file models a simple basix cache"""

from base_caching import BaseCaching


class BasicCache(BaseCaching):
    """A class that implements a basic caching system"""
    def __init__(self):
        """Initialization function"""
        super().__init__()

    def put(self, key, item):
        """Insert data into memory"""
        if key is not None and item is not None:
            self.cache_data[key] = item

    def get(self, key):
        """get a value from cache data"""
        if key is None or key not in self.cache_data:
            return None
        return self.cache_data.get(key)
