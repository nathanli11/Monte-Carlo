#Importing imports and librairies
import xlwings
import numpy
from modelMC import MCModel
from optionTrade import OptionTrade
from market import Market
import datetime
import time
import pandas as pd


# range formula that returns the price of an option with a Monte-Carlo pricer
@xlwings.func(volatile=True)
@xlwings.arg('pricer_range', numpy.array)
@xlwings.arg('option_range', numpy.array)
@xlwings.arg('market_range', numpy.array)
def OptionPriceMCPy(pricer_range: numpy.array, option_range: numpy.array, market_range: numpy.array) -> numpy.array:
    # instantiate option
    call_put: str = option_range[0]
    mat: datetime = option_range[2]
    k: float = option_range[1]
    option: OptionTrade = OptionTrade(call_put, mat, k, OptionTrade.EURO_LABEL)     # in this context, force the option to be European

    # instantiate market object
    UndPrice : float = market_range[0]
    Rate : float = market_range[2]
    Volatility : float = market_range[1]
    DividendYield : float = market_range[3]
    market: Market = Market(UndPrice,Volatility,Rate,DividendYield) 

    # instantiate pricer
    pr_date : datetime = pricer_range[0]
    Nbsteps : int = pricer_range[1]
    NbDraws : int = pricer_range[2]
    MCModel1: MCModel = MCModel(pr_date,market,NbDraws,Nbsteps)
    MCModel1.InitVariables(market=market,option=option)

    return MCModel1.priceThreeSchemas(option)


# used for debugging
if __name__ == '__main__':
   pass

#This part is used to call and run the code
#Option
Type_opt = 'Call'
Strike_K=100.00
Maturity='31/03/2025'

#Market
Stock_price_S=100.00
Volatility=0.2
interest_rate_r=0.03
Dividend_yield_q=0.02

#Pricer
Pricing_Date='22/03/2024'

market_range=numpy.array([Stock_price_S,Volatility,interest_rate_r,Dividend_yield_q],dtype=object)

Steps=[10**k for k in range(4)]
Draws=[10**k for k in range(6)]

np_schemas1_call=numpy.zeros((4,6))
np_schemas2_call=numpy.zeros((4,6))
np_schemas1_put=numpy.zeros((4,6))
np_schemas2_put=numpy.zeros((4,6))
np_times=numpy.zeros((4,6))


j=0
for draw in Draws:
    i=0
    for step in Steps:
        #Debut du timer
        debut=time.time()
        
        #Affectation des Nb_Draws et Nb_Steps
        Nb_Steps=step
        Nb_Draws=draw
        
        #Affectation du type de l option
        Type_opt = 'Call'
        
        #Affectation du pricer et de l option
        pricer_range=numpy.array([Pricing_Date,Nb_Steps,Nb_Draws],dtype=object)
        option_range=numpy.array([Type_opt,Strike_K,Maturity],dtype=object)
        
        #Calcul du prix
        prix=OptionPriceMCPy(pricer_range,option_range,market_range)
        np_schemas1_call[i,j]=prix[0]
        np_schemas2_call[i,j]=prix[1]
        
        #Affectation du type de l option
        Type_opt = 'Put'
        
        #Affectation de l option
        option_range=numpy.array([Type_opt,Strike_K,Maturity],dtype=object)
        
        #Calcul du prix
        prix=OptionPriceMCPy(pricer_range,option_range,market_range)
        np_schemas1_put[i,j]=prix[0]
        np_schemas2_put[i,j]=prix[1]
        
        #Calcul du temps d execution
        fin=time.time()
        np_times[i,j]=fin-debut
        i+=1
    j+=1
        
#Creation des tableaux avec les donnees pour la visualisation
tabl1=pd.DataFrame(np_schemas1_call,columns=Draws,index=Steps)
tabl2=pd.DataFrame(np_schemas2_call,columns=Draws,index=Steps)
tabl3=pd.DataFrame(np_schemas1_put,columns=Draws,index=Steps)
tabl4=pd.DataFrame(np_schemas2_put,columns=Draws,index=Steps)
tabl5=pd.DataFrame(np_times,columns=Draws,index=Steps)

#ecriture des resultats dans un fichier excel
filename = 'resultat.xlsx'
with pd.ExcelWriter(filename, engine='xlsxwriter') as writer:
    startrow = 0
    for i, df in enumerate([tabl1, tabl2, tabl3, tabl4, tabl5], start=1):
        # Écrire le dataframe
        df.to_excel(writer, sheet_name='Feuille1', startrow=startrow, index=True)
        
        # Ajout d'une ligne vide (ou plus) après chaque dataframe pour la séparation
        # Ajustez le nombre 2 ci-dessous pour ajouter plus ou moins d'espace
        startrow += len(df.index) + 2