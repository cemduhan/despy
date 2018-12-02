import despy as des


def bank_teller_kiosk():
    des.clear()
    des.Storage("Tellers", 2)
    des.Storage("Kiosks", 5)

    des.GenerateBlock("GeneratePeople", "Uniform", 0, 3)
    # People arrive between 0 - 5 minute with an uniform distribution
    des.TransferBlock("NeedsToSeeTeller", 60, "Teller")
    # There is fifty percent chance that a people needs to go to teller
    des.QueueBlock("KioskQue")
    des.EnterBlock("Kiosk", "Kiosks", 1)
    # Enter the line for a kiosk and wait until seizing one
    des.AdvanceBlock("KioskDone", "Uniform", 2, 6)  # Do necessary job
    des.LeaveBlock("LeaveKiosk", "Kiosks", 1)  # Leave the kiosk
    des.LeaveQueueBlock("LeaveKioskQue", "KioskQue")
    des.TransferBlock("NeedsTellerAssistance", 40, "Teller")
    # Does the person still needs help from a teller if so go to teller
    des.TerminateBlock("LeaveTheBankUsingKiosk", 1)  # If not leave the bank

    des.QueueBlock("TellerQue")
    des.EnterBlock("Teller", "Tellers", 1)
    # Enter the line for a Teller and wait until seizing one
    des.AdvanceBlock("TellerWait", "Uniform", 2, 6)  # Do necessary job
    des.LeaveBlock("LeaveTeller", "Tellers", 1)  # Leave the teller
    des.LeaveQueueBlock("LeaveTellerQue", "TellerQue")

    des.TerminateBlock("LeaveBankUsingTeller", 1)  # Leave the bank
    des.set_terminate(20)  # Bank closes after 50 people is done
    des.simulate()


if __name__ == "__main__":
    bank_teller_kiosk()





