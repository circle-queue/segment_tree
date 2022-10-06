from typing import Union
from operator import add

class SegmentTree:
    '''
    Example use:
        t = SegmentTree([6, 3, -1, 1, 3], operator=add) # O(n)
        t[0] -= 3 # O(log(n))
        t[3] = 11 # O(log(n))
        assert t[:4] == 16 # prints the sum of the first 4 elements O(log(n))
        BROKEN: t[3:5] -= 3 # O(log(n)) # Updates 3 and 4
    '''
    def __init__(self, array, operator=add):
        self.op = operator

        self.size = 1
        while self.size <= len(array):
            self.size <<= 1

        padding = [0]*(self.size-len(array)) # Pad to power of 2
        self.A = [0]*self.size + array + padding

        for i in range(self.size-1, 0, -1):
            self.update(i)

    def update(self, parent):
        left_child = parent << 1
        self.A[parent] = self.op(self.A[left_child], self.A[left_child + 1])

    def __getitem__(self, query: Union[slice, int]):
        if isinstance(query, int):
            return self.A[self.size + query]

        lo = (query.start or 0) + self.size
        hi = (self.size if query.stop is None else query.stop) + self.size - 1

        LEFT_CHILD = 0
        RIGHT_CHILD = 1

        total = 0
        A = self.A
        while lo <= hi:
            if lo % 2 == RIGHT_CHILD:
                total = self.op(total, A[lo])
                lo += 1
            if hi % 2 == LEFT_CHILD:
                total = self.op(total, A[hi])
                hi -= 1
            lo >>= 1
            hi >>= 1
        return total

    def __setitem__(self, i: Union[slice, int], value):
        i += self.size
        self.A[i] = value
        i >>= 1
        while i:
            self.update(i)
            i >>= 1

    def __str__(self):
        lo = 1
        hi = 2
        layers = []
        while hi <= len(self.A):
            layers.append(self.A[lo:hi])
            lo <<= 1
            hi <<= 1
        return '\n'.join(map(str, layers))
