# Node class to make the nodes that make up the doubly linked list (therefore need to store both the previous and future nodes)
from __future__ import annotations

from collections.abc import Iterator
from dataclasses import dataclass
from collections.abc import MutableSequence


@dataclass
class Node[T]:
    # Node constructor that allows for a node to be created without a previous or next
    value: T
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
        self.head: Node | None = None
        """the head of the list starts at None but will be assigned a Node when nodes are added"""

        # going through and pushing all values fron the initializing list
        for val in initial:
            self.push(val)

    def push_front(self, value: T):
        """pushes a value to the front of the list"""
        old_head = self.head
        self.head = Node(value, None, self.head)
        old_head.prev = self.head
        self.size += 1

    def push(self, value: T):
        """pushes a value to the end of the list"""
        tail = self.tail()
        if tail is None:
            self.head = Node(value, None, None)
        else:
            tail.next = Node(value, tail, None)
        self.size += 1

    def __iter__(self) -> ListIterator[T]:
        return ListIterator(self.head)

    def __getitem__(self, index: int) -> T:
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

    # insert a value into the list at a specific positon (given either an index value or a list iterator) -- cannot insert to the end (pushes back the value currently in that spot)
    def insert(self, value, pos):
        temp_node = None
        if isinstance(pos, int):
            temp_node = self.__getitem__(pos)
        elif isinstance(pos, ListIterator):
            temp_node = pos.get_node()
        else:
            raise Exception("pos needs to be an int or listIterator")

        try:
            prev_node = temp_node.prev
            new_node = Node(value, prev_node, temp_node)
            temp_node.set_prev(new_node)
            if prev_node is not None:
                prev_node.set_next(new_node)
            else:
                self.head = new_node
            self.size += 1
        except Exception:
            print("There was an error inserting")

    # returns the node at the front of the list
    def front(self):
        return self.head

    def tail(self):
        """returns the node at the end of the list"""
        node = self.head
        if node is None:
            return None
        while node.next:
            node = node.next
        return node

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

    # given an iterator for the destination of the data (within the current list), an iterator that points to where the data should come from and the number of elements to be moved, this method will transfer the nodes to directly after the destination node cutting them from where they originally were
    def splice(self, dest, source, length):
        # if no length is entered it is autoatically set to 1
        if length is None:
            length = 1

        # connecting the front of the splice section to the destination
        if self.size == 0:
            self.head = source.get_node()
            source.get_node().set_prev(None)
            end = source + length
            end.get_node().set_next(None)
            # end.get_node().Next.setPrev(end.get_node())
        else:
            dest.get_node().set_next(source.get_node())
            source.get_node().set_prev(dest.get_node())

            # if dest isn't the last value in the list, the end of the splice section is connected to it
            temp_end = dest.get_node().prev
            if temp_end is not None:
                end = source + length
                end.get_node().set_next(temp_end)
                end.get_node().prev.set_prev(end.get_node())

        # disconnecting  the spliced section from it's original place
        sourceEnd = (source + length).get_node().prev
        if source.list.head == source.get_node():
            source.list.head = (source + length).get_node().prev
            if sourceEnd is not None:
                sourceEnd.set_prev(None)
        else:
            sourcePrev = source.get_node().prev
            sourcePrev.set_next(sourceEnd)
            sourceEnd.set_prev(sourcePrev)

        # updating the sizes of the lists that were affected
        dest.list.size += length
        source.list.size -= length

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
        temp = []
        iter = self.begin()
        for i in range(self.size):
            temp.append(iter.val())
            iter += 1
        return temp


@dataclass
class ListIterator[T](Iterator[T]):
    node: Node[T]

    def __next__(self) -> T:
        result = self.node
        if result is None:
            raise StopIteration

        next_node = result.next
        self.node = next_node
        return result.value
