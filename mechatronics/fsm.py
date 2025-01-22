class FSM:

    def __init__(self):
        self.state = "start"
        self.statev = list()

        # Inputs
        self.ps = 0  # pollen sensor: 1 if there is a change in pollon sensed and there is pollen there
        self.cs = 0  # 1 if pollen is right color
        self.lr = 0  # location reached (1 if yes)
        self.sg = 0  # start game: 1 if active
        self.np = 0  # nonzero pollen in bot (based on count(cs ~= 0))
        self.fp = 0  # is the bot full?

        # Outputs
        self.tp = 0  # run target pattern if 1
        self.hp = 0  # run home pattern if 1
        self.pd = 0  # release one stored pollen if 1
        self.rp = 0  # reject pollen: 1 if pollen should be tossed
        self.ap = 0  # accept pollen: 1 if pollen should be accepted

    """
    S0: start (neutral, wait for user input and pollen)
        S0.1: pre_accept (accept state before game starts)
        S0.2: pre_reject (reject state before game starts)
    S1: accept (pollen loaded and it is the desired color)
    S2: reject (pollen loaded and not desired color)
    S3: drive_targ (drive to targ) 
    S4: deposit (at target)
    S5: return (to home)
    S6: ready (just returned home, ready to reload) --> back to S1, S2
    S7: done (timer out)
    """

    # BEGIN STATE DECLARATION

    def start(self):
        # Outputs - no nonzero outputs

        # Transition
        if self.ps and self.cs:
            self.state = "pre_accept"
        elif self.ps and (not self.cs):
            self.state = "pre_reject"
        elif self.sg:
            self.state = "ready"

    def pre_acc(self):
        # Outputs
        self.ap = 1
        print("ACCEPT ACTIVATED")

        # Transition
        if not self.ps:
            self.state = "start"

    def pre_rej(self):
        # Outputs
        self.rp = 1
        print("REJECT ACTIVATED")

        # Transition
        if not self.ps:
            self.state = "start"

    def accept(self):
        # Outputs
        self.ap = 1
        print("ACCEPT ACTIVATED")

        # Transition
        if (not self.ps) and self.sg:
            self.state = "ready"
        elif not self.sg:
            self.state = "done"

    def reject(self):
        # Outputs
        self.rp = 1
        print("REJECT ACTIVATED")

        # Transition
        if (not self.ps) and self.sg:
            self.state = "ready"
        elif not self.sg:
            self.state = "done"

    def drive(self):
        # Outputs
        self.tp = 1
        print("TARGET PATTERN ACTIVATED")

        # Transition
        if self.lr and self.sg:
            self.state = "deposit"
        elif not self.sg:
            self.state = "done"

    def deposit(self):
        # Outputs
        self.pd = 1
        print("POLLEN DEPOSIT ACTIVATED")

        # Add: decrease pollen count OR release for an arbitrary time

        # Transition
        if (not self.fp) and self.sg:
            self.state = "return"
        elif not self.sg:
            self.state = "done"


    def ret(self):
        # Outputs
        self.hp = 1
        print("HOME PATTERN ACTIVATED")

        # Transition
        if self.lr and self.sg:
            # TODO: pause timer
            self.state = "ready"
        elif not self.sg:
            self.state = "done"

    def ready(self):
        # Outputs - no nonzero outputs

        # Transition
        if self.ps and self.cs and (not self.fp):
            self.state = "accept"
        elif self.ps and (not self.cs) and (not self.fp):
            self.state = "reject"
        elif self.fp:
            self.state = "drive_targ"
        elif not self.sg:
            self.state = "done"

    def done(self):
        # Outputs - no nonzero outputs

        # Transition - no transition
        print("DONE STATE")

    # END STATE DECLARATION

    def update_state(self):
        # Facilitates moving between states as sub-functions
        self.statev.append(self.state)  # Record state for future use

        if self.state == "start":
            self.start()
        elif self.state == "pre_accept":
            self.pre_acc()
        elif self.state == "pre_reject":
            self.pre_rej()
        elif self.state == "accept":
            self.accept()
        elif self.state == "reject":
            self.reject()
        elif self.state == "drive_targ":
            self.drive()
        elif self.state == "deposit":
            self.deposit()
        elif self.state == "return":
            self.ret()
        elif self.state == "ready":
            self.ready()
        elif self.state == "done":
            self.done()

    def update(self, ps, cs, lr, sg, np, fp):
        # TODO: no outputs should hang at 0; reset (if things don't work, fix
        # this)
        self.hp = 0
        self.tp = 0
        self.pd = 0
        self.rp = 0
        self.ap = 0

        # Set inputs
        self.ps = ps
        self.cs = cs
        self.lr = lr
        self.sg = sg
        self.np = np
        self.fp = fp

        self.update_state()
        print(self.state)