from doubly_linkedlist import LinkedList

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
