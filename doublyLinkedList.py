# Node class to make the nodes that make up the doubly linked list (therefore need to store both the previous and future nodes)
class Node:
    # Node constructor that allows for a node to be created without a previous or next
    def __init__(self, value, Prev, Next):
        self.value = value
        self.Prev = None
        self.Next= None
        if (Prev!=None):
            self.Prev = Prev
        if (Next!=None):
            self.Next = Next

    # set the previous node 
    def setPrev(self,Prev):
        self.Prev = Prev

    # set the node's value (the node must always have a value but this allows it to be changed)
    def setVal(self,val):
        self.value = val

    # set the next node
    def setNext(self,Next):
        self.Next = Next

    # make it so that when a node is used in an f-string it will only use it's value (for readability)
    def __format__(self,format_specs):
        return f"{self.value}"
    
    def __lt__(self,other):
        return str(self.value) < str(other.value)
    
    def __gt__(self,other):
        return str(self.value) > str(other.value)
    
    def __le__(self,other):
        return str(self.value)<=str(other.value)
    
    def __ge__(self,other):
        return str(self.value)>=str(other.value)
    

# Class to actually make the linked list and all it's methods
class linkedList:
    # constructor method that allows an initial list to be passed in to instantiate values
    def __init__(self, initial: list):
        self.size_ = 0 # stores the length of the list
        self.head = None # the head of the list starts at None but will be assigned a Node when nodes are added

        if len(initial)>0: # going through and pushing all values fron the initializing list
            for val in initial:
                self.push(val)

    # pushes a value to the front of the list
    def pushFront(self,value):
        temp = Node(value,None,self.head)
        self.head = temp
        self.size_+=1

    # pushes a value to the end of the list
    def push(self,value):
        if (self.size_>0):
            iter = self.end()
            curNode = iter.getNode()
            
            temp = Node(value,curNode,None)
            curNode.setNext(temp)
        else:
            temp = Node(value,None,None)
            self.head = temp
        self.size_+=1

    # dunder method so that list[index] will return the node at that position also facilitates for x in list
    def __getitem__(self,index):
        if index > self.size_:
            return None
        iter = self.begin()+(index) 
        return iter.getNode()
    
    # dunder methat so that writing list[index] = value will actually change the value of the node at that position
    def __setitem__(self,index,val):
        iter = self.begin()+(index) 
        iter.getNode().setVal(val)

    # pops the first node out of the list (moves the head down by one value)
    def popFront(self):
        self.head = self.head.Next
        self.size_-=1

    # pops the last value from the list (changes the second last node to go to None instead of the next node)
    def pop(self):
        secondLast = self.end()-1
        secondLast.getNode().setNext(None)
        self.size_-=1

    # insert a value into the list at a specific positon (given either an index value or a list iterator) -- cannot insert to the end (pushes back the value currently in that spot)
    def insert(self,value,pos):
        tempNode = None
        if type(pos) == int:
            tempNode = self.__getitem__(pos)
        elif type(pos) == listIterator:
            tempNode = pos.getNode()
        else:
            raise Exception("pos needs to be an int or listIterator")

        try:
            prevNode = tempNode.Prev
            newNode = Node(value,prevNode,tempNode)
            tempNode.setPrev(newNode)
            if prevNode != None:
                prevNode.setNext(newNode)
            else:
                self.head = newNode
            self.size_+=1       
        except:
            print("There was an error inserting")

    # returns the node at the front of the list
    def front(self):
        return self.head
    
    # returns the node at the end of the list
    def back(self):
        return self.end().getNode()

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
        return listIterator(self.head,self)
    
    # will return an iterator that points to the last node
    def end(self):
        return listIterator(self.head,self)+(self.size_)
    
    # given an iterator for the destination of the data (within the current list), an iterator that points to where the data should come from and the number of elements to be moved, this method will transfer the nodes to directly after the destination node cutting them from where they originally were
    def splice(self,dest, source, length):
        # if no length is entered it is autoatically set to 1
        if length == None:
            length = 1
        # connecting the front of the splice section to the destination
        if self.size_==0:
            self.head = source.getNode()
            source.getNode().setPrev(None)
            end = source+length
            end.getNode().setNext(None)
            # end.getNode().Next.setPrev(end.getNode())
        else:
            dest.getNode().setNext(source.getNode())
            source.getNode().setPrev(dest.getNode())

            # if dest isn't the last value in the list, the end of the splice section is connected to it
            tempEnd = dest.getNode().Next
            if tempEnd!=None:
                end = source+length
                end.getNode().setNext(tempEnd)
                end.getNode().Next.setPrev(end.getNode())
        

        # disconnecting  the spliced section from it's original place
        sourceEnd = (source+length).getNode().Next
        if source.list.head == source.getNode():
            source.list.head = (source+length).getNode().Next
            if sourceEnd!=None:
                sourceEnd.setPrev(None)
        else:
            sourcePrev = source.getNode().Prev
            sourcePrev.setNext(sourceEnd)
            sourceEnd.setPrev(sourcePrev)

        # updating the sizes of the lists that were affected
        dest.list.size_+=length
        source.list.size_-=length

    # deletes the first instance of a value from the list
    def delete(self,value):
        iter = self.begin()
        for i in range(self.size_):
            if iter.val() == value:
                if iter.getNode().Prev != None:
                    prev = iter.getNode().Prev
                    prev.setNext(iter.getNode().Next)
                if iter.getNode().Next != None:
                    next = iter.getNode().Next
                    next.setPrev(iter.getNode().Prev)
                self.size_-=1
                break
            iter+=1

    # bubble sort bc I said so
    def sortList(self):
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
    
    def convertToList(self):
        temp = []
        iter = self.begin()
        for i in range(self.size_):
            temp.append(iter.val())
            iter+=1
        return temp
    
class listIterator:
    # constructor method for pointer/iterator that requires a starting node and the list it should be part of
    def __init__(self, node: Node, lst: linkedList):
        self.node = node
        self.list = lst

    # dunder method so that iterator+=number will correctly increment it with relation to the list
    def __iadd__(self,other: int):
        for i in range(other):
            if self.node.Next!= None:
                self.node = self.node.Next
            else:
                return None
        return self

    # dunder method so that iterator+number will return a new iterator incremented with relation to the list
    def __add__(self,other:int):
        temp = listIterator(self.node, self.list)
        for i in range(other):
            if temp.getNode().Next!= None:
                temp.node = temp.getNode().Next
            else:
                break
        return temp
    
    # dunder method such that iterator-=number will decrement the iterator with respect to the list
    def __isub__(self, other: int):
        for i in range(other):
            if self.node.Prev != None:
                self.node = self.node.Prev
            else:
                return None
        return self

    # dunder method such that iterator-number will return a new iterator that has been decremented with respect to the list
    def __sub__(self, other: int):
        temp = listIterator(self.node,self.list)
        for i in range(other):
            if temp.getNode().Prev != None:
                temp.node = temp.getNode().Prev
            else:
                break
        return temp
    
    # returns the value of the iterator's node
    def val(self): 
        return self.node.value
    
    # returns the iterator's node
    def getNode(self):
        return self.node
    
    # dunder method such that f"{listIterator}" will show the value of the node
    def __format__(self,format_specs):
        return f"{self.node.value}"
    