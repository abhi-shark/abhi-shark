from utilities import FSM
import pandas as pd

def main():
    fsm = FSM()
    M = pd.read_csv('inputs.csv')

    for i in range(len(M.exps)):

        ps = M.ps[i]  # pollen sensor: 1 is pollen sensed at loading pt
        cs = M.cs[i]  # 1 is pollen is right color
        lr = M.lr[i]  # location reached (1 if yes)
        sg = M.sg[i]  # start game: 1 if active
        np = M.np[i]  # nonzero pollen in bot (based on count(cs ~= 0))
        fp = M.fp[i]  # is the bot full?

        # Update state
        fsm.update(ps, cs, lr, sg, np, fp)


    # Check expected behavior
    v = list()
    for i in range(len(M.exps)):
        curr_state = M.exps[i]
        fsm_state = fsm.statev[i]
        v.append(curr_state == fsm_state)

    print("\nAll elements match: ", all(v))


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()


