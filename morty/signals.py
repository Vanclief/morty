class EnterMarket:

    def __init__(self, signal_type, tick, size):
        self.signal_type = signal_type
        self.tick = tick
        self.size = size

class ExitMarket:

    def __init__(self, tick, trade):
        self.tick = tick
        self.trade = trade
