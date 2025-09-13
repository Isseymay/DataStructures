from skiplist import SkipList
from pytest import fixture

@fixture
def sl():
    return SkipList(1,[2])

def test_init():
    value = SkipList(1, [2])
    assert len(value) == 1
    assert value.base()[0].value == 2
