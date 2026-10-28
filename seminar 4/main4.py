import sys

import numpy as np
import  pandas as pd

np.set_printoptions(suppress=True,precision=3,threshold=sys.maxsize)

from grafice import *
from functii4 import *

df=pd.read_csv("data_in/ConsumAlimentar/ConsumAlimentar.csv",index_col=0)

if df.isna().any().any():
    #exista valori
    nan_replace_df(df)

variabile_observate=list(df)[1:] #de la 1 incolo
x=df[variabile_observate].values
x_,r_v,alpha,a,c=acp(x)


#matrice centrata sau std, matrice cor si cov, alpha, val proprii ce repr val comp, saturatii, matr componenta

#                                   ANALIZA VARIANTEI COMPONENTELOR

#construim tabel, grafic, interpretari

#tabelarea variantei
#o col cu varianta comp, var cuplata, procent varianta, procent cumulat


df_varianta=tabelare_varianta(alpha)
df_varianta.round(3).to_csv("data_out/Varianta.csv")

#Analiza varianteo componente;pr
#tabelarea variantei
plot_varianta(alpha)

show()