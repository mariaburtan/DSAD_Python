from idlelib.colorizer import color_config

import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from seaborn import heatmap


def plot_varianta(alpha:np.ndarray, standardizare=True, P=80):
    fig = plt.figure("Plot varianta",figsize=(10,6))
    ax = fig.add_subplot(1,1,1)
    ax.set_title("Plot varianta",
                 fontdict={"fontsize":16,"color":"b"})
    m = len(alpha)
    x = np.arange(1,m+1)
    ax.set_xticks(x)
    ax.plot(x,alpha)
    ax.set_xlabel("Componenta",fontdict={"fontsize":12,"color":"b"})
    ax.set_ylabel("Varianta",fontdict={"fontsize":12,"color":"b"})
    ax.scatter(x,alpha,color="r",alpha=0.5)
    # Aplicare criterii
    # Criteriul variantei minimale
    procent = np.cumsum(alpha*100/sum(alpha))
    k1 = np.where(procent>P)[0][0] + 1
    ax.axhline(alpha[k1-1],color="g",label="Varianta explicata > "+str(P))
    # Kaiser
    if standardizare:
        k2 =len(np.where(alpha>1)[0])
        ax.axhline(1,color="k",label="Kaiser")
    else:
        k2 = None
    # Cattell (Elbow)
    eps = alpha[:m-1] - alpha[1:]
    d = eps[:m-2] - eps[1:]
    # print(alpha,eps,d,sep="\n")
    if np.any(d<0):
        k3 = np.where(d<0)[0][0] + 2
        # print(k3)
        ax.axhline(alpha[k3-1], color="c", label="Cattell (Punct elbow)")
    else:
        k3 = None
    ax.legend()
    return {"Varianta":k1,"Kaiser":k2,"Cattell":k3}

def show():
    plt.show()

def corelograma(df:pd.DataFrame,titlu="Corelatii factoriale",vmin=-1,cmap="RdYlBu",annot=True,vmax=1):
    fig = plt.figure(titlu,figsize=(10,6))
    ax = fig.add_subplot(1,1,1)
    ax.set_title(titlu,fontdict={"fontsize":16,"color":"b"})
    heatmap(df,ax=ax,vmin=vmin,cmap=cmap,annot=annot,vmax=vmax)

#seminar 7
def heat_plot(df:pd.DataFrame,titlu="Corelatii factoriale",vmin=-1,cmap="RdYlBu",annot=True, pas=30,vmax=1):
    #pas - cate instante vizualizez deodata
    n=len(df)
    l=[i for i in range(0,n,pas)] # de la 0 la n folosim pasul
    #ultima valoare nu e inclusa
    l.append(n)
    for i in range(1,len(l)):
        corelograma(df.iloc[l[i-1]:l[i]],titlu+"("+str(l[i-1])+":"+str(l[i])+").",vmin,cmap,annot,vmax)
        #ii dau liniile din DataFrame de la


def scatter_plot(
        df:pd.DataFrame,eticheta_x="C1",eticheta_y="C2",
        titlu="Plot scoruri",corelatii=False,etichetare=True):
    fig = plt.figure(titlu+"-"+eticheta_x+","+eticheta_y,figsize=(10,6))
    ax = fig.add_subplot(1,1,1,aspect="equal")
    ax.set_title(titlu,fontdict={"fontsize":16,"color":"b"})
    ax.set_xlabel(eticheta_x,fontdict={"fontsize":12,"color":"b"})
    ax.set_ylabel(eticheta_y,fontdict={"fontsize":12,"color":"b"})
    ax.scatter(df[eticheta_x],df[eticheta_y],color="r",alpha=0.5)
    ax.axvline(0, color="k", linestyle="--")
    ax.axhline(0, color="k", linestyle="--")
    if corelatii:
        tetha = np.arange(0,2*np.pi+0.05,0.05)
        ax.plot(np.cos(tetha),np.sin(tetha))
        ax.plot(0.7*np.cos(tetha), 0.7*np.sin(tetha))
    if etichetare:
        n = len(df)
        for i in range(n):
            ax.text(df[eticheta_x].iloc[i],df[eticheta_y].iloc[i],df.index[i])