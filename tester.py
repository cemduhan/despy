import despy as des
from matplotlib import pyplot
from matplotlib.pyplot import hist, title, xlabel, ylabel, xlim, ylim


def empirical_generate_test_valid_file():
    print("EmpiricalGenerate_Test_Valid_File")
    des.state.clear()
    des.state.debugging = False
    des.state.add_block(des.GenerateBlock('Empirical', "distru.txt", False))  # 0
    des.state.add_block(des.TerminateBlock(1))  # 2

    des.state.terminate_counter = 5


def empirical_generate_test_with_false_file():
    print("EmpiricalGenerate_Test_With_False_File")
    des.state.clear()
    des.state.debugging = False
    des.state.add_block(des.GenerateBlock('Empirical', "distrust.txt", False))  # 0
    des.state.add_block(des.TerminateBlock(1))  # 2

    des.state.terminate_counter = 5


#######################################################################################
def uniform_generate_test():
    print("UniformGenerate_Test")
    des.state.clear()
    des.state.debugging = False
    des.state.add_block(des.GenerateBlock('Uniform', 5.5, 12.3, 1.5))  # 0
    des.state.add_block(des.TerminateBlock(1))  # 2

    des.state.terminate_counter = 5


#######################################################################################
def terminate_block_test_with_invalid_limit():
    print("TerminateBlock_Test_With_Invalid_Limit")
    des.state.clear()
    des.state.debugging = False
    des.state.add_block(des.GenerateBlock('NoDelay', 5))  # 0
    des.state.add_block(des.TerminateBlock(-2))  # 2

    des.state.terminate_counter = 5


def terminate_block_test_with_valid_limit():
    print("TerminateBlock_Test_With_Valid_Limit")
    des.state.clear()
    des.state.debugging = False
    des.state.add_block(des.GenerateBlock('NoDelay', 5))  # 0
    des.state.add_block(des.TerminateBlock(2))  # 2

    des.state.terminate_counter = 5


#######################################################################################
def nodelay_generate_test_with_valid_limit():
    print("NoDelayGenerate_Test")
    des.state.clear()
    des.state.debugging = False
    des.state.add_block(des.GenerateBlock('NoDelay', 5))  # 0
    des.state.add_block(des.TerminateBlock(1))  # 2

    des.state.terminate_counter = 5


def nodelay_generate_test_with_invalid_limit():
    print("NoDelayGenerate_Test")
    des.state.clear()
    des.state.debugging = False
    des.state.add_block(des.GenerateBlock('NoDelay', -2))  # 0
    des.state.add_block(des.TerminateBlock(1))  # 2

    des.state.terminate_counter = 5


#######################################################################################
def enterblock_test_valid_que_size():
    print("EnterBlockTest_Valid_Que_Size")
    des.state.clear()
    des.state.debugging = True
    des.state.add_block(des.GenerateBlock('Uniform', 2, 2, 1.2))  # 0
    des.state.add_block(des.EnterBlock("Depot", 1))  # 1
    des.state.add_block(des.AdvanceBlock('Uniform', 5, 5))  # 2
    des.state.add_block(des.LeaveBlock("Depot"))  # 3
    des.state.add_block(des.TerminateBlock(1))  # 4

    des.state.terminate_counter = 2


def enterblock_test_invalid_que_size():
    print("EnterBlockTest_Invalid_Que_Size")
    des.state.clear()
    des.state.debugging = False
    des.state.add_block(des.GenerateBlock('Uniform', 2, 2, 1.2))  # 0
    des.state.add_block(des.EnterBlock("Depot", -2))  # 1
    des.state.add_block(des.AdvanceBlock('Uniform', 10, 10))  # 2
    des.state.add_block(des.LeaveBlock("Depot"))  # 3
    des.state.add_block(des.TerminateBlock(1))  # 4

    des.state.terminate_counter = 10


#######################################################################################
def transferblock_test_with_everything_passing():
    print("TransferBlock_Test_With_Everything_Passing")
    des.state.clear()
    des.state.debugging = False
    des.state.add_block(des.GenerateBlock('Uniform', 5, 5, 1.2))  # 0
    des.state.add_block(des.TransferBlock(100, 3))  # 1
    des.state.add_block(des.TerminateBlock(2))  # 2
    des.state.add_block(des.TerminateBlock(1))  # 3

    des.state.terminate_counter = 10


def transferblock_test_with_nothing_passing():
    print("TransferBlock_Test_With_Nothing_Passing")
    des.state.clear()
    des.state.debugging = False
    des.state.add_block(des.GenerateBlock('Uniform', 5, 5, 1.2))  # 0
    des.state.add_block(des.TransferBlock(0, 3))  # 1
    des.state.add_block(des.TerminateBlock(2))  # 2
    des.state.add_block(des.TerminateBlock(1))  # 3

    des.state.terminate_counter = 10


#######################################################################################
def experiment():
    seed = 987654321
    des.random.seed(seed)

    enterblock_test_valid_que_size()

    des.simulate()


if __name__ == "__main__":
    experiment()
