#Author: Cem Karagöz - 150130066
import random
import heapq
import collections
import math
from collections import deque
import distribution as dis

def simulate():

    for block in state.blocks:
        block.setup()

    cntr=0

    #main simulation loop - grab next event off future event list and process
    while len(state.FEL)>0 and state.terminate_counter>0:


      print()
      print("--------------")
      #print("STATE:\n",state)

      cevent = heapq.heappop(state.FEL)

      state.clock=cevent[0]

      source_block = cevent[1]
      target_block = cevent[2]
      transaction = cevent[3]

      if source_block != -1:
          state.blocks[source_block].transactions.remove(transaction)
      state.blocks[target_block].enter(transaction)
      state.blocks[target_block].transactions.add(transaction)
      transaction.current_block = target_block

      cntr+=1

class Transaction:

    def __init__(self):

        self.id = next(state.genid)
        self.current_block = -1

    def __repr__(self):

        if hasattr(self,"A1"):
            return 'XN:{}(A1={})'.format(self.id,self.A1)
        else:
            return 'XN:{}'.format(self.id)

    #make this sortable - just an implementation detail
    def __lt__(self,other):

        return self.id < other.id

class UserList:

    def __init__(self):

        self.waiting_transactions = deque()

    def __repr__(self):

        s = "UserList: {}".format(self.waiting_transactions)
        return s

class StateVars:

    def __init__(self):

        self.clear()

    def clear(self):

        self.clock = 0.0
        self.terminate_counter = None # set this yourself or be sorry later
        self.FEL=[] # future event list
        #self.delay_list = []
        self.userlists= {}
        self.blocks = []
        self.genid = idgen()
        self.genblockid = idgen()


    def add_block(self,block):

        ind = len(self.blocks)
        assert(ind==block.blockno)
        self.blocks.append(block)

    def __repr__(self):

        s = "\nStateVars:\n"
        s += "   clock: {0:.4f}\n".format(self.clock)
        s += "   termn: {0: 6}\n".format(self.terminate_counter)
        s += "     FEL: {0}\n".format(str(self.FEL))
        s += "  ulists: {0}\n".format(str(self.userlists))
        s += "  queues: {0}\n".format(str(self.queues))
        s += "  blocks:\n"
        for i,block in enumerate(self.blocks):
            s += "        {0: 3}: {1}\n".format(i,block)
        return s
        s += "  termn:"+str(self.terminate_counter)+"\n"
        s += "  clock:"+str(self.clock)+"\n"


# just a utility generator to return IDs in order
def idgen():

    id=0
    while True:
        yield id
        id+=1

# this is a global object and we never replace it, just clear it
# just because I don't like using the global keyword I guess??
state=StateVars()

class Block:

    def __init__(self):

        self.blockno = next(state.genblockid)
        self.transactions = set()

    def setup(self):
        for transaction in self.transactions:
            transaction.current_block = -1
        self.transactions.clear()

    def enter(self,transaction):

        print("{:12.2f}".format(state.clock),":","transaction {:6}".format(transaction.id),"entered block {:3}".format(self.blockno),"(",type(self).__name__,")")
        return 1

    def enter_next_block(self,transaction):

        fevent = (state.clock,self.blockno,self.blockno+1,transaction)
        heapq.heappush(state.FEL,fevent)

    def __repr__(self):

        s = "[{}({}): {}]".format(type(self).__name__,self.blockno,self.transactions)
        return s

class GenerateBlock(Block):

    def __init__(self,type, lowest_interarrival=0,highest_interarrival=15, seed=100.99107 , mulp=42.4242, add=1001.1199):

        Block.__init__(self)
        self.dist = dis.Distribution.factory(type,lowest_interarrival,highest_interarrival, seed , mulp, add);


    def setup(self):
        Block.setup(self)
        self.bootstrap()

    def bootstrap(self):
        inter_arrival = self.dist.bootstrap()
        print(inter_arrival)
        #print(inter_arrival,file=self.ffs)

        fevent = (inter_arrival+state.clock,-1,self.blockno,Transaction())
        heapq.heappush(state.FEL,fevent)

    def enter(self,transaction):

        Block.enter(self,transaction)
        self.bootstrap()
        self.enter_next_block(transaction)

class TerminateBlock(Block):

    def __init__(self,decrement):

        Block.__init__(self)
        self.decrement = decrement

    def enter(self,transaction):

        Block.enter(self,transaction)

        state.terminate_counter -= self.decrement
        self.transactions.clear()

class TransferBlock(Block):

    def __init__(self,probability,target_block):

        Block.__init__(self)
        self.target_block = target_block
        self.prob=dis.Probability(probability)

    def enter(self,transaction):

        Block.enter(self,transaction)

        if self.prob.roll():

            fevent = (state.clock,self.blockno,self.target_block,transaction)
            heapq.heappush(state.FEL,fevent)

        else:

            self.enter_next_block()

class AdvanceBlock(Block):

    def __init__(self,type, lowest_interarrival=0,highest_interarrival=15, seed=100.99107 , mulp=42.4242, add=1001.1199):

        Block.__init__(self)
        self.dist = dis.Distribution.factory(type,lowest_interarrival,highest_interarrival, seed , mulp, add);

    def enter(self,transaction):

        Block.enter(self,transaction)
        advance = self.dist.bootstrap()
        print(advance)
        fevent = (state.clock+advance,self.blockno,self.blockno+1,transaction)
        heapq.heappush(state.FEL,fevent)

class LinkBlock(Block):

    def __init__(self,listname):

        Block.__init__(self)
        self.listname = listname
        state.userlists[listname]=UserList()

    def setup(self):

        Block.setup(self)
        state.userlists[self.listname].waiting_transactions.clear()

    def enter(self,transaction):

        Block.enter(self,transaction)

        state.userlists[self.listname].waiting_transactions.append(transaction)

class UnlinkBlock(object):
    def factory(type):
        if type == "FIFO":
            Unlink = UnlinkBlockFIFO()
            return Unlink

        if type == "LIFO":
            Unlink = UnlinkBlockLIFO()
            return Unlink

        assert 0, "Bad Distribution: " + type
    factory = staticmethod(factory)

class UnlinkBlockFIFO(Block):

    def __init__(self,listname,target_block,alternative_block):

        Block.__init__(self)
        self.listname = listname
        self.target_block = target_block
        self.alternative_block = alternative_block

    def enter(self,transaction):

        Block.enter(self,transaction)

        if len(state.userlists[self.listname].waiting_transactions)>0:

            unlinked_transaction = state.userlists[self.listname].waiting_transactions.popleft()

            fevent = (state.clock,unlinked_transaction.current_block,self.target_block,unlinked_transaction)
            heapq.heappush(state.FEL,fevent)

            self.enter_next_block(transaction)

        else:

            fevent = (state.clock,self.blockno,self.alternative_block,transaction)
            heapq.heappush(state.FEL,fevent)

class UnlinkBlockLIFO(Block):

    def __init__(self,listname,target_block,alternative_block):

        Block.__init__(self)
        self.listname = listname
        self.target_block = target_block
        self.alternative_block = alternative_block

    def enter(self,transaction):

        Block.enter(self,transaction)

        if len(state.userlists[self.listname].waiting_transactions)>0:

            unlinked_transaction = state.userlists[self.listname].waiting_transactions.pop()

            fevent = (state.clock,unlinked_transaction.current_block,self.target_block,unlinked_transaction)
            heapq.heappush(state.FEL,fevent)

            self.enter_next_block(transaction)

        else:

            fevent = (state.clock,self.blockno,self.alternative_block,transaction)
            heapq.heappush(state.FEL,fevent)
