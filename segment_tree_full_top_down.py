from typing import Union, Tuple
from operator import add
from collections import namedtuple

class SegmentTree:
    '''
    Example use:
        t = SegmentTree([6, 3, -1, 1, 3], operator=add) # O(n)
        t[0] -= 3 # O(log(n))
        t[3] = 11 # O(log(n))
        assert t[:4] == 16 # prints the sum of the first 4 elements O(log(n))
        BROKEN: t[3:5] -= 3 # O(log(n)) # Updates 3 and 4
    
    NOTE: Pads input to be power of 2. Doesn't validate input to be in original range!
    '''
    # Supports assignment like x[5:8] = 0 and changes like x[9:12] += 2
    # When assigment occurs, the change should be reset to 0
    # When no assignment has been done, it is None.
    # When a new assignment occurs, it just overwrites the old assignment value
    Lazy = namedtuple('Lazy', ['assign', 'change'])

    def __init__(self, array, operator=add, default=0):
        ''' Default is the starting/fill value, e.g. for operator=min you might want default=float('inf') '''
        self.op = operator
        self.default = default

        self.n = 1
        while self.n <= len(array):
            self.n <<= 1

        padding = [self.default]*(self.n-len(array)) # Pad to power of 2
        self.A = [0]*self.n + array + padding

        self._lazy = [self.Lazy(None, 0)]*len(self.A)

        for i in range(self.n-1, 0, -1):
            self._update(i)

    def _update(self, parent):
        left_child = parent << 1
        self.A[parent] = self.op(self.A[left_child], self.A[left_child + 1])

    def __getitem__(self, query: Union[slice, int]):
        if isinstance(query, int):
            return self.A[self.n + query]

        start, end, = self._get_start_end(query) # Note, end is inclusive
        if start == end:
            return self[start - self.n]

        total = self.default
        if start >= len(self.A) or end < self.n:
            return total

        cut_size = self.n

        l_idx = self.n # Left boundry inclusive
        r_idx = len(self.A)-1 # Right boundry inclusive

        lo = hi = 1 # Subtree root corresponding to boundry
        while (lo := lo << 1) <= (hi := hi << 1) < len(self.A):
            cut_size >>= 1
            different_subtrees = hi != lo
            hi += 1
            # If start is to the right after doing cut:
            if start >= (new_l := l_idx + cut_size): 
                l_idx = new_l
                lo += 1 # Goto right neighbour subtree
            elif different_subtrees:
                # Add right subtree
                total = self.op(total, self.A[lo + 1]) 

            if end <= (new_r := r_idx - cut_size):
                r_idx = new_r
                hi -= 1
            elif different_subtrees:
                total = self.op(total, self.A[hi - 1]) 

        lo >>= 1 # While statement increased it
        hi >>= 1
        assert l_idx == lo and r_idx == hi
        total = self.op(self.op(
                total, 
                self.A[hi]
            ),
            self.A[lo],
        )

        return total

    def __setitem__(self, query: Union[slice, int], value) -> None:
        if isinstance(query, int):
            i = query + self.n
            self.A[i] = value
            while (i := i >> 1): self._update(i)
            return None
        raise NotImplementedError
    
    def _get_start_end(self, query: slice) -> Tuple[int, int]:
        # Returns inclusive
        start = (query.start or 0) + self.n
        end = self.n-1 + (self.n if query.stop is None else query.stop)
        if query.start < 0: start += self.n
        if query.stop < 0:  end += self.n
        assert start <= end
        return start, end

    def __str__(self):
        # size = max(map(len, map(str, self.A)))

        # lo = 1
        # hi = 2
        # layers = []
        # while hi <= len(self.A):
        #     layer = ''.join(f'{c:^{size}}' for c in self.A[lo:hi])
        #     layers.append(f'{layer:^{size*log2(self.n*2)}}')
        #     lo <<= 1
        #     hi <<= 1
        # return '\n'.join(layers)

        lo = 1
        hi = 2
        layers = []
        while hi <= len(self.A):
            layers.append(self.A[lo:hi])
            lo <<= 1
            hi <<= 1
        return '\n'.join(map(str, layers))

if __name__ == '__main__':
    st = SegmentTree([1, 2, 3, 4, 5, 6, 7], operator=add)
    print(st)
    print(st[:0])
    print(st[:1])
    print(st[:2])
    print(st[:3])
    print(st[:4])
    print(st[:5])
    print(st[:6])
    print(st[:7])
    print(st[:8])
    print(st[:9])
    print(st[:10])
    print(st[10:])
