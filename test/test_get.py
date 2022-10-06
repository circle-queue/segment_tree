from random import randint

from segment_tree_complete_top_down import SegmentTree

def test_get_add():
    st = SegmentTree([1, 2, 3, 4, 5, 6, 7])
    assert st[:0] == 0
    assert st[:1] == 1
    assert st[:2] == 3
    assert st[:3] == 6
    assert st[:4] == 10
    assert st[:5] == 15
    assert st[:6] == 21
    assert st[:7] == 28
    assert st[:8] == 28
    assert st[:9] == 28
    assert st[10:] == 0

def test_get_min():
    st = SegmentTree([1, 2, 3, 4, 5, 6, 7], operator=min, default=float('inf'))
    assert st[0:] == 1
    assert st[1:] == 2
    assert st[2:] == 3
    assert st[3:] == 4
    assert st[4:] == 5
    assert st[5:] == 6
    assert st[6:] == 7
    assert st[7:] == float('inf')
    assert st[:10] == 1

def test_get_random():
    for _ in range(100):
        A = [randint(1, 10) for _ in range(randint(1, 25))]
        st = SegmentTree(A)
        for _ in range(100):
            s = randint(0, len(A))
            e = randint(s+1, len(A)+2)
            assert st[s:e] == sum(A[s:e])

    for _ in range(100):
        A = [randint(1, 10) for _ in range(randint(1, 25))]
        st = SegmentTree(A, operator=min, default=float('inf'))
        for _ in range(100):
            s = randint(0, len(A))
            e = randint(s+1, len(A)+2)
            assert st[s:e] == (min(A[s:e] + [float('inf')]))
test_get_random()