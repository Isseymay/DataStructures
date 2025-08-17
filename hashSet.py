import copy
from doublyLinkedList import linkedList,listIterator

sizes = [1,13,59,127,257,541,1109,2357,5087,10273,20753,42043,85229,172993,351061,712697,1447153,2938679]

class hashSet:
    def __init__(self,initial):
        self.buckets = [None]
        self.keys = None
        self.maxLoadFactor_ = 2
        self.numBucketsPos = 0

        if len(initial) >0:
            for val in initial:
                self.insert(val)

    def bucket(self,value):
        hashed = hash(value)
        return hashed%len(self.buckets)
    
    def begin(self):
        return self.keys.begin()
    
    def end(self):
        return self.keys.end()
    
    def __format__(self,format_specs):
        if format_specs=="ll":
            return f"{self.keys}"
        elif format_specs=="b":
            out = "["
            for i in self.buckets:
                out+=f"{i}, "
            out=out[:-2]
            out+=f"]\n"
            return out
        else:
            out = ""
            for i in range(len(self.buckets)):
                out+=f"{i}: "
                iter = copy.copy(self.buckets[i])
                while iter!= None and self.bucket(iter.val())==i:
                    out+=f"{iter.getNode()}, "
                    iter += 1
                out+="\n"
            out+="\n"
            return out
        
    def insert(self,value):
        if self.keys == None:
            self.keys = linkedList([])
        if value not in self.keys:
            hashed = self.bucket(value)
            if self.buckets[hashed] == None:
                self.keys.push(value)
                self.buckets[hashed] = self.keys.end()
            else:
                self.keys.insert(value,self.buckets[hashed])
            if self.loadFactor() > self.maxLoadFactor_:
                self.rehash(len(self.buckets))

    def loadFactor(self):
        return len(self.keys)/len(self.buckets)

    def maxLoadFactor(self):
        return self.maxLoadFactor_
    
    def setMaxLoad(self,value):
        self.maxLoadFactor_ = value
        if self.loadFactor()> self.maxLoadFactor_:
            self.rehash(len(self.buckets))

    def size(self):
        return self.keys.size()
    
    def empty(self):
        return self.keys.size() == 0
    
    def bucketCount(self):
        return len(self.buckets)
    
    def bucketSize(self,pos):
        if pos<len(self.buckets):
            iter = self.buckets[pos]
            count = 0
            ogHash = self.bucket(iter.val())
            while iter.getNode().Next != None:
                if self.bucket(iter.val()) != ogHash:
                    break
                count+=1
                iter+=1
            if iter.getNode().Next == None:
                if self.bucket(iter.val()) == ogHash:
                    count+=1
            return count
        return 0
    
    # returns a boolean of if the value is in the hashset (allows if val in hashset:)
    def __contains__(self,value):
        hashed = self.bucket(value)
        iter = self.buckets[hashed]
        while iter.getNode().Next != None:
            if iter.val() == value:
                return True
            
            if self.bucket(iter.val()) != hashed:
                break

            iter+=1

        if iter.getNode().Next == None and iter.val() == value:
            return True
        return False
    
    # will return the list iterator for the value or none if not found
    def find(self,value):
        hashed = self.bucket(value)
        iter = self.buckets[hashed]
        while iter.getNode().Next != None:
            if iter.val() == value:
                return iter
            
            if self.bucket(iter.val()) != hashed:
                break

            iter+=1

        if iter.getNode().Next == None and iter.val() == value:
            return iter
        return None
    
    def erase(self,val):
        value = None
        if type(val) == int:
            value = val
        elif type(val) == listIterator:
            value = val.val()

        self.keys.delete(value)

    def rehash(self,newSize):
        if newSize>len(self.buckets) or self.loadFactor()>self.maxLoadFactor_:
            curSize = len(self.buckets)
            curLoad = self.loadFactor()
            for i in range(self.numBucketsPos+1, len(sizes)):
                curSize = sizes[i]
                curLoad = len(self.keys)/curSize
                if curSize>=newSize and curLoad<=self.maxLoadFactor_:
                    break

            self.numBucketsPos = i
            self.buckets = [None] * curSize

            self.splicing()

    def splicing(self):
        temp = linkedList([])
        temp.splice(temp.begin(),self.keys.begin(),self.keys.size())
        length = temp.size()
        cur = temp.begin()
        old = temp.begin()
        for i in range(length):
            key = cur.val()
            hashed = self.bucket(key)
            dest = self.buckets[hashed]
            old+=1
            if dest!=None:
                self.keys.splice(dest,temp,cur)
                self.buckets[hashed] = dest-1
            else:
                self.keys.push(key)
                self.buckets[hashed] = self.keys.end()
            cur = copy.copy(old)

