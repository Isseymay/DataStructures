from pytest import raises

from doubly_linkedlist import LinkedList, ListIterator


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
