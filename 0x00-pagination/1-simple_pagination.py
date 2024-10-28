#!/usr/bin/env python3
"""A server thats paginates data from a database for an api"""

import csv
import math
from typing import List


class Server:
    """Server class to paginate a database of popular baby names.
    """
    DATA_FILE = "Popular_Baby_Names.csv"

    def __init__(self):
        self.__dataset = None

    def dataset(self) -> List[List]:
        """Cached dataset
        """
        if self.__dataset is None:
            with open(self.DATA_FILE) as f:
                reader = csv.reader(f)
                dataset = [row for row in reader]
            self.__dataset = dataset[1:]

        return self.__dataset

    def get_page(self, page: int = 1, page_size: int = 10) -> List[List]:
        """This function receives a page and the requested size then
        returns the range of indexes that will be contained in the page

        Parameters:
            page: The requested full page
            page_size: the size of each page

        Returns: inde_range (the range of indexes that will be in the page
        """
        assert isinstance(page, int) and page > 0
        assert isinstance(page_size, int) and page_size > 0
        self.dataset()

        # Check if query is out of range
        try:
            if page == 1:
                return self.__dataset[:page_size]
            else:
                return self.__dataset[(page - 1)*page_size:page*page_size]
        except IndexError:
            return []
