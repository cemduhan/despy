#an example model and experiment in the vaccination stocks scenario

from __future__ import print_function #ensure print functions are like Python 3
import despy as DES
from matplotlib import pyplot
from matplotlib.pyplot import hist,title,xlabel,ylabel,xlim,ylim

# turn these on to make the simulation chattier
#DES.verbosity.add("block")
#DES.verbosity.add("state")


###use the machinery in basic_block_simulator to make a sample model
###note that blocks are indexed according to their order
def setup_cabbageshop_model():

    #DES.state.clear()
    DES.state.add_block(DES.GenerateUniformBlock(5, 15))
    DES.state.add_block(DES.TerminateBlock(1))
    DES.state.terminate_counter = 5


def experiment():

    seed = 987654321;
    setup_cabbageshop_model()
    DES.random.seed(seed)

    DES.simulate()



if __name__=="__main__":

    experiment()
    #import cProfile
    #cProfile.run('experiment1()')
