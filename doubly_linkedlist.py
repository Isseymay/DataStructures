# Node class to make the nodes that make up the doubly linked list (therefore need to store both the previous and future nodes)
from __future__ import annotations

from collections.abc import Iterator
from dataclasses import dataclass


@dataclass
class Node[T]:
    # Node constructor that allows for a node to be created without a previous or next
    value: T
    prev: Node[T] | None = None
    next: Node[T] | None = None

    def __lt__(self,other):
        return str(self.value) < str(other.value)
    
    def __gt__(self,other):
        return str(self.value) > str(other.value)
    
    def __le__(self,other):
        return str(self.value)<=str(other.value)
    
    def __ge__(self,other):
        return str(self.value)>=str(other.value)
    

# Class to actually make the linked list and all it's methods
class LinkedList:
    # constructor method that allows an initial list to be passed in to instantiate values
    def __init__(self, initial: list):
        self.size_ = 0 # stores the length of the list
        self.head: Node | None = None # the head of the list starts at None but will be assigned a Node when nodes are added

         # going through and pushing all values fron the initializing list
        for val in initial:
            self.push(val)

    # pushes a value to the front of the list
    def push_front(self, value):
        temp = Node(value,None,self.head)
        self.head = temp
        self.size_+=1

    # pushes a value to the end of the list
    def push(self,value):
        tail = self.tail()
        if tail is None:
            self.head = Node(value, None, None)
        else:
            tail.next = Node(value, tail, None)
        self.size_+=1

    # dunder method so that list[index] will return the node at that position also facilitates for x in list
    def __getitem__(self,index):
        if index > self.size_:
            return None
        iter = self.begin()+(index) 
        return iter.get_node()

    def __iter__(self):
        return self.begin()

    # dunder methat so that writing list[index] = value will actually change the value of the node at that position
    def __setitem__(self,index,val):
        iter = self.begin()+(index) 
        iter.get_node().set_val(val)

    # pops the first node out of the list (moves the head down by one value)
    def pop_front(self):
        self.head = self.head.prev
        self.size_-=1

    # pops the last value from the list (changes the second last node to go to None instead of the next node)
    def pop(self):
        second_last = self.end()-1
        second_last.get_node().set_next(None)
        self.size_-=1

    # insert a value into the list at a specific positon (given either an index value or a list iterator) -- cannot insert to the end (pushes back the value currently in that spot)
    def insert(self,value,pos):
        temp_node = None
        if type(pos) == int:
            temp_node = self.__getitem__(pos)
        elif type(pos) == ListIterator:
            temp_node = pos.get_node()
        else:
            raise Exception("pos needs to be an int or listIterator")

        try:
            prev_node = temp_node.prev
            new_node = Node(value,prev_node,temp_node)
            temp_node.set_prev(new_node)
            if prev_node != None:
                prev_node.set_next(new_node)
            else:
                self.head = new_node
            self.size_+=1       
        except:
            print("There was an error inserting")

    # returns the node at the front of the list
    def front(self):
        return self.head

    def tail(self) -> Node | None:
        """returns the node at the end of the list"""
        node = self.head
        if node is None:
            return None
        while node.next:
            node = node.next
        return node

    # returns a boolean that is true if the list is empty
    def empty(self):
        return self.size_==0
    
    # returns the size of the list
    def size(self):
        return self.size_
    
    def __len__(self):
        return self.size_
    
    # dunder method such that if value in list will work accuately (value in list will return a boolean)
    def __contains__(self,val):
        iter = self.begin()
        for i in range(self.size_):
            if iter.val() == val:
                return True
            iter+=1
        return False
    
    # returns the index of the first version of that value or none if it's not there.
    def index(self,val):
        iter = self.begin()
        for i in range(self.size_):
            if iter.val() == val:
                return i
            iter+=1
        return None
    
    def find(self,val):
        iter = self.begin()
        for i in range(self.size_-1):
            if iter.val() == val:
                return iter
            iter+=1
        return None
    
    # will return an iterator that points to the first node
    def begin(self):
        return ListIterator(self.head, self)

    # given an iterator for the destination of the data (within the current list), an iterator that points to where the data should come from and the number of elements to be moved, this method will transfer the nodes to directly after the destination node cutting them from where they originally were
    def splice(self,dest, source, length):
        # if no length is entered it is autoatically set to 1
        if length == None:
            length = 1


        # connecting the front of the splice section to the destination
        if self.size_==0:
            self.head = source.get_node()
            source.get_node().set_prev(None)
            end = source+length
            end.get_node().set_next(None)
            # end.get_node().Next.setPrev(end.get_node())
        else:
            dest.get_node().set_next(source.get_node())
            source.get_node().set_prev(dest.get_node())

            # if dest isn't the last value in the list, the end of the splice section is connected to it
            temp_end = dest.get_node().prev
            if temp_end!=None:
                end = source+length
                end.get_node().set_next(temp_end)
                end.get_node().prev.set_prev(end.get_node())
        

        # disconnecting  the spliced section from it's original place
        sourceEnd = (source+length).get_node().prev
        if source.list.head == source.get_node():
            source.list.head = (source+length).get_node().prev
            if sourceEnd!=None:
                sourceEnd.set_prev(None)
        else:
            sourcePrev = source.get_node().prev
            sourcePrev.set_next(sourceEnd)
            sourceEnd.set_prev(sourcePrev)

        # updating the sizes of the lists that were affected
        dest.list.size_+=length
        source.list.size_-=length

    # deletes the first instance of a value from the list
    def delete(self,value):
        iter = self.begin()
        for i in range(self.size_-1):
            if iter.val() == value:
                if iter.get_node().prev != None:
                    prev = iter.get_node().prev
                    prev.set_next(iter.get_node().prev)
                if iter.get_node().prev != None:
                    next = iter.get_node().prev
                    next.set_prev(iter.get_node().prev)
                break

    # bubble sort bc I said so
    def sort_list(self):
        passes = 1
        swapped = False
        while passes<(self.size_-1):
            i = 0
            j = 1
            while j<(self.size_):
                if self[i] > self[j]:
                    temp = self[i].value
                    self[i] = self[j].value
                    self[j] = temp
                    swapped = True
                i+=1
                j+=1
            if swapped == False:
                break
            passes+=1



    # using format dunder method so that f"{linkedList}" will look like a regular list
    def __format__(self,format_specs):
        out = f"["
        
        if self.size_>0:
            iter = self.begin()
            # print(f"======{iter}")
            out+=f"{iter.val()}"
            for i in range(self.size_-1):
                iter+=1
                # if iter is not None:
                #     print(f"======={iter}")
                # print(i, iter, self.size_)
                if (i<(self.size_-1)):
                    out+=", "
                out+=f"{iter.val()}"  
        out+="]"
        return out
    
    def convert_to_list(self):
        temp = []
        iter = self.begin()
        for i in range(self.size_):
            temp.append(iter.val())
            iter+=1
        return temp
    
class ListIterator(Iterator):
    # constructor method for pointer/iterator that requires a starting node and the list it should be part of
    def __init__(self, node: Node, lst: LinkedList):
        self.node = node
        self.list = lst

    def __next__(self):
        result = self.node
        if result is None:
            raise StopIteration

        next_node = result.next
        self.node = next_node
        return result.value

    # dunder method such that f"{listIterator}" will show the value of the node
    def __format__(self,format_specs):
        return f"{self.node.value}"
    