import despy as des
from matplotlib import pyplot
from matplotlib.pyplot import hist,title,xlabel,ylabel,xlim,ylim

def EmpiricalGenerate_Test_Valid_File():
    print("EmpiricalGenerate_Test_Valid_File")
    des.state.clear()
    des.state.debugging=False
    des.state.add_block(des.GenerateBlock('Empirical', "distru.txt", False))#0
    des.state.add_block(des.TerminateBlock(1))#2

    des.state.terminate_counter = 5

def EmpiricalGenerate_Test_With_False_File():
    print("EmpiricalGenerate_Test_With_False_File")
    des.state.clear()
    des.state.debugging=False
    des.state.add_block(des.GenerateBlock('Empirical', "distrust.txt", False))#0
    des.state.add_block(des.TerminateBlock(1))#2

    des.state.terminate_counter = 5
#######################################################################################
def UniformGenerate_Test():
    print("UniformGenerate_Test")
    des.state.clear()
    des.state.debugging=False
    des.state.add_block(des.GenerateBlock('Uniform',5.5, 12.3, 1.5))#0
    des.state.add_block(des.TerminateBlock(1))#2

    des.state.terminate_counter = 5
#######################################################################################
def TerminateBlock_Test_With_Invalid_Limit():
    print("TerminateBlock_Test_With_Invalid_Limit")
    des.state.clear()
    des.state.debugging=False
    des.state.add_block(des.GenerateBlock('NoDelay',5))#0
    des.state.add_block(des.TerminateBlock(-2))#2

    des.state.terminate_counter = 5

def TerminateBlock_Test_With_Valid_Limit():
    print("TerminateBlock_Test_With_Valid_Limit")
    des.state.clear()
    des.state.debugging=False
    des.state.add_block(des.GenerateBlock('NoDelay',5))#0
    des.state.add_block(des.TerminateBlock(2))#2

    des.state.terminate_counter = 5
#######################################################################################
def NoDelayGenerate_Test_With_Valid_Limit():
    print("NoDelayGenerate_Test")
    des.state.clear()
    des.state.debugging=False
    des.state.add_block(des.GenerateBlock('NoDelay',5))#0
    des.state.add_block(des.TerminateBlock(1))#2

    des.state.terminate_counter = 5

def NoDelayGenerate_Test_With_Invalid_Limit():
    print("NoDelayGenerate_Test")
    des.state.clear()
    des.state.debugging=False
    des.state.add_block(des.GenerateBlock('NoDelay',-2))#0
    des.state.add_block(des.TerminateBlock(1))#2

    des.state.terminate_counter = 5
#######################################################################################
def EnterBlockTest_Valid_Que_Size():
    print("EnterBlockTest_Valid_Que_Size")
    des.state.clear()
    des.state.debugging=True
    des.state.add_block(des.GenerateBlock('Uniform',2, 2, 1.2))#0
    des.state.add_block(des.EnterBlock("Depot", 2))#1
    des.state.add_block(des.AdvanceBlock('Uniform',5,5))#2
    des.state.add_block(des.LeaveBlock("Depot"))#3
    des.state.add_block(des.TerminateBlock(1))#4

    des.state.terminate_counter = 3

def EnterBlockTest_Invnalid_Que_Size():
    print("EnterBlockTest_Invnalid_Que_Size")
    des.state.clear()
    des.state.debugging=False
    des.state.add_block(des.GenerateBlock('Uniform',2, 2, 1.2))#0
    des.state.add_block(des.EnterBlock("Depot", -2))#1
    des.state.add_block(des.AdvanceBlock('Uniform',10,10))#2
    des.state.add_block(des.LeaveBlock("Depot"))#3
    des.state.add_block(des.TerminateBlock(1))#4

    des.state.terminate_counter = 10
#######################################################################################
def TransferBlock_Test_With_Everything_Passing():
    print("TransferBlock_Test_With_Everything_Passing")
    des.state.clear()
    des.state.debugging=False
    des.state.add_block(des.GenerateBlock('Uniform',5, 5, 1.2))#0
    des.state.add_block(des.TransferBlock(100,3))#1
    des.state.add_block(des.TerminateBlock(2))#2
    des.state.add_block(des.TerminateBlock(1))#3

    des.state.terminate_counter = 10

def TransferBlock_Test_With_Nothing_Passing():
    print("TransferBlock_Test_With_Nothing_Passing")
    des.state.clear()
    des.state.debugging=False
    des.state.add_block(des.GenerateBlock('Uniform',5, 5, 1.2))#0
    des.state.add_block(des.TransferBlock(0,3))#1
    des.state.add_block(des.TerminateBlock(2))#2
    des.state.add_block(des.TerminateBlock(1))#3

    des.state.terminate_counter = 10
#######################################################################################
def experiment():

    seed = 987654321
    des.random.seed(seed)

    EnterBlockTest_Valid_Que_Size()

    des.simulate()


if __name__=="__main__":

    experiment()
