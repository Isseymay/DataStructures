import random

from doubly_linkedlist import LinkedList
from skiplist import SkipList
from pytest import fixture

from textwrap import dedent


@fixture
def sl():
    random.seed(123)
    return SkipList(2, [2, 3])


def test_init():
    value = SkipList(2, [1, 2])
    base = value.base
    assert base.head.value == 1
    assert base.head.next.value == 2
    assert base.head.next.next is None


def test_init_linkedlist():
    value = SkipList(2, LinkedList([1, 2]))
    base = value.base
    assert base.head.value == 1
    assert base.head.next.value == 2
    assert base.head.next.next is None


def test_format(sl: SkipList):
    assert format(SkipList(4, [1, 2, 3, 4, 5, 6, 7, 8, 9, 10])) == dedent(
        """
          .  .  .  .  5  .  7  .  .  . 
                      |     |          
          .  2  .  .  5  .  7  .  9  . 
             |        |     |     |    
          .  2  .  .  5  .  7  8  9  . 
             |        |     |  |  |    
         [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]"""[1:]
    )
    assert format(sl, "ll") == dedent(
        """
        [[2, 3],
        [2, 3]]"""[1:]
    )
    assert format(sl, "b") == "[2, 3]"


def test_repr(sl: SkipList):
    assert repr(sl) == "SkipList(2, [2, 3])"


def test_str(sl: SkipList):
    assert str(sl) == "[2, 3]"
