import heapq
from collections import defaultdict


class OrderedSet:

    __slots__ = ["n_added_items", "n_current_items", "order_to_data", "data"]

    def __init__(self, data=None):
        self.n_added_items = 0
        self.n_current_items = 0
        self.data = defaultdict(int)
        self.order_to_data = dict()
        if data is not None:
            [self.add(d) for d in data]

    def add(self, item):
        self.data[item] += 1
        self.order_to_data[self.n_added_items] = item
        self.n_added_items += 1
        self.n_current_items += 1

    def _remove_n(self, n):
        item = self.order_to_data[n]
        self.data[item] -= 1
        if not self.data[item]:
            del self.data[item]
        del self.order_to_data[n]
        self.n_current_items -= 1

    def remove_first(self):
        self._remove_n(self._min_n())

    def remove_last(self):
        self._remove_n(self._max_n())

    def _min_n(self):
        return min(self.order_to_data.keys())

    def _max_n(self):
        return max(self.order_to_data.keys())

    def first(self):
        return self.order_to_data[self._min_n()]

    def last(self):
        return self.order_to_data[self._max_n()]

    def nth_item(self, n):
        if n == 0:
            return self.first()
        elif n == -1:
            return self.last()
        else:
            orders = self.order_to_data.keys()
            if n > 0:
                return self.order_to_data[heapq.nsmallest(n + 1, orders)[-1]]
            else:
                return self.order_to_data[heapq.nlargest(-n, orders)[-1]]

    def __contains__(self, item):
        return item in self.data.keys()

    def __len__(self):
        return self.n_current_items

    def get(self):
        return [x[1] for x in sorted(self.order_to_data.items(), key=lambda y: y[0])]

    def __str__(self):
        return str(self.get())

    def __copy__(self):
        new = OrderedSet()
        new.data = self.data.copy()
        new.order_to_data = self.order_to_data.copy()
        new.n_current_items = self.n_current_items
        new.n_added_items = self.n_added_items
        return new

    def copy(self):
        return self.__copy__()

    def n_unique_items(self):
        return len(self.data)
