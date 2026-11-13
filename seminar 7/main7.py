import sys

import numpy as np
import pandas as pd

from functii7 import nan_replace_df, acp, tabelare_varianta, tabelare_salvare_matrice
from grafice7 import plot_varianta, heat_plot, show, corelograma, scatter_plot

pd.set_option('display.max_columns', None)
np.set_printoptions(suppress=True, precision=3, threshold=sys.maxsize)

df = pd.read_csv("data_in/GrupeDeSange/GrupeSanguineRH.csv",
                 index_col=0)
if df.isna().any().any():
    nan_replace_df(df)

variabile_observate = list(df.columns.values)[2:-1]
# print(variabile_observate)

# std indica standardizare sau nu
standardizare = True
# Ajustare grade libertate
nlib = 0

x = df[variabile_observate].values
n,m = x.shape
x_, r_v, alpha, a, c = acp(x,standardizare, nlib=0)

# Analiza variantei componentelor
df_varianta = tabelare_varianta(alpha)
df_varianta.round(3).to_csv("data_out/Varianta.csv")

criterii = plot_varianta(alpha,standardizare)
print(criterii)
nr_componente = min([v for v in criterii.values() if v is not None])
print("Numar minim componente selectate:",nr_componente)

# Analiza corelatiilor factoriale
# Calcul corelatii
if standardizare:
    r = a*np.sqrt(alpha)
else:
    r = np.corrcoef(x_,c,rowvar=False)[:m,m:]
df_r = tabelare_salvare_matrice(
    r,variabile_observate,df_varianta.index,"Variabile","R.csv"
)
# print(r)
corelograma(df_r)
if nr_componente>1:
    for i in range(2,nr_componente+1):
        scatter_plot(df_r,eticheta_y="C"+str(i),corelatii=True,titlu="Corelatii factoriale")
else:
    scatter_plot(df_r,titlu="Corelatii factoriale")

# Analiza componente si scoruri
df_c = tabelare_salvare_matrice(c,df.index,df_varianta.index,df.index.name,"C.csv")
if nr_componente>1:
    for i in range(2,nr_componente+1):
        scatter_plot(df_c,eticheta_y="C"+str(i),titlu="Plot componente (ACP)")
else:
    scatter_plot(df_c,titlu="Plot componente (ACP)")

s = c/np.sqrt(alpha)
df_s = tabelare_salvare_matrice(s,df.index,df_varianta.index,df.index.name,"S.csv")
if nr_componente>1:
    for i in range(2,nr_componente+1):
        scatter_plot(df_s,eticheta_y="C"+str(i),titlu="Plot scoruri (ACP)")
else:
    scatter_plot(df_s,titlu="Plot scoruri (ACP)")

# Evaluare model. Metrici
# Cosinusuri
c2 = c*c
cosin = (c2.T / np.sum(c2,axis=1)).T
df_cosin = tabelare_salvare_matrice(cosin,df.index,df_varianta.index,df.index.name,"Cosin.csv")
#corelograma(df_cosin,"Cosinusuri",0,"Reds",annot=False)
heat_plot(df_cosin,"Valori cosinus",0,"Reds",False,vmax=1)

if nr_componente>1:
    for i in range(2,nr_componente+1):
        scatter_plot(df_cosin,eticheta_y="C"+str(i),titlu="Valori cosinus")
else:
    scatter_plot(df_cosin,titlu="Valori cosinus")

#       CONTRIBUTII
n=len(df)
contrib=(1/n)*c2/alpha

df_contrib=tabelare_salvare_matrice(contrib,df.index,df_varianta.index,df.index.name,"Contrib.csv")

heat_plot(df_contrib,"Contributii",0,"Blues",False,vmax=np.max(contrib))

if nr_componente>1:
    for i in range(2,nr_componente+1):
        scatter_plot(df_contrib,eticheta_y="C"+str(i),titlu="Contributii")
else:
    scatter_plot(df_contrib,titlu="Contributii")

#       COMUNALITATI    (variante extrase din x1,x1, dupa x1,x2, dupa x1,x3
#   pentru variabila j observata si primele k componente=suma(dupa i=1,k) din (R^2 de j si i

r2=r*r

#sume calculare sume progresive/cumulate
comunalitati=np.cumsum(r2,axis=1)
df_comm=tabelare_salvare_matrice(comunalitati,variabile_observate,df_c.columns,"Variabile","Comm.csv")

corelograma(df_comm,"Comunalitati",0,"Greens")

show()
