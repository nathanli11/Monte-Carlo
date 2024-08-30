class Market:
    #Market class is used to intialize the different market values
    def __init__(self,p, v, r, divY):
        self.UndPrice = p
        self.Volatility = v
        self.Rate = r
        self.DividendYield = divY
    
    def Inititalize_Market(self, p, v, r, divY):
        self.UndPrice = p
        self.Volatility = v
        self.Rate = r
        self.DividendYield = divY
    
    def AreSame(self, mkt2):
        return (self.UndPrice == mkt2.UndPrice and
                self.Volatility == mkt2.Volatility and
                self.Rate == mkt2.Rate and
                self.DividendYield == mkt2.DividendYield)
    
    def DeepCopy(self):
        return Market(self.UndPrice, self.Volatility, self.Rate, self.DividendYield)
