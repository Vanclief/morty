class Balance:
    def __init__(self, pair, asset1_balance):
        self.pair = pair.split("-")
        self.asset1 = float(asset1_balance)
        self.asset2 = 0
        self.asset2_debt = 0
        self.initial = float(asset1_balance)
