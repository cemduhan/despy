import despy as DES
from matplotlib import pyplot
from matplotlib.pyplot import hist,title,xlabel,ylabel,xlim,ylim


def test_model_1():

    DES.state.clear()
    DES.state.debugging=True
    DES.state.add_block(DES.GenerateBlock('Uniform',5, 5, 1.2))#0
    DES.state.add_block(DES.LinkBlock("shelf"))#1
    DES.state.add_block(DES.TransferBlock(30,6))#2
    DES.state.add_block(DES.TerminateBlock(2))#3

    DES.state.add_block(DES.GenerateBlock('Uniform',5, 5, 1.2))#4
    DES.state.add_block(DES.AdvanceBlock('Uniform',1,1))#5
    DES.state.add_block(DES.UnlinkBlock.factory("FIFO","shelf",3,2))#6
    DES.state.add_block(DES.TerminateBlock(1))#7

    DES.state.terminate_counter = 10

def test_model_2():

    DES.state.clear()
    DES.state.debugging=True
    DES.state.add_block(DES.GenerateBlock('Uniform',5, 5, 1.2))#0
    DES.state.add_block(DES.EnterBlock("Depot", 2))#1
    DES.state.add_block(DES.AdvanceBlock('Uniform',10,10))#2
    DES.state.add_block(DES.LeaveBlock("Depot"))#3
    DES.state.add_block(DES.TerminateBlock(1))#4

    DES.state.terminate_counter = 10

def test_model_3():

    DES.state.clear()
    DES.state.debugging=True
    DES.state.add_block(DES.GenerateBlock('Empirical', "distru.txt", False))#0
    DES.state.add_block(DES.TerminateBlock(1))#4

    DES.state.terminate_counter = 1

def test_model_4():

    DES.state.clear()
    DES.state.debugging=True
    DES.state.add_block(DES.GenerateBlock('Uniform',5.5, 12.3, 1.5))#0
    DES.state.add_block(DES.TerminateBlock(1))#4

    DES.state.terminate_counter = 1

def test_model_5():

    DES.state.clear()
    DES.state.debugging=True
    DES.state.add_block(DES.GenerateBlock('NoDelay',5))#0
    DES.state.add_block(DES.TerminateBlock(1))#4

    DES.state.terminate_counter = 5

def experiment():

    seed = 987654321;
    test_model_1()

    DES.simulate()



if __name__=="__main__":

    experiment()
