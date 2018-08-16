import despy as DES
from matplotlib import pyplot
from matplotlib.pyplot import hist,title,xlabel,ylabel,xlim,ylim


def test_model():

    #DES.state.clear()
    DES.state.add_block(DES.GenerateBlock('Uniform',5, 15, 1.2))
    DES.state.add_block(DES.TerminateBlock(1))
    DES.state.terminate_counter = 5


def experiment():

    seed = 987654321;
    test_model()
    DES.random.seed(seed)

    DES.simulate()



if __name__=="__main__":

    experiment()
