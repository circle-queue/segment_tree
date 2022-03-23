# segment_tree
    Example use:
        t = SegmentTree([6, 3, -1, 1, 3], operator=sum) # O(n)
        t[0] -= 3 # O(log(n))
        t[3] = 11 # O(log(n))
        assert t[:4] == 18 # prints the sum of the first 4 elements O(log(n))
