import despy as des


def empirical_generate_test_valid_file():
    print("EmpiricalGenerate_Test_Valid_File")
    des.state.clear()
    des.debug(False)
    des.GenerateBlock('Empirical', "distru.txt", False)  # 0
    des.TerminateBlock(1)  # 2

    des.set_terminate(5)

    des.simulate()


def empirical_generate_test_with_false_file():
    print("EmpiricalGenerate_Test_With_False_File")
    des.state.clear()
    des.debug(False)
    des.GenerateBlock('Empirical', "distrust.txt", False)  # 0
    des.TerminateBlock(1)  # 2

    des.set_terminate(5)

    des.simulate()


#######################################################################################
def uniform_generate_test():
    print("UniformGenerate_Test")
    des.state.clear()
    des.debug(False)
    des.GenerateBlock('Uniform', 5.5, 12.3, 1.5)  # 0
    des.TerminateBlock(1)  # 2

    des.set_terminate(5)

    des.simulate()


#######################################################################################
def terminate_block_test_with_invalid_limit():
    print("TerminateBlock_Test_With_Invalid_Limit")
    des.state.clear()
    des.debug(False)
    des.GenerateBlock('NoDelay', 5)  # 0
    des.TerminateBlock(-2)  # 2

    des.set_terminate(5)

    des.simulate()


def terminate_block_test_with_valid_limit():
    print("TerminateBlock_Test_With_Valid_Limit")
    des.state.clear()
    des.debug(False)
    des.GenerateBlock('NoDelay', 5)  # 0
    des.TerminateBlock(2)  # 2

    des.set_terminate(5)

    des.simulate()


#######################################################################################
def nodelay_generate_test_with_valid_limit():
    print("NoDelayGenerate_Test")
    des.state.clear()
    des.debug(False)
    des.GenerateBlock('NoDelay', 5)  # 0
    des.TerminateBlock(1)  # 2

    des.set_terminate(5)

    des.simulate()


def nodelay_generate_test_with_invalid_limit():
    print("NoDelayGenerate_Test")
    des.state.clear()
    des.debug(False)
    des.GenerateBlock('NoDelay', -2)  # 0
    des.TerminateBlock(1)  # 2

    des.set_terminate(5)

    des.simulate()


#######################################################################################
def enterblock_test_valid_que_size():
    print("EnterBlockTest_Valid_Que_Size")
    des.state.clear()
    des.debug(True)
    des.GenerateBlock('Uniform', 2, 2, 1.2)  # 0
    des.EnterBlock("Depot", 1)  # 1
    des.AdvanceBlock('Uniform', 5, 5)  # 2
    des.LeaveBlock("Depot")  # 3
    des.TerminateBlock(1)  # 4

    des.set_terminate(2)

    des.simulate()


def enterblock_test_invalid_que_size():
    print("EnterBlockTest_Invalid_Que_Size")
    des.state.clear()
    des.debug(False)
    des.GenerateBlock('Uniform', 2, 2, 1.2)  # 0
    des.EnterBlock("Depot", -2)  # 1
    des.AdvanceBlock('Uniform', 10, 10)  # 2
    des.LeaveBlock("Depot")  # 3
    des.TerminateBlock(1)  # 4

    des.set_terminate(10)
    des.simulate()

#######################################################################################
def transferblock_test_with_everything_passing():
    print("TransferBlock_Test_With_Everything_Passing")
    des.state.clear()
    des.debug(False)
    des.GenerateBlock('Uniform', 5, 5, 1.2)  # 0
    des.TransferBlock(100, 3)  # 1
    des.TerminateBlock(2)  # 2
    des.TerminateBlock(1)  # 3

    des.set_terminate(10)

    des.simulate()


def transferblock_test_with_nothing_passing():
    print("TransferBlock_Test_With_Nothing_Passing")
    des.state.clear()
    des.debug(False)
    des.GenerateBlock('Uniform', 5, 5, 1.2)  # 0
    des.TransferBlock(0, 3)  # 1
    des.TerminateBlock(2)  # 2
    des.TerminateBlock(1)  # 3

    des.set_terminate(10)

    des.simulate()


#######################################################################################

def split_assamble_block():
    print("Split_Block_With_Assemble")
    des.clear()
    des.debug(True)

    des.GenerateBlock('Uniform', 25, 25, 1.2)  # 0
    des.SplitBlock(2, 4)
    des.AdvanceBlock('Uniform', 3, 3)  # 1
    des.AssembleBlock()    # 2
    des.AdvanceBlock('Uniform', 5, 5)  # 1
    des.TerminateBlock(1)  # 3

    des.set_terminate(2)

    des.simulate()


def split_block():
    print("Split_Block_With_Displace_Assemble")
    des.clear()
    des.debug(True)

    des.GenerateBlock('Uniform', 25, 25, 1.2)  # 0
    des.SplitBlock(2, 4)
    des.AdvanceBlock('Uniform', 3, 3)  # 1
    des.AssembleBlock()    # 2
    des.AdvanceBlock('Uniform', 5, 5)  # 1
    des.TerminateBlock(1)  # 3

    des.set_terminate(2)

    des.simulate()
#######################################################################################


if __name__ == "__main__":
    split_block()
