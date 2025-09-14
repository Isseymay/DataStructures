from pytest import raises, fixture

from doubly_linkedlist import LinkedList, ListIterator


@fixture
def ll() -> LinkedList[int]:
    return LinkedList([1, 2, 3])


def test_init():
    value = LinkedList([1, 2, 3])
    head = value.head
    assert head.value == 1
    assert head.prev is None

    next_node = head.next
    assert next_node.value == 2
    assert next_node.prev is head

    last_node = next_node.next
    assert last_node.value == 3
    assert last_node.next is None
    assert last_node.prev is next_node


def test_iter():
    value = LinkedList([1, 2, 3])
    list_iter = iter(value)
    assert isinstance(list_iter, ListIterator)
    assert next(list_iter) == 1
    assert next(list_iter) == 2
    assert next(list_iter) == 3

    with raises(StopIteration):
        next(list_iter)

def test_push(ll: LinkedList[int]):
    ll.push(4)

    assert ll.size == 4
    assert ll.tail().value == 4

def test_push_front(ll: LinkedList[int]):
    ll.push_front(0)

    assert ll.size == 4

    head = ll.head
    assert head.value == 0
    assert head.prev is None
    next_node = head.next
    assert next_node.value == 1
    assert next_node.prev is head


def test_getitem(ll: LinkedList[int]):
    assert ll[0] == 1
    assert ll[1] == 2
    assert ll[2] == 3

    with raises(IndexError):
        _ = ll[3]

    assert ll[-1] == 3
    assert ll[-2] == 2
    assert ll[-3] == 1

    with raises(IndexError):
        _ = ll[-4]


def test_setitem(ll: LinkedList[int]):
    ll[1] = 7
    assert ll[0] == 1
    assert ll[1] == 7
    assert ll[2] == 3

    with raises(IndexError):
        ll[3] = 4

    ll[-2] = 6
    assert ll[0] == 1
    assert ll[1] == 6
    assert ll[2] == 3

    with raises(IndexError):
        ll[-4] = 4

def test_delitem(ll: LinkedList[int]):
    del ll[1]
    assert ll.size == 2
    assert ll[0] == 1
    assert ll[1] == 3


def test_contains(ll: LinkedList[int]):
    assert 1 in ll
    assert 4 not in ll
    assert None not in ll


def test_stringification(ll: LinkedList[int]):
    assert repr(ll) == "LinkedList([1, 2, 3])"
    assert str(ll) == "[1, 2, 3]"
    assert format(ll) == "[1, 2, 3]"