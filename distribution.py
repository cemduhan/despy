import random
import heapq
import collections
import math

class UniformDistribution():

    def __init__(self,lowest_interarrival,highest_interarrival, seed=100.99107 , mulp=42.4242, add=1001.1199 ):

        self.lowest_interarrival=lowest_interarrival
        self.highest_interarrival=highest_interarrival
        self.seed = seed
        self.mulp = mulp
        self.add = add

    def SetSeed(self, seed=873.3546):
        self.seed=seed;

    def bootstrap(self):
        #basic linear congruential generator
        inter_arrival = ((self.seed * self.mulp) + self.add) % (self.highest_interarrival - self.lowest_interarrival)
        inter_arrival = inter_arrival + self.lowest_interarrival
        self.seed = inter_arrival
        #print(self.seed, self.mulp, self.add, self.highest_interarrival, self.lowest_interarrival)
        #print(inter_arrival)
        return inter_arrival

class ExponentialDistribution():

    def __init__(self,lambda_parameter=1.3):

        self.lambda_parameter=lambda_parameter

    def SetLambda(self, lambda_parameter):
        self.lambda_parameter=lambda_parameter

    def bootstrap(self):

        r = random.random()
        inter_arrival = -(1.0/self.lambda_parameter) * math.log(r)
