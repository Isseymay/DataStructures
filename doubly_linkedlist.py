# Node class to make the nodes that make up the doubly linked list (therefore need to store both the previous and future nodes)
from __future__ import annotations

from collections.abc import Iterator, MutableSequence
from dataclasses import dataclass
from traceback import format_exception
from typing import assert_never, override


@dataclass
class Node[T]:
    # Node constructor that allows for a node to be created without a previous or next
    value: T
    list: LinkedList[T]
    prev: Node[T] | None = None
    next: Node[T] | None = None

    def __lt__(self, other):
        return str(self.value) < str(other.value)

    def __gt__(self, other):
        return str(self.value) > str(other.value)

    def __le__(self, other):
        return str(self.value) <= str(other.value)

    def __ge__(self, other):
        return str(self.value) >= str(other.value)


# Class to actually make the linked list and all it's methods
class LinkedList[T](MutableSequence[T]):
    # constructor method that allows an initial list to be passed in to instantiate values
    def __init__(self, initial: list[T]):
        self.size = 0
        """stores the length of the list"""
        self.head: Node[T] | None = None
        """the head of the list starts at None but will be assigned a Node when nodes are added"""

        # going through and pushing all values fron the initializing list
        for val in initial:
            self.push(val)

    def push_front(self, value: T):
        """pushes a value to the front of the list"""
        old_head = self.head
        self.head = Node(value, self, prev=self.head)
        old_head.prev = self.head
        self.size += 1

    def push(self, value: T):
        """pushes a value to the end of the list"""
        tail = self.tail()
        if tail is None:
            self.head = Node(value, self)
        else:
            tail.next = Node(value, self, tail)
        self.size += 1

    def __iter__(self):
        return ListIterator(self.head)

    def __getitem__(self, index: int):
        """dunder method so that list[index] will return the node at that position also facilitates for x in list"""
        if index >= self.size or index < -self.size:
            raise IndexError
        if index < 0:
            index += self.size
        node = self.head
        for i in range(index):
            node = node.next
        return node.value

    def __setitem__(self, index: int, val: T):
        """dunder method so that writing list[index] = value will actually change the value of the node at that position"""
        if index >= self.size or index < -self.size:
            raise IndexError
        if index < 0:
            index += self.size
        node = self.head
        for i in range(index):
            node = node.next
        node.value = val

    def __delitem__(self, index: int):
        if index >= self.size or index < -self.size:
            raise IndexError
        if index < 0:
            index += self.size
        node = self.head
        for i in range(index):
            node = node.next
        node.prev.next = node.next
        node.next.prev = node.prev
        self.size -= 1

    # pops the first node out of the list (moves the head down by one value)
    def pop_front(self):
        self.head = self.head.next
        self.head.prev = None
        self.size -= 1

    # pops the last value from the list (changes the second last node to go to None instead of the next node)
    def pop(self):
        tail = self.tail()
        if not tail:
            raise IndexError
        second_last = tail.prev
        second_last.next = None
        self.size -= 1
        return tail.value

    def insert(self, value: T, pos: int | ListIterator[T]):
        """insert a value into the list at a specific positon (given either an index value or a list iterator) -- cannot insert to the end (pushes back the value currently in that spot)"""
        match pos:
            case int():
                temp_node = (iter(self) + pos).node
            case ListIterator():
                temp_node = pos.node
            case _:
                assert_never(pos)

        try:
            prev_node = temp_node.prev
            new_node = Node(value, self, prev_node, temp_node)
            temp_node.prev = new_node
            if prev_node is not None:
                prev_node.next = new_node
            else:
                self.head = new_node
            self.size += 1
        except Exception as e:
            print(f"There was an error inserting:\n{format_exception(e)}")

    # returns the node at the front of the list
    def front(self):
        return self.head

    def tail(self):
        """returns the node at the end of the list"""
        return iter(self).move_to_end().node_or_empty

    @property
    def is_empty(self):
        """returns a boolean that is true if the list is empty"""
        return self.size == 0

    def __len__(self):
        return self.size

    def __contains__(self, val: object):
        """dunder method such that if value in list will work accuately (value in list will return a boolean)"""
        for item in self:
            if item == val:
                return True
        return False

    def index(self, val: object):
        """returns the index of the first version of that value or none if it's not there."""
        for i, element in enumerate(self):
            if element == val:
                return i
        return None

    def find(self, val):
        for element in self:
            if element == val:
                return element
        return None

    def splice(self, dest: ListIterator[T], source: ListIterator[T], length: int = 1):
        """this method will transfer the nodes to directly after the destination node cutting them from where they originally were

        given an iterator for the destination of the data (within the current list), an iterator that points to where the data should come from and the number of elements to be moved
        """
        # connecting the front of the splice section to the destination
        if self.is_empty:
            source_node = source.node
            self.head = source_node
            source_node.prev = None
            end = source + length
            end.node.next = None
            # end.node.Next.setPrev(end.node)
        else:
            dest.node.next = source.node
            source.node.prev = dest.node

            # if dest isn't the last value in the list, the end of the splice section is connected to it
            temp_end = dest.node.prev
            if temp_end is not None:
                end = source + length
                end.node.next = temp_end
                prev = end.node.prev
                if prev is None:
                    raise IndexError
                prev.prev = end.node

        # disconnecting  the spliced section from it's original place
        source_end = (source + length).node.prev
        if source.node.list.head == source.node:
            source.node.list.head = (source + length).node.prev
            if source_end is not None:
                source_end.prev = None
        else:
            source_prev = source.node.prev
            if source_prev is None:
                raise IndexError
            source_prev.next = source_end
            if source_end is None:
                raise IndexError
            source_end.prev = source_prev

        # updating the sizes of the lists that were affected
        dest.node.list.size += length
        source.node.list.size -= length

    def delete(self, value: object):
        """deletes the first instance of a value from the list"""
        node = self.head
        while node.next:
            if node.value != value:
                node = node.next
                continue
            if node.prev is not None:
                node.prev.next = node.next
            if node.next is not None:
                node.next.prev = node.prev
            self.size -= 1
            return

    # bubble sort bc I said so
    def sort_list(self):
        passes = 1
        swapped = False
        while passes < (self.size - 1):
            i = 0
            j = 1
            while j < self.size:
                if self[i] > self[j]:
                    temp = self[i].value
                    self[i] = self[j].value
                    self[j] = temp
                    swapped = True
                i += 1
                j += 1
            if not swapped:
                break
            passes += 1

    # using format dunder method so that string methods will look like a regular list
    def __str__(self):
        return "[" + ", ".join(map(repr, self)) + "]"

    def __repr__(self):
        return "LinkedList(" + str(self) + ")"

    def convert_to_list(self):
        return list(self)


@dataclass
class ListIterator[T](Iterator[T]):
    node_or_empty: Node[T] | None

    @property
    def node(self):
        result = self.node_or_empty
        if result is None:
            raise IndexError
        return result

    @property
    def value(self):
        return self.node.value

    @override
    def __next__(self):
        result = self.node
        if result is None:
            raise StopIteration

        next_node = result.next
        self.node = next_node
        return result.value

    def __add__(self, other: int):
        return self._move(other)

    def __sub__(self, other: int):
        return self._move(other)

    def _move(self, amount: int):
        result = self.node
        for _ in range(amount):
            result = result.next if amount > 0 else result.prev
            if result is None:
                raise IndexError
        return ListIterator(result)

    def move_to_end(self):
        while self.node_or_empty and self.node_or_empty.next:
            self.node_or_empty = self.node_or_empty.next
        return self
