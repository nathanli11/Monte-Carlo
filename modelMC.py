# local imports, not xlwings!
from model import Model
from market import Market
from optionTrade import OptionTrade
from brownian import Brownian


import numpy as np
import datetime

#pr_date correspond a pricing_date

class MCModel(Model):
    #Initializing variables. Use of other classes
    def __init__(self, pr_date : datetime, market : Market, NbDraws : int, NbSteps : int):
        Model.__init__(self, pr_date)
        self.market = market
        self.NbDraws = NbDraws
        self.NbSteps = NbSteps
        self.TimeToMaturity = None
        self.DiscountF = None
        self.Forward = None
        self.Timestep = None
        self.TimeValueDaysInYear = 365.0
    
    def InitVariables(self, market:Market, option:OptionTrade):
        self.TimeToMaturity = (datetime.datetime.strptime(option.mat_date, "%d/%m/%Y") - 
                               datetime.datetime.strptime(self.pricing_date, "%d/%m/%Y")).days / self.TimeValueDaysInYear
        self.DiscountF = np.exp(-self.market.Rate * self.TimeToMaturity)
        self.Forward = self.market.UndPrice * np.exp((self.market.Rate - 
                                                      self.market.DividendYield) * self.TimeToMaturity)
        self.Timestep = self.TimeToMaturity / self.NbSteps

    
    def priceThreeSchemas(self, opt: OptionTrade):
        #Fonction qui calcule les prix selon des deux schemas avec les memes browniens
        TimestepArray = np.ones((self.NbSteps,1))*self.Timestep
        #1e schema de discretisation
        V = np.ones((self.NbDraws))
        #2nd schema de discretisation
        Vexp = np.ones((self.NbDraws))
        
        for i in range( self.NbDraws):
            Br = Brownian()
            Mb = Br.generate(TimestepArray)
            
            #2nd schema de discretisation
            StExp = self.market.UndPrice
            StExp = StExp * np.exp((self.market.Rate - self.market.DividendYield - 0.5 * 
                                    ((self.market.Volatility) ** 2)) * self.TimeToMaturity + 
                                   self.market.Volatility * Mb[self.NbSteps-1,0])
            
            #1e schema de discretisation
            St = self.market.UndPrice
            St = St * (1 + (self.market.Rate - self.market.DividendYield)*self.Timestep + 
                       self.market.Volatility *Mb[0,0])
            for j in range(1, self.NbSteps):
                St = St * (1 + (self.market.Rate - self.market.DividendYield)*self.Timestep + 
                           self.market.Volatility * (Mb[j,0] - Mb[j-1,0]))
            
            #Utilisation de la fonction pay_off de la classe optionTrade
            V[i] = opt.pay_off(St)
            Vexp[i] = opt.pay_off(StExp)
        
        #Calcul des resultats (prix)
        result1 = np.mean(V) / ((1 + self.market.Rate * self.Timestep) ** self.NbSteps)
        result2 = np.mean(Vexp)*self.DiscountF

      
        return result1,result2


