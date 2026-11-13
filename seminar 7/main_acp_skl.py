import sys

import numpy as np
import pandas as pd
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

from functii7 import nan_replace_df, acp, tabelare_varianta, tabelare_salvare_matrice
from grafice7 import plot_varianta, heat_plot, show, corelograma, scatter_plot

pd.set_option('display.max_columns', None)
np.set_printoptions(suppress=True, precision=3, threshold=sys.maxsize)

df = pd.read_csv("data_in/GrupeDeSange/GrupeSanguineRH.csv",
                 index_col=0)
if df.isna().any().any():
    nan_replace_df(df)

variabile_observate = list(df.columns.values)[2:-1]
#print(variabile_observate)

x = df[variabile_observate].values #datele normale

#           STANDARDIZARE
standardizare=True
if standardizare:
    scalare=StandardScaler()
    x_=scalare.fit_transform(x) #matricea standardizata
else:
    x_=x


#       MODEL ACP       PCA - principal component analysis
model_acp=PCA()

model_acp.fit(x_) #calculeaza parametrii modelului
alpha=model_acp.explained_variance_
print(alpha)
