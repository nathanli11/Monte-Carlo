import numpy as np
import numpy.random as npr


class Brownian:
    #Brownian class to generate brownian 
    def __init__(self, N=1):
        self.N = N  #Nombre de scénarios
        

    def generate(self, timestepArray):
        n = len(timestepArray)  #Nombre de pas de temps basé sur l'entrée times
        B = np.zeros((n, self.N))  #Création de la matrice de Brownien
       
        for j in range(self.N):
            B[0, j] += np.sqrt(timestepArray[0])* npr.randn()
            for i in range(1, n):  #Valeurs de 1 à n-1
                B[i, j] = B[i-1, j] + np.sqrt(timestepArray[i]) * npr.randn()
        
        return B
