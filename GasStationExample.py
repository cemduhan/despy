import despy as des


def gasstation():
    des.clear()
    des.debug(True)

    des.Storage("GasStation", 5)  # Set Pump count to 5
    des.Storage("Cashier", 2)  # Set Cashier count to 2
    des.Storage("FuelTank", 100)
    des.Storage("FuelTruck", 1)

    des.GenerateBlock("Uniform", 5, 12.3, 1.5)  # 0 Cars arrive between 5.5 and 12.3 seconds
    des.EnterBlock("GasStation", 1)  # 1 Cars Enter gas station which has 5 gas pumps so sixth car must wait
    des.EnterBlock("FuelTank", 20, 9)  # 2 car takes  fuel from station tank if fuel is low at the station car moves out from the station
    des.AdvanceBlock('Uniform', 5, 15)  # 3 Filling the gas tank of a vehicle takes between 5 and 15 seconds
    des.EnterBlock("Cashier", 1)  # 4 After filling gas tank car owner must enter the line for payment
    des.AdvanceBlock('Uniform', 3, 10)  # 5 Payment takes between 3 and 10 seconds
    des.LeaveBlock("Cashier", 1)  # 6 After paying owner leaves the cashier line
    des.LeaveBlock("GasStation", 1)  # 7 After all owner leaves the station
    des.TerminateBlock(1)  # 8 Car destroyed

    des.LeaveBlock("GasStation", 1)  # 9 Car left the station without ever getting gas and calls the fuel truck
    des.EnterBlock("FuelTruck", 1, 14)  # 10 Car calls the fuel truck  but there  is only  one truck
    des.AdvanceBlock('Uniform', 10, 20)  # 11  It takes the truck 10 to 20 seconds to arrive
    des.LeaveBlock("FuelTank", 200)  # 12 Fuel truck fills the tanks
    des.LeaveBlock("FuelTruck", 1)  # 13 Fuel truck returns to base
    des.TerminateBlock(0)  # 14

    des.set_terminate(7)

    des.simulate()


#######################################################################################

if __name__ == "__main__":
    gasstation()
