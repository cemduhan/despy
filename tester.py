import despy as DES
from matplotlib import pyplot
from matplotlib.pyplot import hist,title,xlabel,ylabel,xlim,ylim

def EmpiricalGenerate_Test_Valid_File():
    print("EmpiricalGenerate_Test_Valid_File")
    DES.state.clear()
    DES.state.debugging=False
    DES.state.add_block(DES.GenerateBlock('Empirical', "distru.txt", False))#0
    DES.state.add_block(DES.TerminateBlock(1))#2

    DES.state.terminate_counter = 5

def EmpiricalGenerate_Test_With_False_File():
    print("EmpiricalGenerate_Test_With_False_File")
    DES.state.clear()
    DES.state.debugging=False
    DES.state.add_block(DES.GenerateBlock('Empirical', "distrust.txt", False))#0
    DES.state.add_block(DES.TerminateBlock(1))#2

    DES.state.terminate_counter = 5
#######################################################################################
def UniformGenerate_Test():
    print("UniformGenerate_Test")
    DES.state.clear()
    DES.state.debugging=False
    DES.state.add_block(DES.GenerateBlock('Uniform',5.5, 12.3, 1.5))#0
    DES.state.add_block(DES.TerminateBlock(1))#2

    DES.state.terminate_counter = 5
#######################################################################################
def TerminateBlock_Test_With_Invalid_Limit():
    print("TerminateBlock_Test_With_Invalid_Limit")
    DES.state.clear()
    DES.state.debugging=False
    DES.state.add_block(DES.GenerateBlock('NoDelay',5))#0
    DES.state.add_block(DES.TerminateBlock(-2))#2

    DES.state.terminate_counter = 5

def TerminateBlock_Test_With_Valid_Limit():
    print("TerminateBlock_Test_With_Valid_Limit")
    DES.state.clear()
    DES.state.debugging=False
    DES.state.add_block(DES.GenerateBlock('NoDelay',5))#0
    DES.state.add_block(DES.TerminateBlock(2))#2

    DES.state.terminate_counter = 5
#######################################################################################
def NoDelayGenerate_Test_With_Valid_Limit():
    print("NoDelayGenerate_Test")
    DES.state.clear()
    DES.state.debugging=False
    DES.state.add_block(DES.GenerateBlock('NoDelay',5))#0
    DES.state.add_block(DES.TerminateBlock(1))#2

    DES.state.terminate_counter = 5

def NoDelayGenerate_Test_With_Invalid_Limit():
    print("NoDelayGenerate_Test")
    DES.state.clear()
    DES.state.debugging=False
    DES.state.add_block(DES.GenerateBlock('NoDelay',-2))#0
    DES.state.add_block(DES.TerminateBlock(1))#2

    DES.state.terminate_counter = 5
#######################################################################################
def EnterBlockTest_Valid_Que_Size():
    print("EnterBlockTest_Valid_Que_Size")
    DES.state.clear()
    DES.state.debugging=False
    DES.state.add_block(DES.GenerateBlock('Uniform',2, 2, 1.2))#0
    DES.state.add_block(DES.EnterBlock("Depot", 2))#1
    DES.state.add_block(DES.AdvanceBlock('Uniform',10,10))#2
    DES.state.add_block(DES.LeaveBlock("Depot"))#3
    DES.state.add_block(DES.TerminateBlock(1))#4

    DES.state.terminate_counter = 10

def EnterBlockTest_Invnalid_Que_Size():
    print("EnterBlockTest_Invnalid_Que_Size")
    DES.state.clear()
    DES.state.debugging=False
    DES.state.add_block(DES.GenerateBlock('Uniform',2, 2, 1.2))#0
    DES.state.add_block(DES.EnterBlock("Depot", -2))#1
    DES.state.add_block(DES.AdvanceBlock('Uniform',10,10))#2
    DES.state.add_block(DES.LeaveBlock("Depot"))#3
    DES.state.add_block(DES.TerminateBlock(1))#4

    DES.state.terminate_counter = 10
#######################################################################################
def TransferBlock_Test_With_Everything_Passing():
    print("TransferBlock_Test_With_Everything_Passing")
    DES.state.clear()
    DES.state.debugging=False
    DES.state.add_block(DES.GenerateBlock('Uniform',5, 5, 1.2))#0
    DES.state.add_block(DES.TransferBlock(100,3))#1
    DES.state.add_block(DES.TerminateBlock(2))#2
    DES.state.add_block(DES.TerminateBlock(1))#3

    DES.state.terminate_counter = 10

def TransferBlock_Test_With_Nothing_Passing():
    print("TransferBlock_Test_With_Nothing_Passing")
    DES.state.clear()
    DES.state.debugging=False
    DES.state.add_block(DES.GenerateBlock('Uniform',5, 5, 1.2))#0
    DES.state.add_block(DES.TransferBlock(0,3))#1
    DES.state.add_block(DES.TerminateBlock(2))#2
    DES.state.add_block(DES.TerminateBlock(1))#3

    DES.state.terminate_counter = 10
#######################################################################################
def experiment():

    seed = 987654321
    DES.random.seed(seed)

    TerminateBlock_Test_With_Valid_Limit()

    DES.simulate()


if __name__=="__main__":

    experiment()
