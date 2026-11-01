import sys

import numpy as np
import  pandas as pd

from grafice5 import *

np.set_printoptions(suppress=True,precision=3,threshold=sys.maxsize)

from functii5 import *

df=pd.read_csv("data_in/ConsumAlimentar/ConsumAlimentar.csv",index_col=1)

if df.isna().any().any():
    #exista valori
    nan_replace_df(df)

model_standardizat=True

variabile_observate=list(df)[1:] #de la 1 incolo
x=df[variabile_observate].values

n,m= x.shape

x_,r_v,alpha,a,c=acp(x,model_standardizat)


#matrice centrata sau std, matrice cor si cov, alpha, val proprii ce repr val comp, saturatii, matr componenta

#                                   ANALIZA VARIANTEI COMPONENTELOR

#construim tabel, grafic, interpretari

#tabelarea variantei
#o col cu varianta comp, var cuplata, procent varianta, procent cumulat

#Analiza varianteo componente;pr
#tabelarea variantei
df_varianta=tabelare_varianta(alpha)
df_varianta.round(3).to_csv("data_out/Varianta.csv")


#seminar 5

#Aplicare criterii de selectie si plot varianta
criterii=plot_varianta(alpha, model_standardizat)
print(criterii,model_standardizat)

numar_componente=min((v for v in criterii.values() if v is not None))
print('Numar componente selectate:', numar_componente)

#Analiza corelatiilor factoriale
#pentru model standardizat
if model_standardizat:
    r=a*np.sqrt(alpha) #a vector val proprii?
else: #model standardizat, calculare manuala
    r=np.corrcoef(x_,c,rowvar=False)[:m,m:] # c matrice componenta #nu sunt asezate pe linii,ci coloane
print(r)

#Analiza pe baza de tabele si output?
#pt matricea corelatiilor tabelare

df_r=tabelare_salvare_matrice(
    r,
    variabile_observate,
    df_varianta.index,
    'Variabile ' #index de linie se refera la variabile
    #pe linie numele variab observate
    #pe coloana etichetele de coloana
    'R.csv'
)

corelograma(df_r)

for i in range(2,numar_componente+1): #inclusiv
    scatter_plot(df_r, "Corelatii factoriale",ax_y='C'+str(i) ,corelatii=True)

show()