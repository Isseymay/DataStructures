from dataclasses import dataclass

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


class SkipList:
    # initializing the skip list
    def __init__(self, height, initial):
        self.lanes = []
        self.size_ = height
        # making a list of the right height full of empty linked lists
        for i in range(height):
            self.lanes.append(LinkedList([]))

        # if initial is a linked list - using the linked list to work initial values into the skip list
        if type(initial) == LinkedList:
            initial.sort_list()  # has to be sorted
            for i in range(len(initial)):
                base = initial[i].value
                cur_val = initial[i]
                level = 1
                raised = random.choice([True, False])
                self.lanes[-1].push(base)
                while level < (height) and raised == True:
                    temp = SkipListIterator(cur_val, base, self.lanes[-level])
                    level += 1
                    self.lanes[-level].push(temp)
                    cur_val = self.lanes[-level].back()
                    raised = random.choice([True, False])

        # if initial is a list - using the list to work initial values into the skip list
        elif type(initial) == list:
            # this could be done in a better way but this will work for now.
            initial.sort()
            initial = LinkedList(initial)
            for i in range(len(initial)):
                base = initial[i].value
                cur_val = initial[i]
                self.lanes[-1].push(base)
                raised = random.choice([True, False])
                level = 1  # the current level (starting with 1) the number is up to so that it can be used to move backwards through the lanes list
                while level < (height) and raised == True:
                    temp = SkipListIterator(
                        cur_val, base, self.lanes[-level]
                    )  # getting the skipListIterator of the current lane to put as the element in the lane one step upwards
                    level += 1  # adding to level so it is now referring to the lane one step up
                    self.lanes[-level].push(temp)
                    cur_val = self.lanes[-level].back()
                    raised = random.choice([True, False])

    # making it so that the skip list will print in one of two formats
    def __format__(self, format_specs):
        # printing as lists e.g
        #    [[1],
        #    [1, 2, 4],
        #    [1, 2, 3, 4, 5, 6, 7, 8]]

        if format_specs == "ll":
            out = "["
            count = 0
            for lane in self.lanes:
                out += "["
                if len(lane) > 0:
                    iter = lane.begin()
                    if iter is not None:
                        out += f"{iter.value}"
                    for i in range(lane.size() - 1):
                        iter += 1
                        if i < (lane.size() - 1):
                            out += ", "
                        if iter is not None:
                            out += f"{iter.value}"

                    count += 1
                out += "],\n"
            out = out[:-2]
            out += "]\n"
            return out
        # only printing the base list e.g.
        #    [1, 2, 3, 4, 5, 6, 7, 8]

        elif format_specs == "b":
            return f"{self.lanes[-1]}"

        # printing in the form of a skip list e.g.
        #     1  .  .  .  .  .  .  .
        #     |
        #     1  2  .  4  .  .  .  .
        #     |  |     |
        #     [1, 2, 3, 4, 5, 6, 7, 8]

        else:
            # is buggy (will run into issues if there's repeat numbers)
            out = ""
            for i in range(len(self.lanes) - 1):
                vals = [" . "] * len(self.lanes[-1])
                gaps = ["   "] * len(self.lanes[-1])
                lane = self.lanes[i]
                if len(lane) > 0:
                    iter = lane.begin()
                    for n in range(lane.size()):
                        v = iter.value.value
                        num = self.lanes[-1].index(v)
                        if num != None:
                            vals[num] = " " + str(v) + " "
                            gaps[num] = " | "
                        iter += 1

                out += "".join(vals) + "\n"
                out += "".join(gaps) + "\n"

            out += f"{self.lanes[-1]}\n"
            return out

            # go through each lane and make two lists the same width as len(base) one populated with dots and the other with spaces
            # go through every value from the lane and find the index it is in base, replace that index in the dots list with the value, and that index in the spaces list with a pipe
            # print the two lists joined with no gaps ""
            # repeat except for base, with base just print the joined version of base

    # currently adding twice to base (in wrong spot) then adding none to upper lane
    def add(self, val):
        place = self.lane_search(
            val, (self.size_ - 1)
        )  # currently an iter to base (or none if the val is greater than all current values)
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
        while level <= self.size_ and raised == True:
            lane_iter = self.lane_search(val, (self.size_ - level))
            temp = SkipListIterator(cur_node, val, self.lanes[-(level)])

            if lane_iter == None:
                self.lanes[-level].push(temp)
                cur_node = self.lanes[-level].back()
            else:
                self.lanes[-level].insert(temp, lane_iter)
                cur_node = lane_iter.node
            level += 1
            raised = random.choice([True, False])

    # REWRITE THIS!!!!!!!!!
    # will return the iter of the first instance of val or the element higher than it and will throw an error if laneNum out of range and will return None if val should be at the end
    def lane_search(
        self, val, lane_num
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
    def delete(self, val):
        pass

    # base algo (original with singly linked list) returns the listIterator to the base that either points to the first instance of the value or the value directly above it .: can just add to base at the place iter that has been returned)
    def search(self, val):
        if val < self.front().value:
            return self.base().begin()
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
    def search_rec(self, cur_iter, old_iter, lane, val, same):
        cur_val = cur_iter.value
        if lane < (self.size_ - 1):
            cur_val = cur_val.value
        if val == cur_val:
            if lane == (self.size_ - 1):
                return cur_iter
            elif not same:
                temp = ListIterator(old_iter.value.node, self.lanes[lane + 1])
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
                temp = ListIterator(old_iter.value.node, self.lanes[lane + 1])
                a = self.search_rec(temp, temp, lane + 1, val, True)
                return a
        else:
            if cur_iter.node.prev != None:
                temp = cur_iter
                a = self.search_rec(cur_iter + 1, temp, lane, val, False)
                return a
            else:
                temp = ListIterator(cur_iter.value.node, self.lanes[lane + 1])
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
        return self.base().size()

    # returns the base linked list
    def base(self):
        return self.lanes[-1]

    # returns true id the skip list is emtpy
    def empty(self):
        return self.num_elements() == 0

    # dunder method to make len(skipList) work
    def __len__(self):
        return self.base().size()

    # converts skip list to list based off linked list method
    def convert_to_list(self):
        return self.base().convert_to_list()

    # returns the first node of the base
    def front(self):
        return self.base().front()

    # returns the last node of the base
    def back(self):
        return self.base().back()

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
        val = self.back()
        for i in range(self.size_):
            if self.lanes[i].back() == val:
                self.lanes[i].pop()

    # fully reconfigures the skip list to contain more lanes, re-issuing new max heights to each element using the same initial process
    def reconfigure(self, new_height):
        lst = self.base()
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
            while level < (new_height) and raised == True:
                temp = SkipListIterator(cur_val, base, self.lanes[-level])
                level += 1
                self.lanes[-level].push(temp)
                cur_val = self.lanes[-level].back()
                raised = random.choice([True, False])


# iterator that will be used in the lanes of the skip list to ensure that all processes can be easlily performed (similar to the linkedListIterator but it contains one more attribute and method. The attribute is base value (the value at the base of the skip list column), and the method is used to get said vlaue)
@dataclass
class SkipListIterator:
    node: Node
    """the whole node at this iterator (like using * in c++)"""
    value: object
    """the base value at this iterator"""
    list: LinkedList

    # dunder method so that iterator+=number will correctly increment it with relation to the current lane of the skip list
    def __iadd__(self, other: int):
        for i in range(other):
            if self.node.prev != None:
                self.node = self.node.prev
            else:
                return None
        return self

    # dunder method so that iterator+number will return a new iterator incremented with relation to the current lane of the skip list
    def __add__(self, other: int):
        temp = ListIterator(self.node, self.list)
        for i in range(other):
            if temp.node.prev != None:
                temp.node = temp.node.prev
            else:
                break
        return temp

    # dunder method such that iterator-=number will decrement the iterator with respect to the current lane of the skip list
    def __isub__(self, other: int):
        for i in range(other):
            if self.node.prev != None:
                self.node = self.node.prev
            else:
                return None
        return self

    # dunder method such that iterator-number will return a new iterator that has been decremented with respect to the current lane of the skip list
    def __sub__(self, other: int):
        temp = ListIterator(self.node, self.list)
        for i in range(other):
            if temp.node.prev != None:
                temp.node = temp.node.prev
            else:
                break
        return temp

    # makes it so that when you print this iterator, it prints just the base value
    def __format__(self, format_specs):
        return f"{self.value}"


# testing
