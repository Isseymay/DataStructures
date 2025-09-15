import copy
from collections.abc import Iterable, Iterator, MutableSet
from typing import override

from doubly_linkedlist import LinkedList, ListIterator

sizes = [
    1,
    13,
    59,
    127,
    257,
    541,
    1109,
    2357,
    5087,
    10273,
    20753,
    42043,
    85229,
    172993,
    351061,
    712697,
    1447153,
    2938679,
]


class HashSet[T](MutableSet[T]):
    def __init__(self, initial: Iterable[T]):
        self.buckets: list[ListIterator[T] | None] = [None]
        self.keys = LinkedList[T]([])
        self.max_load_factor = 2
        self.num_buckets_pos = 0

        for val in initial:
            self.insert(val)

    def bucket(self, value: object):
        hashed = hash(value)
        return hashed % len(self.buckets)

    def __format__(self, format_specs):
        if format_specs == "ll":
            return f"{self.keys}"
        elif format_specs == "b":
            out = "["
            for i in self.buckets:
                out += f"{i}, "
            out = out[:-2]
            out += "]\n"
            return out
        else:
            out = ""
            for i in range(len(self.buckets)):
                out += f"{i}: "
                list_iterator = ListIterator(self.buckets[i].node)
                while (
                    list_iterator is not None
                    and self.bucket(list_iterator.node.value) == i
                ):
                    out += f"{list_iterator.node}, "
                    next(list_iterator)
                out += "\n"
            out += "\n"
            return out

    def insert(self, value: T):
        if value in self.keys:
            return
        hashed = self.bucket(value)
        if self.buckets[hashed] is None:
            self.keys.push(value)
            self.buckets[hashed] = iter(self.keys).move_to_end()
        else:
            self.keys.insert(value, self.buckets[hashed])
        if self.load_factor() > self.max_load_factor:
            self.rehash(len(self.buckets))

    def load_factor(self):
        return len(self.keys) / len(self.buckets)

    def set_max_load(self, value):
        self.max_load_factor = value
        if self.load_factor() > self.max_load_factor:
            self.rehash(len(self.buckets))

    def size(self):
        return len(self.keys)

    def empty(self):
        return len(self.keys) == 0

    def bucket_count(self):
        return len(self.buckets)

    def bucket_size(self, pos):
        if pos < len(self.buckets):
            list_iterator = self.buckets[pos]
            count = 0
            og_hash = self.bucket(list_iterator.value)
            while list_iterator.node.prev is not None:
                if self.bucket(list_iterator.value) != og_hash:
                    break
                count += 1
                next(list_iterator)
            if list_iterator.node.prev is None:
                if self.bucket(list_iterator.value) == og_hash:
                    count += 1
            return count
        return 0

    # returns a boolean of if the value is in the hashset (allows if val in hashset:)
    def __contains__(self, value):
        hashed = self.bucket(value)
        iter = self.buckets[hashed]
        while iter.node.prev is not None:
            if iter.value == value:
                return True

            if self.bucket(iter.value) != hashed:
                break

            iter += 1

        if iter.node.prev is None and iter.value == value:
            return True
        return False

    # will return the list iterator for the value or none if not found
    def find(self, value):
        hashed = self.bucket(value)
        iter = self.buckets[hashed]
        while iter.node.prev is not None:
            if iter.value == value:
                return iter

            if self.bucket(iter.value) != hashed:
                break

            iter += 1

        if iter.node.prev is None and iter.value == value:
            return iter
        return None

    def erase(self, val):
        value = None
        if isinstance(val, int):
            value = val
        elif isinstance(val, ListIterator):
            value = val.value

        self.keys.delete(value)

    def rehash(self, new_size):
        if new_size > len(self.buckets) or self.load_factor() > self.max_load_factor:
            cur_size = len(self.buckets)
            cur_load = self.load_factor()
            i = 0
            for i in range(self.num_buckets_pos + 1, len(sizes)):
                cur_size = sizes[i]
                cur_load = len(self.keys) / cur_size
                if cur_size >= new_size and cur_load <= self.max_load_factor:
                    break

            self.num_buckets_pos = i
            self.buckets = [None] * cur_size

            self.splicing()

    def splicing(self):
        temp = LinkedList[T]([])
        temp.splice(iter(temp), iter(self.keys), self.keys.size)
        length = temp.size
        cur = iter(temp)
        old = iter(temp)
        for i in range(length):
            key = cur.value
            hashed = self.bucket(key)
            dest = self.buckets[hashed]
            old += 1
            if dest is not None:
                self.keys.splice(dest, iter(temp), cur)
                self.buckets[hashed] = dest - 1
            else:
                self.keys.push(key)
                self.buckets[hashed] = iter(self.keys).move_to_end()
            cur = copy.copy(old)

    @override
    def __iter__(self) -> Iterator[T]:
        return iter(self.keys)

    @override
    def __len__(self):
        return self.size()

    @override
    def add(self, value: T):
        self.insert(value)

    @override
    def discard(self, value: object):
        self.erase(value)
