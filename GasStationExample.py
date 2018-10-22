import despy as des


def gasstation():
    des.clear()
    des.debug(True)

    des.Storage("GasStation", 5)  # Set Pump count to 5
    des.Storage("Cashier", 2)  # Set Cashier count to 2
    des.Storage("FuelTank", 100)
    des.Storage("FuelTruck", 1)

    des.GenerateBlock("GenerateUniformOne", "Uniform", 5, 12.3, 1.5)  # 0 Cars arrive between 5.5 and 12.3 seconds
    des.EnterBlock("GasStationEnter", "GasStation", 1)  # 1 Cars Enter gas station which has 5 gas pumps so sixth car must wait
    des.EnterBlock("FuelTankEnter", "FuelTank", 20, "LeaveGasStation")  # 2 car takes  fuel from station tank if fuel is low at the station car moves out from the station
    des.AdvanceBlock("FillGasStation", "Uniform", 5, 15)  # 3 Filling the gas tank of a vehicle takes between 5 and 15 seconds
    des.EnterBlock("CashierEnter", "Cashier", 1)  # 4 After filling gas tank car owner must enter the line for payment
    des.AdvanceBlock("MakePayment", "Uniform", 3, 10)  # 5 Payment takes between 3 and 10 seconds
    des.LeaveBlock("LeaveCashier", "Cashier", 1)  # 6 After paying owner leaves the cashier line
    des.LeaveBlock("LeaveGasStation", "GasStation", 1)  # 7 After all owner leaves the station
    des.TerminateBlock("TerminateCar", 1)  # 8 Car destroyed

    des.LeaveBlock("LeaveGasStation", "GasStation", 1)  # 9 Car left the station without ever getting gas and calls the fuel truck
    des.EnterBlock("FuelTruckEnter", "FuelTruck", 1, "TerminateFuelTruck")  # 10 Car calls the fuel truck  but there  is only  one truck
    des.AdvanceBlock("FuelTruckArrive", "Uniform", 10, 20)  # 11  It takes the truck 10 to 20 seconds to arrive
    des.LeaveBlock("LeaveFuelTank", "FuelTank", 200)  # 12 Fuel truck fills the tanks
    des.LeaveBlock("LeaveFuelTruck", "FuelTruck", 1)  # 13 Fuel truck returns to base
    des.TerminateBlock("TerminateFuelTruck", 0)  # 14

    des.set_terminate(7)

    des.simulate()


#######################################################################################

if __name__ == "__main__":
    gasstation()
