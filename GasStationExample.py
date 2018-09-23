import despy as des
from matplotlib import pyplot
from matplotlib.pyplot import hist, title, xlabel, ylabel, xlim, ylim


def gasstation():
    des.state.clear()
    des.state.debugging = False
    des.state.add_block(des.GenerateBlock('Uniform', 5.5, 12.3, 1.5))  # 0 Cars arrive between 5.5 and 12.3 seconds

    des.state.add_block(
        des.EnterBlock("GasStation", 5))  # 1 Cars Enter gas station which has 5 gas pumps so sixth car must wait

    des.state.add_block(
        des.AdvanceBlock('Uniform', 5, 15))  # 2 Filling the gas tank of a vehicle takes between 5 and 15 seconds

    des.state.add_block(
        des.EnterBlock("Cashier", 2))  # 3 After filling gas tank car owner must enter the line for payment

    des.state.add_block(des.AdvanceBlock('Uniform', 3, 10))  # 4 Payment takes between 3 and 10 seconds
    des.state.add_block(des.LeaveBlock("Cashier"))  # 5 After paying owner leaves the cashier line
    des.state.add_block(des.LeaveBlock("GasStation"))  # 6 After all owner leaves the station
    des.state.add_block(des.TerminateBlock(1))  # 7 Car destroyed

    des.state.terminate_counter = 5


#######################################################################################
def experiment():
    seed = 987654321
    des.random.seed(seed)

    gasstation()

    des.simulate()


if __name__ == "__main__":
    experiment()
