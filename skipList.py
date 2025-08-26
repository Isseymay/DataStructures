from doublyLinkedList import linkedList,listIterator,Node
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

class skipList:
    #initializing the skip list
    def __init__(self,height,initial):
        self.lanes = []
        self.size_ = height
        # making a list of the right height full of empty linked lists
        for i in range(height):
            self.lanes.append(linkedList([]))

        # if initial is a linked list - using the linked list to work initial values into the skip list
        if type(initial) == linkedList:
            initial.sortList() # has to be sorted
            for i in range(len(initial)):
                
                base = initial[i].value
                curVal = initial[i]
                level = 1
                raised = random.choice([True,False])
                self.lanes[-1].push(base)
                while level<(height) and raised==True:

                    temp = skipListIterator(curVal,base,self.lanes[-level])
                    level+=1
                    self.lanes[-level].push(temp)
                    curVal = self.lanes[-level].back()
                    raised = random.choice([True,False])

        # if initial is a list - using the list to work initial values into the skip list 
        elif type(initial) == list:
            # this could be done in a better way but this will work for now.
            initial.sort()
            initial = linkedList(initial)
            for i in range(len(initial)):
                
                base = initial[i].value
                curVal = initial[i]
                self.lanes[-1].push(base)
                raised = random.choice([True,False])
                level = 1 # the current level (starting with 1) the number is up to so that it can be used to move backwards through the lanes list
                while level<(height) and raised==True:
                    temp = skipListIterator(curVal,base,self.lanes[-level]) # getting the skipListIterator of the current lane to put as the element in the lane one step upwards
                    level+=1 #adding to level so it is now referring to the lane one step up
                    self.lanes[-level].push(temp)
                    curVal = self.lanes[-level].back()
                    raised = random.choice([True,False])

    # making it so that the skip list will print in one of two formats        
    def __format__(self,format_specs):
        # printing as lists e.g
        #    [[1],
        #    [1, 2, 4],
        #    [1, 2, 3, 4, 5, 6, 7, 8]]

        if format_specs=="ll": 
            out="["
            count = 0
            for lane in self.lanes:
                out+="["
                if len(lane)>0:
                    iter = lane.begin()
                    if iter is not None:
                        
                        out+=f"{iter.val()}"
                    for i in range(lane.size()-1):
                        iter+=1
                        if (i<(lane.size()-1)):
                            out+=", "
                        if iter is not None:
                            out+=f"{iter.val()}"  
                    
                    count+=1
                out+="],\n"
            out = out[:-2]
            out+="]\n"
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
            for i in range(len(self.lanes)-1):
                vals = [" . "]*len(self.lanes[-1])
                gaps = ["   "]*len(self.lanes[-1])
                lane = self.lanes[i]
                if len(lane)>0:
                    iter = lane.begin()
                    for n in range(lane.size()):
                        v = iter.val().val()
                        num = self.lanes[-1].index(v)
                        if num!=None:
                            vals[num] = " "+str(v)+" "
                            gaps[num] = " | "
                        iter+=1

                out+="".join(vals)+"\n"
                out+="".join(gaps)+"\n"

            out+=f"{self.lanes[-1]}\n"
            return out
            
            # go through each lane and make two lists the same width as len(base) one populated with dots and the other with spaces
            # go through every value from the lane and find the index it is in base, replace that index in the dots list with the value, and that index in the spaces list with a pipe
            # print the two lists joined with no gaps ""
            # repeat except for base, with base just print the joined version of base

    # currently adding twice to base (in wrong spot) then adding none to upper lane
    def add(self,val):
        place = self.laneSearch(val,(self.size_-1)) # currently an iter to base (or none if the val is greater than all current values)
        if place is None:
            self.lanes[-1].push(val)
        else:
            self.lanes[-1].insert(val,place) #insert the value into the base (place is the issue TwT)
            temp = place-1

        # need to then escalate it up (need to write a search algorithm to find it's place in each upper level)
        # need a node of the element in base to make the raised skipListIterator
        tempIndex = self.lanes[-1].index(val) # this will find the first instance of val (which will always be the new node as it's always inserting into the iterator at the first instance of the number therefore becoming the first instance)
        curNode = self.lanes[-1][tempIndex] 
        level = 2
        raised = random.choice([True,False])
        while level<=self.size_ and raised == True:
            
            laneIter = self.laneSearch(val,(self.size_-level))
            temp = skipListIterator(curNode,val,self.lanes[-(level)])

            
            if laneIter == None:
                self.lanes[-level].push(temp)
                curNode = self.lanes[-level].back()
            else:
                self.lanes[-level].insert(temp,laneIter)
                curNode = laneIter.getNode()
            level+=1
            raised = random.choice([True,False])

    # REWRITE THIS!!!!!!!!!
    # will return the iter of the first instance of val or the element higher than it and will throw an error if laneNum out of range and will return None if val should be at the end
    def laneSearch(self,val,laneNum): # here laneNum starts at 0 -> lane 0 (like the list structure)
        if laneNum>= self.size_: # if the lane is out of bounds it can't have a position therefore returns None
            raise Exception("laneNum out of range")
        base = False
        if laneNum == (self.size_-1): # if lane is base (wrong)
            base = True
        iter = self.lanes[laneNum].begin()
        temp = iter.val() # listIterator of a skipListIterator
        if not base:
            temp = temp.val()
        if val<temp:
            return self.lanes[laneNum].begin()
        temp2 = self.lanes[laneNum].end().val()
        if not base:
            temp2 = temp2.val()
        if val>temp2:
            return None # returns none if val greater than the last value of the lane (basically as a flag to show it needs to be pushed not inserted)
        for i in range(self.lanes[laneNum].size()):
            temp3 = iter.val()
            if not base:
                temp3 = temp3.val()
            if temp3 == val:
                return iter
            elif temp3>val:
                return iter
            iter+=1
        return None

    # sort of works but need to fix it so that it actually only deletes the connected ones from the upper lanes (make new skip list iterators and search with them?)
    def delete(self,val):
        self.lanes[-1].delete(val)
        laneIndex = self.size_-2
        found = True
        while laneIndex>=0 and found == True:
            lane = self.lanes[laneIndex]
            iter = lane.begin()
            found = False
            for i in range(len(lane)):
                if iter.val().val() == val:
                    self.lanes[laneIndex].delete(iter.val())
                    found = True
                    break
                iter+=1
            laneIndex-=1

    # base algo (original with singly linked list) returns the listIterator to the base that either points to the first instance of the value or the value directly above it .: can just add to base at the place iter that has been returned)
    def search(self,val):
        if val<self.front().value:
            return self.base().begin()
        if val>self.back().value:
            return None # needs to not return the last value as insert doesn't work at the last value so it needs a special return to show that it needs to be pushed instead
        lane = 0
        while lane < self.size_:
            if len(self.lanes[lane])==0:
                lane+=1
                continue
            temp = self.lanes[lane].begin()
            return self.searchRec(temp,temp,lane,val,True)

    
    # uses a recursive method to search the skip list (standard singly linked list algorithm)
    def searchRec(self,curIter,oldIter,lane,val,same):
        curVal = curIter.val()
        if lane<(self.size_-1):
            curVal = curVal.val()
        if val == curVal:
            if lane == (self.size_-1):
                return curIter
            elif not same:
                temp = listIterator(oldIter.val().getNode(),self.lanes[lane+1])
                a = self.searchRec(temp,temp,lane+1,val,True)
                return a
            else:
                a = self.searchRec(self.lanes[lane+1].begin(),self.lanes[lane+1].begin(),lane+1,val,True)
                return a
        elif curVal > val:
            if lane == (self.size_-1):
                return curIter
            elif same:
                a = self.searchRec(self.lanes[lane+1].begin(),self.lanes[lane+1].begin(),lane+1,val,True)
                return a
            else:
                temp = listIterator(oldIter.val().getNode(),self.lanes[lane+1])
                a = self.searchRec(temp,temp,lane+1,val,True)
                return a
        else:
            if curIter.getNode().Next != None:
                temp = curIter
                a = self.searchRec(curIter+1,temp,lane,val,False)
                return a
            else:
                temp = listIterator(curIter.val().getNode(),self.lanes[lane+1])
                a = self.searchRec(temp,temp,lane+1,val,True)
                return a
            

    # if its a valid lane, returns the whole linked list
    def getLane(self,lane):
        if lane>=self.size_:
            return linkedList([])
        else:
            return self.lanes[lane]
    
    # if its a valid, returns the size of the lane otherwise returns 0
    def sizeOfLane(self,lane):
        return self.getLane(lane).size()
    
    # returns the number of elements in the base list
    def numElements(self):
        return self.base().size()
    
    # returns the base linked list
    def base(self):
        return self.lanes[-1]
        
    # returns true id the skip list is emtpy
    def empty(self):
        return self.numElements()==0
    
    # dunder method to make len(skipList) work
    def __len__(self):
        return self.base().size()             

    # converts skip list to list based off linked list method
    def convertToList(self):
        return self.base().convertToList()
    
    # returns the first node of the base
    def front(self):
        return self.base().front()
    
    # returns the last node of the base
    def back(self):
        return self.base().back()
    
    # dunder method so that if val in skipList works
    def __contains__(self,val):
        a = self.search(val)
        return a.val()==val

    # pops the first node from the skip list (based off the c++ pop)
    def popFront(self):
        val = self.front()
        for i in range(self.size_):
            if self.lanes[i].front() == val:
                self.lanes[i].popFront()

    # pops the last node from the skip list (based off the c++ pop)
    def pop(self):
        val = self.back()
        for i in range(self.size_):
            if self.lanes[i].back() == val:
                self.lanes[i].pop()

    # fully reconfigures the skip list to contain more lanes, re-issuing new max heights to each element using the same initial process
    def reconfigure(self,newHeight):
        lst = self.base()
        self.lanes = []
        self.size_ = newHeight
        for i in range(newHeight):
            self.lanes.append(linkedList([]))
        for i in range(len(lst)):
            
            base = lst[i].value
            curVal = lst[i]
            level = 1
            raised = random.choice([True,False])
            self.lanes[-1].push(base)
            while level<(newHeight) and raised==True:

                temp = skipListIterator(curVal,base,self.lanes[-level])
                level+=1
                self.lanes[-level].push(temp)
                curVal = self.lanes[-level].back()
                raised = random.choice([True,False])

# iterator that will be used in the lanes of the skip list to ensure that all processes can be easlily performed (similar to the linkedListIterator but it contains one more attribute and method. The attribute is base value (the value at the base of the skip list column), and the method is used to get said vlaue)
class skipListIterator:
    def __init__(self,node: Node,value,lst:linkedList):
        self.node = node
        self.value=value
        self.list=lst

    # dunder method so that iterator+=number will correctly increment it with relation to the current lane of the skip list
    def __iadd__(self,other: int):
        for i in range(other):
            if self.node.Next!= None:
                self.node = self.node.Next
            else:
                return None
        return self
    
    # dunder method so that iterator+number will return a new iterator incremented with relation to the current lane of the skip list
    def __add__(self,other:int):
        temp = listIterator(self.node, self.list)
        for i in range(other):
            if temp.getNode().Next!= None:
                temp.node = temp.getNode().Next
            else:
                break
        return temp
    
    # dunder method such that iterator-=number will decrement the iterator with respect to the current lane of the skip list
    def __isub__(self, other: int):
        for i in range(other):
            if self.node.Prev != None:
                self.node = self.node.Prev
            else:
                return None
        return self
    
    # dunder method such that iterator-number will return a new iterator that has been decremented with respect to the current lane of the skip list
    def __sub__(self, other: int):
        temp = listIterator(self.node,self.list)
        for i in range(other):
            if temp.getNode().Prev != None:
                temp.node = temp.getNode().Prev
            else:
                break
        return temp
    
    # returns the base value at this iterator 
    def val(self):
        return self.value
    
    # gets the whole node at this iterator (like using * in c++)
    def getNode(self):
        return self.node
    
    # makes it so that when you print this iterator, it prints just the base value
    def __format__(self,format_specs):
        return f"{self.value}"
    

# testing
temp = skipList(3,[1,2,3,4,5,5,5,6])
print(f"{temp}")
print("deleting......\n")
temp.delete(5)
print(f"{temp}")