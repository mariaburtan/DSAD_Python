# tema 1.1
# În fișierul Teritorial_2022.csv sunt date privind indicatori statistici din diverse domenii si
# subdomenii economico-sociale. Să se implementeze următoarele cerințe:
# - Înlocuirea valorilor lipsă cu media
# - Standardizarea și centrarea datelor
# - Calculul matricelor de corelație și covarianță totale și pe grupe (dacă există criteriu de grupare)
import sys

import numpy as np
import pandas as pd

from functii import *
from sklearn.preprocessing import StandardScaler

np.set_printoptions(precision=3, suppress=True, threshold=sys.maxsize)

# returneaza un obiect tip data frame, df extensie de dictionar
df = pd.read_csv("data.in/Teritorial_2022.csv", index_col=0)
# index col - index de linie

variabile=list(df)[3:] #constructorul lui list preia cheile (numele coloane) si valorile (coresp coloanelor)
#de la 3 pana la final

x=df[variabile].values #selectie pe baza listei, extragem valorile (viziune/referinta) la selectie
#values fix la valori
#print(x,type(x),sep="\n")

#inlocuire valori lipsa
x= nan_replace(x)
print(x)


# cerinta 2
x_std=standardizare(x)
x_c=standardizare(x,scal=False)


#salvare matrice standardizata
tabelare_salvare_matrice(x_std, df.index, variabile, df.index.name, "x_std.csv")

#pt matrice centrata
tabelare_salvare_matrice(x_c, df.index, variabile, df.index.name, "x_c.csv")

#standardizare date
std=StandardScaler()
x_std_=std.fit_transform(x)

print(x_std-x_std_) #diferenta dintre calcule este 0


# cerinta 3

#impartire pe clase regiune si macro regiune

#pt matricea de corelatie si covarianta

#covarianta
V=np.cov(x,rowvar=False)
tabelare_salvare_matrice(V, variabile, variabile, "Indicatori", "v.csv")
#index linie = index coloana

#corelatie
R = np.corrcoef(x,rowvar=False)
tabelare_salvare_matrice(R, variabile, variabile, "Indicatori", "r.csv")

#despachetarea tuplului in obiecte
r,v,clase =calcul_corelatii_covariante(x,df["Regiunea"].values)


#salvare direct in fisier csv in data.out

for i in zip(clase, r,v):
    #ffct zip creaza lista cu tuplu de elem liniare
#vect matrici, coloane???
    #fara intoarcere rezultat
    tabelare_salvare_matrice(i[1], variabile, variabile, "Indicatori", "R_"+i[0]+".csv") #i[0] e centru

    tabelare_salvare_matrice(i[2], variabile,variabile, "Indicatori", "V_"+i[0]+".csv")


