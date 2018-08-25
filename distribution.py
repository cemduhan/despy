import random
import heapq
import collections
import math

class Distribution(object):
    def factory(type, lowest_interarrival, highest_interarrival, seed, mulp, add):
        if type == "Uniform":
            Dist = UniformDistribution()
            Dist.SetVariables(lowest_interarrival,highest_interarrival, seed, mulp, add)
            return Dist

        if type == "Exponential":
            Dist = ExponentialDistribution()
            Dist.SetVariables(lowest_interarrival, highest_interarrival, seed)
            return Dist

        if type == "Empirical":
            Dist = EmpiricalDistribution()
            Dist.SetVariables(lowest_interarrival)
            return Dist

        if type == "NoDelay":
            Dist = NoDelayDistribution()
            return Dist

        assert 0, "Bad Distribution: " + type
    factory = staticmethod(factory)

class UniformDistribution(Distribution):

    def __init__(self):
        self.lowest_interarrival = 0
        self.highest_interarrival = 15
        self.seed = 100.99107
        self.mulp = 42.4242
        self.add = 1001.1199

    def CheckValues(self):
        if self.lowest_interarrival < 0:
            assert 0, "Bad Lowest Interarrival Value: " + str(self.lowest_interarrival) + "Should be between greater than 0"

        if self.highest_interarrival < 0 or self.highest_interarrival < self.lowest_interarrival:
            assert 0, "Bad Highest Interarrival Value: " + str(self.lowest_interarrival) + "Should be between greater than 0 and Lowest Interarrival"

        if self.seed < 0:
            assert 0, "Bad Seed Value: " + str(self.seed) + "Should be between greater than 0"

        if self.mulp < 0:
            assert 0, "Bad M Value: " + str(self.mulp) + "Should be between greater than 0"

        if self.add < 0:
            assert 0, "Bad Addative Value: " + str(self.add) + "Should be between greater than 0"

    def SetVariables(self, lowest_interarrival=0, highest_interarrival=15, seed=100.99107, mulp=42.4242, add=1001.1199):
        self.lowest_interarrival = lowest_interarrival
        self.highest_interarrival = highest_interarrival
        self.seed = seed
        self.mulp = mulp
        self.add = add

    def bootstrap(self):
        #basic linear congruential generator
        if self.highest_interarrival - self.lowest_interarrival == 0:
            return self.highest_interarrival

        inter_arrival = ((self.seed * self.mulp) + self.add) % (self.highest_interarrival - self.lowest_interarrival)
        inter_arrival = inter_arrival + self.lowest_interarrival
        #print(self.seed)
        self.seed = inter_arrival
        #print(self.seed, self.mulp, self.add, self.highest_interarrival, self.lowest_interarrival)
        #print(inter_arrival)
        return inter_arrival

class ExponentialDistribution(Distribution):

    def __init__(self):
        self.lowest_interarrival = 0
        self.highest_interarrival = 15
        self.lambda_parameter = 1.3

    def CheckValues(self):
        if self.lowest_interarrival < 0:
            assert 0, "Bad Lowest Interarrival Value: " + str(self.lowest_interarrival) + "Should be between greater than 0"

        if self.highest_interarrival < 0 or self.highest_interarrival < self.lowest_interarrival:
            assert 0, "Bad Highest Interarrival Value: " + str(self.lowest_interarrival) + "Should be between bigger than 0 and Lowest Interarrival"

        if self.lambda_parameter < 0:
            assert 0, "Bad Lambda Value: " + str(self.lambda_parameter) + "Should be between greater than 0"

    def SetVariables(self, lowest_interarrival=0, highest_interarrival=15, lambda_parameter=1.3):
        self.lowest_interarrival = lowest_interarrival
        self.highest_interarrival = highest_interarrival
        self.lambda_parameter = lambda_parameter
        self.CheckValues()

    def bootstrap(self):
        r = random.random()
        inter_arrival = -(1.0/self.lambda_parameter) * math.log(r)#% (self.highest_interarrival - self.lowest_interarrival)
        #inter_arrival = inter_arrival + self.lowest_interarrival
        self.lambda_parameter=inter_arrival
        return inter_arrival

class EmpiricalDistribution(Distribution):

    def __init__(self):
        self.filename = None
        self.interpolation = False

    def CheckValues(self):
        if not(isinstance(self.filename, str)):
            assert 0, "Bad Variable Type: " + type(self.filename) + "Should be string"

        if not(isinstance(self.interpolation, bool)):
            assert 0, "Bad Variable Type: " + type(self.interpolation) + "Should be bool"

    def SetVariables(self, filename=None, interpolation=False):
        self.filename = filename
        self.interpolation = interpolation
        self.setupDisturbution()
        self.CheckValues()

    def bootstrap(self):

        roll = self.lenght * random.random()
        floor = int(math.floor(roll))
        roof = floor + 1

        if self.interpolation:
            inter_arrival = float(self.content[roof] * self.content[floor]) * (roll - floor)
            return inter_arrival
        else:
            inter_arrival = float(self.content[floor])
            return inter_arrival

    def setupDisturbution(self):
        try:
            with open(self.filename) as file:
                self.content = file.readlines()
            self.content = [x.strip() for x in self.content]
            self.lenght = len(self.content)
        except (RuntimeError, TypeError, NameError):
            print("No such file or directory:" + self.filename)


class NoDelayDistribution(Distribution):

    def __init__(self):
        self.delay = None

    def bootstrap(self):

        return 0.0

class Probability():

    def __init__(self, probability = 0.5):
        self.chance = probability
        self.CheckValues()

    def CheckValues(self):
        if self.chance > 1 or self.chance < 0:
            assert 0, "Bad Probability Value: " + str(self.chance* 100) + "Should be between 0 and 100"

    def SetSeed(self, seed=76845326783425):#not recommended but avalible
        random.seed(seed)

    def SetChance(self, probability=0.5):
        self.probability=probability


    def roll(self):

        r = random.random()
        if self.chance >= r:
            return True
        else:
            return False
