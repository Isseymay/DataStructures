from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from doubly_linkedlist import LinkedList, ListIterator, Node
import random

# todo:
#   -> init (Done)
#   -> add (must be sorted so insert can't work)
#   -> search / (contains/find) (MVP done) (should implement the doubly linked version)
#   -> delete
#   -> reconfigure (add more lanes based on input value to then change the highest level the data can be at. Will not need to reconfigure any values) (done)
#   -> !fomat (work out what this should look like)  (done)
#   -> has most of the same functions as a linked list (done)
#   -> front and back (will be useful for adding) (done)
#   -> size and maybe size of individual lanes/ number of lanes (done)
#   -> begin/end (done)
#   -> testing (in progress)


class SkipList[T]:
    # initializing the skip list
    def __init__(self, height: int, initial: list[T] | LinkedList):
        self.lanes = list[LinkedList]()
        self.size_ = height
        # making a list of the right height full of empty linked lists
        for i in range(height):
            self.lanes.append(LinkedList([]))

        # if initial is a list - using the list to work initial values into the skip list
        if isinstance(initial, list):
            initial = LinkedList(initial)

        initial.sort_list()  # has to be sorted
        for i in range(len(initial)):
            base = initial[i]
            cur_val = initial[i]
            level = 1
            raised = random.choice([True, False])
            self.lanes[-1].push(base)
            while level < height and raised:
                level += 1
                self.lanes[-level].push(cur_val)
                cur_val = self.lanes[-level].tail().value
                raised = random.choice([True, False])

    def __repr__(self):
        return f"SkipList({self.size_}, {self.base})"

    def __str__(self):
        return str(self.base)

    # making it so that the skip list will print in various formats
    def __format__(self, format_specs: Literal["ll", "b", ""]):
        if format_specs == "ll":
            # printing as lists e.g
            #    [[1],
            #    [1, 2, 4],
            #    [1, 2, 3, 4, 5, 6, 7, 8]]
            return "[" + ",\n".join(str(lane) for lane in self.lanes) + "]"

        elif format_specs == "b":
            # only printing the base list e.g.
            #    [1, 2, 3, 4, 5, 6, 7, 8]
            return format(self.base)

        # printing in the form of a skip list e.g.
        #     1  .  .  .  .  .  .  .
        #     |
        #     1  2  .  4  .  .  .  .
        #     |  |     |
        #     [1, 2, 3, 4, 5, 6, 7, 8]

        # is buggy (will run into issues if there's repeat numbers)
        out = ""
        for i in range(len(self.lanes) - 1):
            vals = [" . "] * len(self.base)
            gaps = ["   "] * len(self.base)
            lane = self.lanes[i]
            for v in lane:
                num = self.base.index(v)
                if num is not None:
                    vals[num] = " " + repr(v) + " "
                    gaps[num] = " | "

            out += "".join(vals) + "\n"
            out += "".join(gaps) + "\n"

        out += str(self.base)
        return out

        # go through each lane and make two lists the same width as len(base) one populated with dots and the other with spaces
        # go through every value from the lane and find the index it is in base, replace that index in the dots list with the value, and that index in the spaces list with a pipe
        # print the two lists joined with no gaps ""
        # repeat except for base, with base just print the joined version of base

    # currently adding twice to base (in wrong spot) then adding none to upper lane
    def add(self, val: T):
        # currently an iter to base (or none if the val is greater than all current values)
        place = self.lane_search(val, (self.size_ - 1))
        if place is None:
            self.lanes[-1].push(val)
        else:
            self.lanes[-1].insert(
                val, place
            )  # insert the value into the base (place is the issue TwT)
            temp = place - 1

        # ^ works

        # need to then escalate it up (need to write a search algorithm to find it's place in each upper level)
        # need a node of the element in base to make the raised skipListIterator
        temp_index = self.lanes[
            -1
        ].index(
            val
        )  # this will find the first instance of val (which will always be the new node as it's always inserting into the iterator at the first instance of the number therefore becoming the first instance)
        cur_node = self.lanes[-1][temp_index]
        level = 2
        raised = random.choice([True, False])
        while level <= self.size_ and raised:
            lane_iter = self.lane_search(val, (self.size_ - level))
            temp = SkipListIterator(cur_node, val, self.lanes[-(level)])

            if lane_iter is None:
                self.lanes[-level].push(temp)
                cur_node = self.lanes[-level].tail()
            else:
                self.lanes[-level].insert(temp, lane_iter)
                cur_node = lane_iter.node
            level += 1
            raised = random.choice([True, False])

    # REWRITE THIS!!!!!!!!!
    # will return the iter of the first instance of val or the element higher than it and will throw an error if laneNum out of range and will return None if val should be at the end
    def lane_search(
        self, val: T, lane_num: int
    ):  # here laneNum starts at 0 -> lane 0 (like the list structure)
        if (
            lane_num >= self.size_
        ):  # if the lane is out of bounds it can't have a position therefore returns None
            raise Exception("laneNum out of range")
        base = False
        if lane_num == (self.size_ - 1):  # if lane is base (wrong)
            base = True
        iter = self.lanes[lane_num].begin()
        temp = iter.value  # listIterator of a skipListIterator
        if not base:
            temp = temp.value
        if val < temp:
            return self.lanes[lane_num].begin()
        temp2 = self.lanes[lane_num].end().value
        if not base:
            temp2 = temp2.value
        if val > temp2:
            return None  # returns none if val greater than the last value of the lane (basically as a flag to show it needs to be pushed not inserted)
        for i in range(self.lanes[lane_num].size()):
            temp3 = iter.value
            if not base:
                temp3 = temp3.value
            if temp3 == val:
                return iter
            elif temp3 > val:
                return iter
            iter += 1
        return None

    # not yet written
    def delete(self, val: object):
        pass

    # base algo (original with singly linked list) returns the listIterator to the base that either points to the first instance of the value or the value directly above it .: can just add to base at the place iter that has been returned)
    def search(self, val):
        if val < self.front().value:
            return self.base.begin()
        if val > self.back().value:
            return None  # needs to not return the last value as insert doesn't work at the last value so it needs a special return to show that it needs to be pushed instead
        lane = 0
        while lane < self.size_:
            if len(self.lanes[lane]) == 0:
                lane += 1
                continue
            temp = self.lanes[lane].begin()
            return self.search_rec(temp, temp, lane, val, True)

    # uses a recursive method to search the skip list (standard singly linked list algorithm)
    def search_rec(
        self,
        cur_iter: ListIterator,
        old_iter: ListIterator,
        lane: int,
        val: T,
        same: bool,
    ):
        cur_val = cur_iter.val()
        if lane < (self.size_ - 1):
            cur_val = cur_val.value
        if val == cur_val:
            if lane == (self.size_ - 1):
                return cur_iter
            elif not same:
                temp = ListIterator(old_iter.val().node, self.lanes[lane + 1])
                a = self.search_rec(temp, temp, lane + 1, val, True)
                return a
            else:
                a = self.search_rec(
                    self.lanes[lane + 1].begin(),
                    self.lanes[lane + 1].begin(),
                    lane + 1,
                    val,
                    True,
                )
                return a
        elif cur_val > val:
            if lane == (self.size_ - 1):
                return cur_iter
            elif same:
                a = self.search_rec(
                    self.lanes[lane + 1].begin(),
                    self.lanes[lane + 1].begin(),
                    lane + 1,
                    val,
                    True,
                )
                return a
            else:
                temp = ListIterator(old_iter.val().node, self.lanes[lane + 1])
                a = self.search_rec(temp, temp, lane + 1, val, True)
                return a
        else:
            if cur_iter.node.prev is not None:
                temp = cur_iter
                a = self.search_rec(cur_iter + 1, temp, lane, val, False)
                return a
            else:
                temp = ListIterator(cur_iter.val().node, self.lanes[lane + 1])
                a = self.search_rec(temp, temp, lane + 1, val, True)
                return a

    # if its a valid lane, returns the whole linked list
    def get_lane(self, lane):
        if lane >= self.size_:
            return LinkedList([])
        else:
            return self.lanes[lane]

    # if its a valid, returns the size of the lane otherwise returns 0
    def size_of_lane(self, lane):
        return self.get_lane(lane).size()

    # returns the number of elements in the base list
    def num_elements(self):
        return self.base.size()

    @property
    def base(self):
        """returns the base linked list"""
        return self.lanes[-1]

    # returns true id the skip list is emtpy
    def empty(self):
        return self.num_elements() == 0

    # dunder method to make len(skipList) work
    def __len__(self):
        return self.base.size

    # converts skip list to list based off linked list method
    def convert_to_list(self):
        return self.base.convert_to_list()

    # returns the first node of the base
    def front(self):
        return self.base.front()

    # returns the last node of the base
    def tail(self):
        return self.base.tail()

    # dunder method so that if val in skipList works
    def __contains__(self, val):
        a = self.search(val)
        return a.value == val

    # pops the first node from the skip list (based off the c++ pop)
    def pop_front(self):
        val = self.front()
        for i in range(self.size_):
            if self.lanes[i].front() == val:
                self.lanes[i].pop_front()

    # pops the last node from the skip list (based off the c++ pop)
    def pop(self):
        val = self.tail()
        for i in range(self.size_):
            if self.lanes[i].tail() == val:
                self.lanes[i].pop()

    # fully reconfigures the skip list to contain more lanes, re-issuing new max heights to each element using the same initial process
    def reconfigure(self, new_height):
        lst = self.base
        self.lanes = []
        self.size_ = new_height
        for i in range(new_height):
            self.lanes.append(LinkedList([]))
        for i in range(len(lst)):
            base = lst[i].value
            cur_val = lst[i]
            level = 1
            raised = random.choice([True, False])
            self.lanes[-1].push(base)
            while level < (new_height) and raised:
                temp = SkipListIterator(cur_val, base, self.lanes[-level])
                level += 1
                self.lanes[-level].push(temp)
                cur_val = self.lanes[-level].back()
                raised = random.choice([True, False])


# iterator that will be used in the lanes of the skip list to ensure that all processes can be easlily performed (similar to the linkedListIterator but it contains one more attribute and method. The attribute is base value (the value at the base of the skip list column), and the method is used to get said vlaue)
@dataclass
class SkipListIterator[T]:
    node: Node
    """the whole node at this iterator (like using * in c++)"""
    value: T
    """the base value at this iterator"""
    list: LinkedList

    def __next__(self):
        if self.node.next is not None:
            self.node = self.node.next
            return self.value
        raise StopIteration

    # dunder method so that iterator+=number will correctly increment it with relation to the current lane of the skip list
    def __iadd__(self, other: int):
        for i in range(other):
            if self.node.prev is not None:
                self.node = self.node.prev
            else:
                return None
        return self

    # dunder method so that iterator+number will return a new iterator incremented with relation to the current lane of the skip list
    def __add__(self, other: int):
        temp = ListIterator(self.node, self.list)
        for i in range(other):
            if temp.node.prev is not None:
                temp.node = temp.node.prev
            else:
                break
        return temp

    # dunder method such that iterator-=number will decrement the iterator with respect to the current lane of the skip list
    def __isub__(self, other: int):
        for i in range(other):
            if self.node.prev is not None:
                self.node = self.node.prev
            else:
                return None
        return self

    # dunder method such that iterator-number will return a new iterator that has been decremented with respect to the current lane of the skip list
    def __sub__(self, other: int):
        temp = ListIterator(self.node, self.list)
        for i in range(other):
            if temp.node.prev is not None:
                temp.node = temp.node.prev
            else:
                break
        return temp

    # makes it so that when you print this iterator, it prints just the base value
    def __format__(self, format_specs: str):
        return f"{self.value}"


# testing
