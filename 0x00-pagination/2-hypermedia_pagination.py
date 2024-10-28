#!/usr/bin/env python3
"""A server thats paginates data from a database for an api"""

import csv
import math
from typing import List, Dict, Any, Union


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

        low_index: int = (page - 1)*page_size
        high_index: int = page*page_size

        # Check if query is out of range
        try:
            if page == 1:
                return self.__dataset[:page_size]
            else:
                return self.__dataset[low_index:high_index]
        except IndexError:
            return []

    def get_hyper(self, page: int = 1, page_size: int = 10) -> Dict[str, Any]:
        """This method returns an hypermedia"""
        data: List[List] = self.get_page(page, page_size)
        next_page: Union[int, None] = \
            None if len(self.__dataset) <= page*page_size else page + 1
        prev_page: Union[int, None] = None if page == 1 else page - 1
        total_pages: int = len(self.__dataset) // page_size
        if len(self.__dataset) % page_size:
            total_pages += 1

        hypermedia: Dict[str, Any] = {
                "page_size": page_size,
                "page": page,
                "data": data,
                "next_page": next_page,
                "prev_page": prev_page,
                "total_pages": total_pages
                }
        return hypermedia
