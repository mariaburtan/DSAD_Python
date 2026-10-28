import numpy as np
import pandas as pd
from pandas.core.dtypes.common import is_numeric_dtype


def nan_replace_df(df:pd.DataFrame):
    for col in df.columns:
        if df[col].isna().any(): #intoarce obiect serie df[col] fiecare coloana este vazuta ca o serie isna e o metoda serie care intoarce o alta serie true/false in fct de ce gaseste in serie. any este metoda din serie acre intoarce true daca exista cel putin o valoare
            if is_numeric_dtype(df[col]):
                df.fillna({col:df[col].mean()},inplace=True)
            else:
                df.fillna({col: df[col].mode()[0]}, inplace=True)

def acp(x:np.ndarray,std=True,nlib=0):
#trimit var booleana sa vedem daca e standardizat sau nu
    #datele brute se centreaza (daca modelul nu e standardizat)
    n,m=x.shape
    x_=x-np.mean(x,axis=0) #medii pe coloana functia - se scade media coloanei anterioare?
#determinare tabel centrat

#daca avem standardizare
    if std==True:
        x_=x_/np.std(x_,axis=0) #fiecare coloana se imparte la standardizarea sa

    r_v = (1/(n-nlib)) * x_.T @ x_
# r - matrice corelatie; v - matrice covarianta

#@ - inmultire matriceala
    valp,vecp=np.linalg.eig(r_v) #valori_proprii_vecp
    print(valp,vecp,sep='\n')

    valp=np.real(valp)
    vecp=np.real(vecp)

#mutam si coloanele dupa indici (argsort??)
    k=np.flip(np.argsort(valp)) #sortare in ordine crescatoare, nu stie descrescatoare, altfel inversez vectorul - flip

    print(k)
#dupa indixi, construiesc alt vector de valori proprii ordonat dupa indecsi

    alpha=valp[k]

    #matrice a
    a=vecp[:,k] #vecp vectori coresp valorilor proprii

    c=x_@a

    return x_,r_v,alpha,a,c
#matrice centrata sau std, matrice cor si cov, alpha, val proprii ce repr val comp, saturatii, matr componenta

#                                   ANALIZA VARIANTEI COMPONENTELOR

#construim tabel, grafic, interpretari

#tabelarea variantei
#o col cu varianta comp, var cuplata, procent varianta, procent cumulat


def tabelare_varianta(alpha:np.ndarray):
    #a treia coloana
    procent=alpha*100/sum(alpha)
    df=pd.DataFrame(
        {  # folosim un dictionar date si nr coloane si separat o lista cu nr de instanta - etichete componente

            # dictionar
            "Varianta": alpha,
            "Varianta cumulata": np.cumsum(alpha),  # a doua coloana
            # primu elemnt din vect, al doilea a1+a2, al treilea a1+a2+a3, ultima suma de restu
            "Procent varianta": procent,
            "Procent cumulat": np.cumsum(procent)
        }, ['C'+str(i+1) for i in range(len(alpha))]
    )
    df.index.name="Componente"
    return df

















