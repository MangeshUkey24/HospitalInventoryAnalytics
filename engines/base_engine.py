class BaseEngine:

    def __init__(self, opening, purchase, sales, adjustment):
        self.opening = opening
        self.purchase = purchase
        self.sales = sales
        self.adjustment = adjustment

    def calculate(self):
        raise NotImplementedError("Engine must implement calculate()")