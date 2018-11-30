import despy as des


def turnstile():
    des.clear()
    in_use = 5
    in_range = 3
    des.Storage("Turnstile", 1)

    des.GenerateBlock("GeneratePeople", "Uniform", 0, 14)
    des.EnterBlock("TurnstileEnter", "Turnstile", 1)
    des.AdvanceBlock("TurnstileWait", "Uniform", in_use-in_range, in_use+in_range)
    des.LeaveBlock("LeaveTurnstile", "Turnstile", 1)
    des.TerminateBlock("PeopleEntered", 1)
    des.set_terminate(300)

    des.simulate()


if __name__ == "__main__":
    turnstile()





