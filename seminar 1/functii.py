import numpy as np
import pandas as pd


def nan_replace(x:np.ndarray):
    #o sa o facem sa nu lucreze direct pe x
    x=x.copy() #x copie matrice si intoarce referinta
    #identificam valorile lipsa
    #k=np.isnan(x)
    k=np.where(np.isnan(x)) #isnan produce matrice, index linie si coloana, tuplu cu 2 vect
    x[k]=np.nanmean(x[:,k[1]], axis=0) #furnizeaza valoare pt fiecare element lipsa
    #mean tine cont si de val lipsa
    #axis - cum se face calculul pe intreaga matrice, linie sau coloana (0)
    #print(k)
    return x

#centrare, centralizare
#variabila booleana care sa spuna daca face una din cele doua
#populatie cu n grade de libertate (n, n-1)??
def standardizare(x:np.ndarray,scal:bool=True, nlib=0):
    #mai intai centrare
# matricea centrata
    x_=x - np.mean(x,axis=0)
    #primul elem e matrice, a doilea vector (tb sa fie egale nr de coloane???) conventie

    #standardizare
    if scal:
        x_=x_/np.std(x_,axis=0, ddof=nlib) #nu trateaza gradele de libertate, ddof does, nu 1 ci nlib
    return x_


#salvare rez
def tabelare_salvare_matrice(x:np.ndarray, index_linie, index_coloana, nume_index_linie, nume_fisier=None):
    df=pd.DataFrame(x,index=index_linie, columns=index_coloana)
    #nume de index
    df.index.name=nume_index_linie
    if nume_fisier is not None:
        #treb sa fac salvare
        df.to_csv("data.out/"+nume_fisier)

def calcul_corelatii_covariante(x:np.ndarray,y:np.ndarray):
    #trimitem coloana si dam split pe date reg sau macro reg

    #y var calitativa
    #determinam nr claselor
    clase=np.unique(y) #ia coloana si determ valori unice
    q=len(clase)
    m=x.shape[1]

    #structura tridimensionala pt corelatii si indiv covariatii

    r=np.empty((q,m,m)) #automat float
    v=np.empty((q,m,m))

    #calc indiv
    for i in range(q):
        #extragem matricea coresp regiunii i
        z=x[y==clase[i],:] #y e regiunea, luam doar liniile
        r[i]=np.corrcoef(z,rowvar=False)
        v[i]=np.cov(z,rowvar=False)

    return r,v, clase #impachetare in tuplu