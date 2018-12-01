import despy as des


def carwash():
    des.clear()
    des.debug(True)

    des.Storage("Carwash", 2)
    # There is only two carwash slot
    des.GenerateBlock("GenerateCars", "Uniform", 0, 5)
    # Cars get in the carwash every 0 to 5 minutes
    des.EnterBlock("CarwashEnter", "Carwash", 1)
    # Car enters the carwash
    des.AdvanceBlock("WashCar", "Uniform", 15, 15)
    # A Car takes 15 minutes to wash
    des.LeaveBlock("LeaveCarwash", "Carwash", 1)
    # Car leaves the carwash
    des.TerminateBlock("CarLeft", 1)
    # Car leaves the simulation
    des.set_terminate(6)
    # Stop the simulation after 6  Cars Left

    des.simulate()


if __name__ == "__main__":
    carwash()


