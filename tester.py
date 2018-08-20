import despy as DES
from matplotlib import pyplot
from matplotlib.pyplot import hist,title,xlabel,ylabel,xlim,ylim


def test_model():

    DES.state.clear()
    DES.state.add_block(DES.GenerateBlock('Uniform',5, 5, 1.2))#0
    DES.state.add_block(DES.LinkBlock("shelf"))#1
    DES.state.add_block(DES.TerminateBlock(1))#2

    DES.state.add_block(DES.GenerateBlock('Uniform',5, 5, 1.2))#3
    DES.state.add_block(DES.AdvanceBlock('Uniform',1,1))#4
    DES.state.add_block(DES.UnlinkBlock.factory("FIFO","shelf",3,2))#5
    DES.state.add_block(DES.TerminateBlock(0))#6

    DES.state.terminate_counter = 10


def experiment():

    seed = 987654321;
    test_model()
    DES.random.seed(seed)

    DES.simulate()



if __name__=="__main__":

    experiment()
