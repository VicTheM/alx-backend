#!/usr/bin/env python3
"""Defines an api helper function"""

from typing import Tuple


def index_range(page: int = 0, page_size: int = 0) -> Tuple[int, int]:
    """This function receives a page and the requested size then
    returns the range of indexes that will be contained in the page

    Parameters:
        page: The requested full page
        page_size: the size of each page

    Returns: inde_range (the range of indexes that will be in the page
    """
    if page > 0 and page_size >= 0:
        if page == 1:
            return tuple((0, page_size))
        else:
            return tuple(((page - 1)*page_size, page*page_size))
