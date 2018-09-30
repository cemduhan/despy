import despy as des


def gasstation():
    des.simulation.clear()
    des.simulation.debug(False)

    des.Storage("GasStation", 5)  # Set Pump count to 5
    des.Storage("Cashier", 2)  # Set Cashier count to 2

    des.GenerateBlock("Uniform", 5, 12.3, 1.5)  # 0 Cars arrive between 5.5 and 12.3 seconds

    des.EnterBlock("GasStation", 1)  # 1 Cars Enter gas station which has 5 gas pumps so sixth car must wait

    des.AdvanceBlock('Uniform', 5, 15)  # 2 Filling the gas tank of a vehicle takes between 5 and 15 seconds

    des.EnterBlock("Cashier", 1)  # 3 After filling gas tank car owner must enter the line for payment

    des.AdvanceBlock('Uniform', 3, 10)  # 4 Payment takes between 3 and 10 seconds
    des.LeaveBlock("Cashier", 1)  # 5 After paying owner leaves the cashier line
    des.LeaveBlock("GasStation", 1)  # 6 After all owner leaves the station
    des.TerminateBlock(1)  # 7 Car destroyed

    des.simulation.set_terminate(7)

    des.simulate()


#######################################################################################

if __name__ == "__main__":
    gasstation()
