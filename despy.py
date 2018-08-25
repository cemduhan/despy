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

    cntr = 0

    #main simulation loop - grab next event off future event list and process
    while len(state.DEL) > 0 or len(state.FEL) > 0 and state.terminate_counter > 0:



        print("--------------------------------------------------------------------------")
        #Debugging Setting
        if state.debugging:
            print("STATE:\n",state)

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

        cntr += 1

    print("--------------------------------------------------------------------------")

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
        self.debugging = False
        self.terminate_counter = None # set this yourself or be sorry later
        self.FEL=[] # future event list
        self.DEL = []
        self.userlists = {}
        self.enterlists = {}
        self.enterptrs = {}
        self.enterlists_sizes = {}
        self.blocks = []
        self.genid = idgen()
        self.genblockid = idgen()


    def add_block(self,block):

        ind = len(self.blocks)
        assert(ind == block.blockno)
        self.blocks.append(block)

    def __repr__(self):

        s = "\nStateVars:\n"
        s += "   clock: {0:.4f}\n".format(self.clock)
        s += "   termn: {0: 6}\n".format(self.terminate_counter)
        s += "     FEL: {0}\n".format(str(self.FEL))
        s += "     DEL: {0}\n".format(str(self.DEL))
        s += "  ulists: {0}\n".format(str(self.userlists))
        s += "  dlists: {0}\n".format(str(self.enterlists))
        #s += "  queues: {0}\n".format(str(self.queues))
        s += "  blocks:\n"
        for i,block in enumerate(self.blocks):
            s += "        {0: 3}: {1}\n".format(i,block)
        return s
        s += "  termn:"+str(self.terminate_counter)+"\n"
        s += "  clock:"+str(self.clock)+"\n"


# just a utility generator to return IDs in order
def idgen():

    id = 0
    while True:
        yield id
        id += 1

# this is a global object and we never replace it, just clear it
# just because I don't like using the global keyword I guess??
state  = StateVars()

class Block:

    def __init__(self):

        self.blockno = next(state.genblockid)
        self.transactions = set()

    def setup(self):
        for transaction in self.transactions:
            transaction.current_block = -1
        self.transactions.clear()

    def enter(self,transaction):

        print("Time:{:12.2f}".format(state.clock), "|", "Transaction Id {:6}".format(transaction.id), "|", "Block No {:3}".format(self.blockno), "(", type(self).__name__, ")")
        return 1

    def enter_next_block(self, transaction):

        fevent = (state.clock, self.blockno,self.blockno+1, transaction)
        heapq.heappush(state.FEL, fevent)

    def __repr__(self):

        s = "[{}({}): {}]".format(type(self).__name__, self.blockno, self.transactions)
        return s

class GenerateBlock(Block):

    def __init__(self, type= 'Uniform', lowest_interarrival = 1, highest_interarrival = 15, seed = 100.99107, mulp = 42.4242, add = 1001.1199):

        Block.__init__(self)
        self.dist = dis.Distribution.factory(type, lowest_interarrival, highest_interarrival, seed, mulp, add)
        self.type = type
        if (self.type == 'NoDelay') and (self.limit > 0):
            self.limit = math.floor(lowest_interarrival)
        elif (self.type == 'NoDelay') and (self.limit <= 0):
            assert 0, "Bad Limit Value:  " + str(math.floor(lowest_interarrival)) + "Should be greater than 0"


    def setup(self):
        Block.setup(self)
        self.bootstrap()

    def bootstrap(self):

        if (self.type == 'NoDelay') and (self.limit <= 0):
            self.limit -= 1

        inter_arrival = self.dist.bootstrap()
        #Debugging Setting
        if state.debugging:
                print("Transaction Generation Time:",inter_arrival)

        fevent = (inter_arrival+state.clock, -1, self.blockno, Transaction())
        heapq.heappush(state.FEL, fevent)

    def enter(self, transaction):

        Block.enter(self, transaction)

        if (self.type == 'NoDelay') and (self.limit <= 0):
            self.enter_next_block(transaction)
            return

        self.bootstrap()
        self.enter_next_block(transaction)

class TerminateBlock(Block):

    def __init__(self,decrement):

        Block.__init__(self)
        self.decrement = decrement

    def enter(self,transaction):

        Block.enter(self, transaction)

        #Debugging Setting
        if state.debugging:
                print("Transaction", transaction.id, "Terminated with value of", self.decrement, "at Block No:", self.blockno)

        state.terminate_counter -= self.decrement
        self.transactions.clear()

class TransferBlock(Block):

    def __init__(self,probability, target_block):

        Block.__init__(self)
        self.target_block = target_block
        self.prob = dis.Probability(probability/100)

    def enter(self, transaction):

        Block.enter(self, transaction)

        if self.prob.roll():
            #Debugging Setting
            if state.debugging:
                    print("Transaction", transaction.id, "Passed Moving To Block", self.target_block)

            fevent = (state.clock, self.blockno, self.target_block, transaction)
            heapq.heappush(state.FEL, fevent)

        else:
            #Debugging Setting
            if state.debugging:
                    print(transaction.id, "Failed to pass so")
            self.enter_next_block(transaction)

class AdvanceBlock(Block):

    def __init__(self, type, lowest_interarrival=0, highest_interarrival=15, seed=100.99107, mulp=42.4242, add=1001.1199):

        Block.__init__(self)
        self.dist = dis.Distribution.factory(type, lowest_interarrival, highest_interarrival, seed, mulp, add)

    def enter(self, transaction):

        Block.enter(self, transaction)
        advance = self.dist.bootstrap()

        #Debugging Setting
        if state.debugging:
            print("Transaction:", transaction.id, "Moving to Block: ", self.blockno+1, "With Delay of", advance)

        fevent = (state.clock+advance, self.blockno, self.blockno+1, transaction)
        heapq.heappush(state.FEL, fevent)

class LinkBlock(Block):

    def __init__(self, listname):

        Block.__init__(self)
        self.listname = listname
        state.userlists[listname] = UserList()

    def setup(self):

        Block.setup(self)
        state.userlists[self.listname].waiting_transactions.clear()

    def enter(self, transaction):

        Block.enter(self, transaction)

        state.userlists[self.listname].waiting_transactions.append(transaction)

        #Debugging Setting
        if state.debugging:
            print("Transaction", transaction.id, "Is Attached to", self.listname)

class UnlinkBlock(object):
    def factory(type, listname, target_block, alternative_block):
        if type == "FIFO":
            Unlink = UnlinkBlockFIFO(listname, target_block, alternative_block)
            return Unlink

        if type == "LIFO":
            Unlink = UnlinkBlockLIFO(listname, target_block, alternative_block)
            return Unlink

        assert 0, "Bad Distribution: " + type
    factory = staticmethod(factory)

class UnlinkBlockFIFO(Block):

    def __init__(self, listname, target_block, alternative_block):

        Block.__init__(self)
        self.listname = listname
        self.target_block = target_block
        self.alternative_block = alternative_block

    def enter(self, transaction):

        Block.enter(self, transaction)

        if len(state.userlists[self.listname].waiting_transactions)>0:

            unlinked_transaction = state.userlists[self.listname].waiting_transactions.popleft()

            #Debugging Setting
            if state.debugging:
                print("Transaction", transaction.id, "Unlinked the Transaction", unlinked_transaction.id, "From:",self.listname, "Moving to Block:", self.target_block)

            fevent = (state.clock, unlinked_transaction.current_block, self.target_block, unlinked_transaction)
            heapq.heappush(state.FEL, fevent)

            self.enter_next_block(transaction)

        else:

            #Debugging Setting
            if state.debugging:
                print(transaction.id, "Could not unlink anything from the list moving to block:", self.alternative_block)

            fevent = (state.clock, self.blockno, self.alternative_block, transaction)
            heapq.heappush(state.FEL, fevent)

class UnlinkBlockLIFO(Block):

    def __init__(self, listname, target_block, alternative_block):

        Block.__init__(self)
        self.listname = listname
        self.target_block = target_block
        self.alternative_block = alternative_block

    def enter(self, transaction):

        Block.enter(self, transaction)

        if len(state.userlists[self.listname].waiting_transactions) > 0:

            unlinked_transaction = state.userlists[self.listname].waiting_transactions.pop()

            #Debugging Setting
            if state.debugging:
                print(transaction.id, "Unlinked the", unlinked_transaction.id, "From:", self.listname, "Moving to:", self.target_block)

            fevent = (state.clock, unlinked_transaction.current_block, self.target_block, unlinked_transaction)
            heapq.heappush(state.FEL, fevent)

            self.enter_next_block(transaction)

        else:

            #Debugging Setting
            if state.debugging:
                print(transaction.id, "Could not unlink anything from the list moving to block:", self.alternative_block)

            fevent = (state.clock, self.blockno, self.alternative_block, transaction)
            heapq.heappush(state.FEL, fevent)

class EnterBlock(Block):

    def __init__(self, listname, Qsize):

        Block.__init__(self)
        self.listname = listname
        self.Qsize = Qsize
        state.enterlists[listname] = UserList()
        state.enterptrs[listname] = UserList()
        state.enterlists_sizes[listname] = 0
        state.enterptrs[listname].waiting_transactions.append(self)

    def enter(self, transaction):

        if state.enterlists_sizes[self.listname] < self.Qsize:

            Block.enter(self, transaction)
            state.enterlists_sizes[self.listname] += 1
            #Debugging Setting
            if state.debugging:
                print("Transaction:", transaction.id, "Entered", self.listname, "at", state.clock, "Capacity Left Is ", self.Qsize - state.enterlists_sizes[self.listname])

            fevent = (state.clock, self.blockno, self.blockno+1, transaction)
            heapq.heappush(state.FEL, fevent)

        else:

            devent = (state.clock, self.blockno, self.blockno, transaction)
            state.enterlists[self.listname].waiting_transactions.append(devent)
            #Debugging Setting
            if state.debugging:
                print("Transaction:", transaction.id, "Couldn't enter there is no capacity at:", self.listname)

    def check_DEL(self):

        if len(state.enterlists[self.listname].waiting_transactions) > 0 and state.enterlists_sizes[self.listname] < self.Qsize:
            devent = state.enterlists[self.listname].waiting_transactions.pop()
            transaction = devent[3]
            transaction.current_block = self.blockno
            #Debugging Setting
            if state.debugging:
                print("Transaction:", transaction, "Removed from", self.listname, "waiting list at", state.clock, "trying to enter", self.listname)
            self.enter(transaction)

class LeaveBlock(Block):

    def __init__(self, listname):

        Block.__init__(self)
        self.listname = listname

    def enter(self, transaction):

        Block.enter(self, transaction)
        state.enterlists_sizes[self.listname] -= 1
        #Debugging Setting
        if state.debugging:
            print("Transaction:", transaction.id, "Left", self.listname)

        fevent = (state.clock, self.blockno, self.blockno+1, transaction)
        heapq.heappush(state.FEL, fevent)

        state.enterptrs[self.listname].waiting_transactions[0].check_DEL()
