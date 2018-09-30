# Author: Cem Karagöz - 150130066
import heapq
import math
from collections import deque
import distribution as dis


def simulate():
    for block in simulation.blocks:
        block.setup()

    counter = 0

    # main simulation loop - grab next event off future event list and process
    while (len(simulation.state.DEL) > 0 or len(simulation.state.FEL) > 0) and simulation.state.terminate_counter > 0:

        print("--------------------------------------------------------------------------")
        # Debugging Setting
        if simulation.debugging:
            print("simulation.state:\n", simulation.state)

        print("Normal Events")
        current_event = heapq.heappop(simulation.state.FEL)

        simulation.state.clock = current_event[0]

        source_block = current_event[1]
        target_block = current_event[2]
        transaction = current_event[3]

        if source_block != -1:
            simulation.blocks[source_block].transactions.remove(transaction)
        simulation.blocks[target_block].enter(transaction)
        simulation.blocks[target_block].transactions.add(transaction)
        transaction.current_block = target_block

        counter += 1
        if len(simulation.state.DEL) > 0:
            print("DelayList Events")
            for event in simulation.state.DEL:
                delayed_event = heapq.heappop(simulation.state.DEL)

                source_block = delayed_event[1]
                target_block = delayed_event[2]
                transaction = delayed_event[3]

                simulation.blocks[target_block].enter(transaction)
                simulation.blocks[target_block].transactions.add(transaction)
                transaction.current_block = target_block
    print("--------------------------------------------------------------------------")
    print("Simulation Finished")
    print(simulation)
    print(simulation.state)


class Transaction:

    def __init__(self):

        self.id = next(simulation.genid)
        self.current_block = -1

    def __repr__(self):

        if hasattr(self, "A1"):
            return 'XN:{}(A1={})'.format(self.id, self.A1)
        else:
            return 'XN:{}'.format(self.id)

    # make this sortable - just an implementation detail
    def __lt__(self, other):

        return self.id < other.id


class UserList:

    def __init__(self):
        self.waiting_transactions = deque()

    def __repr__(self):
        s = "UserList: {}".format(self.waiting_transactions)
        return s


class Despy:

    def __init__(self):
        self.state = StateVars()
        self.debugging = False
        self.userlists = {}
        self.listdictionary = {}
        self.blocks = []
        self.genid = idgen()
        self.genblockid = idgen()
        self.state.clear()

    def clear(self):
        self.__init__()
        self.state.clear()

    def set_terminate(self, count):
        if count <= 0:
            assert 0, "Please enter a terminate counter that is greater than 0"
        else:
            self.state.terminate_counter = count

    def debug(self, value):
        if type(value) != bool:
            assert 0, "Please a bool type value for debug"
        else:
            self.debugging=value

    def __repr__(self):
        s = "\nSimulation:\n"
        s += "  ulists: {0}\n".format(str(self.userlists))
        s += "  storages:{0}\n".format(self.listdictionary)
        s += "  blocks:\n"
        for i, block in enumerate(self.blocks):
            s += "        {0: 3}: {1}\n".format(i, block)
        return s


class StateVars:

    def __init__(self):
        self.clock = 0.0
        self.terminate_counter = None  # set this yourself or be sorry later
        self.FEL = []  # future event list
        self.DEL = []
        self.clear()

    def clear(self):
        self.clock = 0.0
        self.terminate_counter = None  # set this yourself or be sorry later
        self.FEL = []  # future event list
        self.DEL = []  # delayed event list

    def __repr__(self):
        s = "\nStateVars:\n"
        s += "   clock: {0:.4f}\n".format(self.clock)
        s += "   termn: {0: 6}\n".format(self.terminate_counter)
        s += "     FEL: {0}\n".format(str(self.FEL))
        s += "     DEL: {0}\n".format(str(self.DEL))
        return s


# just a utility generator to return IDs in order
def idgen():
    self_id = 0
    while True:
        yield self_id
        self_id += 1


# this is a global object and we never replace it, just clear it
simulation = Despy()


class Block:

    def __init__(self):
        self.blockno = next(simulation.genblockid)
        self.transactions = set()

        ind = len(simulation.blocks)
        assert (ind == self.blockno)
        simulation.blocks.append(self)

    def setup(self):
        for transaction in self.transactions:
            transaction.current_block = -1
        self.transactions.clear()

    def enter(self, transaction):
        print("Time:{:12.2f}".format(simulation.state.clock), "|", "Transaction Id {:6}".format(transaction.id), "|",
              "Block No {:3}".format(self.blockno), "(", type(self).__name__, ")")
        return 1

    def enter_next_block(self, transaction):
        fevent = (simulation.state.clock, self.blockno, self.blockno + 1, transaction)
        heapq.heappush(simulation.state.FEL, fevent)

    def __repr__(self):
        s = "[{}({}): {}]".format(type(self).__name__, self.blockno, self.transactions)
        return s


class GenerateBlock(Block):

    def __init__(self, variety='Uniform', lowest_interarrival=1, highest_interarrival=15, seed=100.99107, mulp=42.4242,
                 add=1001.1199):

        Block.__init__(self)
        self.dist = dis.Distribution.factory(variety, lowest_interarrival, highest_interarrival, seed, mulp, add)
        self.variety = variety
        if (self.variety == 'NoDelay') and (lowest_interarrival > 0):
            self.limit = math.floor(lowest_interarrival)
        elif (self.variety == 'NoDelay') and (lowest_interarrival <= 0):
            assert 0, "Bad Limit Value: " + str(math.floor(lowest_interarrival)) + " Should be greater than 0"

    def setup(self):
        Block.setup(self)
        self.bootstrap()

    def bootstrap(self):

        if self.variety == 'NoDelay':
            self.limit -= 1

        inter_arrival = self.dist.bootstrap()
        # Debugging Setting
        if simulation.debugging:
            print("Transaction Generation Time:", inter_arrival)

        fevent = (inter_arrival + simulation.state.clock, -1, self.blockno, Transaction())
        heapq.heappush(simulation.state.FEL, fevent)

    def enter(self, transaction):

        Block.enter(self, transaction)
        if (self.variety == 'NoDelay') and (self.limit <= 0):
            self.enter_next_block(transaction)
            return

        self.bootstrap()
        self.enter_next_block(transaction)


class TerminateBlock(Block):

    def __init__(self, decrement):

        Block.__init__(self)
        self.decrement = decrement
        if self.decrement < 0:
            assert 0, "Bad Decrement Value: " + str(self.decrement) + "Should be between greater than 0"

    def enter(self, transaction):

        Block.enter(self, transaction)

        # Debugging Setting
        if simulation.debugging:
            print("Transaction", transaction.id,
                  "Terminated with value of", self.decrement,
                  "at Block No:", self.blockno)

        simulation.state.terminate_counter -= self.decrement
        self.transactions.clear()


class TransferBlock(Block):

    def __init__(self, probability, target_block):

        Block.__init__(self)
        self.target_block = target_block
        self.prob = dis.Probability(probability / 100)

    def enter(self, transaction):

        Block.enter(self, transaction)

        if self.prob.roll():
            # Debugging Setting
            if simulation.debugging:
                print("Transaction", transaction.id, "Passed Moving To Block", self.target_block)

            fevent = (simulation.state.clock, self.blockno, self.target_block, transaction)
            heapq.heappush(simulation.state.FEL, fevent)

        else:
            # Debugging Setting
            if simulation.debugging:
                print(transaction.id, "Failed to pass so")
            self.enter_next_block(transaction)


class AdvanceBlock(Block):

    def __init__(self, variety, lowest_interarrival=0, highest_interarrival=15, seed=100.99107, mulp=42.4242,
                 add=1001.1199):
        Block.__init__(self)
        self.dist = dis.Distribution.factory(variety, lowest_interarrival, highest_interarrival, seed, mulp, add)

    def enter(self, transaction):
        Block.enter(self, transaction)
        advance = self.dist.bootstrap()

        # Debugging Setting
        if simulation.debugging:
            print("Transaction:", transaction.id, "Moving to Block: ", self.blockno + 1, "With Delay of", advance)

        fevent = (simulation.state.clock + advance, self.blockno, self.blockno + 1, transaction)
        heapq.heappush(simulation.state.FEL, fevent)


class LinkBlock(Block):

    def __init__(self, listname):
        Block.__init__(self)
        self.listname = listname
        simulation.state.userlists[listname] = UserList()

    def setup(self):
        Block.setup(self)
        simulation.state.userlists[self.listname].waiting_transactions.clear()

    def enter(self, transaction):
        Block.enter(self, transaction)

        simulation.state.userlists[self.listname].waiting_transactions.append(transaction)

        # Debugging Setting
        if simulation.debugging:
            print("Transaction", transaction.id, "Is Attached to", self.listname)


class UnlinkBlock(object):
    def factory(variety, listname, target_block, alternative_block):
        if variety == "FIFO":
            unlink = UnlinkBlockFIFO(listname, target_block, alternative_block)
            return unlink

        if variety == "LIFO":
            unlink = UnlinkBlockLIFO(listname, target_block, alternative_block)
            return unlink

        assert 0, "Bad Distribution: " + variety

    factory = staticmethod(factory)


class UnlinkBlockFIFO(Block):

    def __init__(self, listname, target_block, alternative_block):

        Block.__init__(self)
        self.listname = listname
        self.target_block = target_block
        self.alternative_block = alternative_block

    def enter(self, transaction):

        Block.enter(self, transaction)

        if len(simulation.state.userlists[self.listname].waiting_transactions) > 0:

            unlinked_transaction = simulation.state.userlists[self.listname].waiting_transactions.popleft()

            # Debugging Setting
            if simulation.debugging:
                print("Transaction", transaction.id, "Unlinked the Transaction", unlinked_transaction.id, "From:",
                      self.listname, "Moving to Block:", self.target_block)

            fevent = (simulation.state.clock, unlinked_transaction.current_block, self.target_block, unlinked_transaction)
            heapq.heappush(simulation.state.FEL, fevent)

            self.enter_next_block(transaction)

        else:

            # Debugging Setting
            if simulation.debugging:
                print(transaction.id, "Could not unlink anything from the list moving to block:",
                      self.alternative_block)

            fevent = (simulation.state.clock, self.blockno, self.alternative_block, transaction)
            heapq.heappush(simulation.state.FEL, fevent)


class UnlinkBlockLIFO(Block):

    def __init__(self, listname, target_block, alternative_block):

        Block.__init__(self)
        self.listname = listname
        self.target_block = target_block
        self.alternative_block = alternative_block

    def enter(self, transaction):

        Block.enter(self, transaction)

        if len(simulation.state.userlists[self.listname].waiting_transactions) > 0:

            unlinked_transaction = simulation.state.userlists[self.listname].waiting_transactions.pop()

            # Debugging Setting
            if simulation.debugging:
                print(transaction.id, "Unlinked the", unlinked_transaction.id, "From:", self.listname, "Moving to:",
                      self.target_block)

            fevent = (simulation.state.clock, unlinked_transaction.current_block, self.target_block, unlinked_transaction)
            heapq.heappush(simulation.state.FEL, fevent)

            self.enter_next_block(transaction)

        else:

            # Debugging Setting
            if simulation.debugging:
                print(transaction.id, "Could not unlink anything from the list moving to block:",
                      self.alternative_block)

            fevent = (simulation.state.clock, self.blockno, self.alternative_block, transaction)
            heapq.heappush(simulation.state.FEL, fevent)


class EnterBlock(Block):

    def __init__(self, listname, limit):
        self.limit = limit
        self.listname = listname
        Block.__init__(self)
        if self.limit <= 0:
            assert 0, "Bad Que Size Value: " + str(self.limit) + " Should be greater than 0"

    def enter(self, transaction):

        if simulation.listdictionary[self.listname].enter(self.limit):

            Block.enter(self, transaction)
            # Debugging Setting
            if simulation.debugging:
                print("Transaction:", transaction.id,
                      "Entered", self.listname,
                      "at", simulation.state.clock,
                      "Capacity Left Is ", simulation.listdictionary[self.listname].size_left())

            fevent = (simulation.state.clock, self.blockno, self.blockno + 1, transaction)
            heapq.heappush(simulation.state.FEL, fevent)

        else:

            delayedevent = (simulation.state.clock, self.blockno - 1, self.blockno, transaction)
            simulation.state.DEL.append(delayedevent)
            # Debugging Setting
            if simulation.debugging:
                print("Transaction:", transaction.id, "Couldn't enter there is no capacity at:", self.listname)


class LeaveBlock(Block):

    def __init__(self, listname, limit=0):
        self.limit = limit
        Block.__init__(self)
        if self.limit < 0:
            assert 0, "Bad Limit Value: " + str(self.limit) + " Should be greater than 0"
        self.listname = listname

    def enter(self, transaction):
        Block.enter(self, transaction)
        # Debugging Setting
        if simulation.debugging:
            print("Transaction:", transaction.id, "Left", self.listname)

        fevent = (simulation.state.clock, self.blockno, self.blockno + 1, transaction)
        heapq.heappush(simulation.state.FEL, fevent)
        simulation.listdictionary[self.listname].leave(self.limit)


class Storage():

    def __repr__(self):
        s = "[Limit:{} : Left:{}]".format(self.limit, self.left)
        return s

    def __init__(self, listname, storage):
        self.listname = listname
        self.left = storage
        self.limit = storage
        simulation.listdictionary[self.listname] = self

    def size_left(self):
        return self.left

    def dec_limit(self, storage):
        self.left = self.left - storage

        if self.left < 0:
            self.left = 0

    def inc_limit(self, storage):
        self.left = self.left + storage

        if self.left > self.limit:
            self.left = 0

    def enter(self, storage):
        if self.check_availability(storage):
            self.dec_limit(storage)
            return True
        else:
            return False

    def check_availability(self, storage):
        if self.left >= storage:
            return True
        else:
            return False

    def leave(self, storage):
        self.inc_limit(storage)
        return True
