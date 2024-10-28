#!/usr/bin/env python3
"""
Deletion-resilient hypermedia pagination
"""

import csv
import math
from typing import List, Dict, Any


class Server:
    """Server class to paginate a database of popular baby names.
    """
    DATA_FILE = "Popular_Baby_Names.csv"

    def __init__(self):
        self.__dataset = None
        self.__indexed_dataset = None

    def dataset(self) -> List[List]:
        """Cached dataset
        """
        if self.__dataset is None:
            with open(self.DATA_FILE) as f:
                reader = csv.reader(f)
                dataset = [row for row in reader]
            self.__dataset = dataset[1:]

        return self.__dataset

    def indexed_dataset(self) -> Dict[int, List]:
        """Dataset indexed by sorting position, starting at 0
        """
        if self.__indexed_dataset is None:
            dataset = self.dataset()
            truncated_dataset = dataset[:1000]
            self.__indexed_dataset = {
                i: dataset[i] for i in range(len(dataset))
            }
        return self.__indexed_dataset

    def get_hyper_index(self, index: int = None, page_size: int = 10) -> Dict:
        """Return a hypermedia in a deletion-proof manner"""
        assert isinstance(index, int) and \
            index > 0 and index < len(self.__indexed_dataset)
        assert isinstance(page_size, int) and page_size > 0

        next_index: int = 0
        deleted: int = 0
        data: List[List] = []
        for position in range(index, page_size + index):
            if position in self.__indexed_dataset:
                data.append(self.__indexed_dataset.get(position))
            else:
                deleted += 1

        end_point: int = index + page_size
        if deleted == 0:
            next_index = index + page_size

        # Some deleted data was skipped, append more data
        while deleted != 0:
            if end_point in self.__indexed_dataset:
                data.append(self.__indexed_dataset.get(end_point))
                deleted -= 1
            else:
                end_point += 1
            if end_point > sorted(self.__indexed_dataset)[-1]:
                break

        if next_index == 0:
            next_index = end_point + 1

        hypermedia: Dict[str, Any] = {
                "index": index,
                "data": data,
                "page_size": page_size,
                "next_index": next_index
                }

        return hypermedia
