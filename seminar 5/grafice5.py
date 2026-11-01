import numpy as np
import pandas as pd
from seaborn import heatmap

from matplotlib import pyplot as plt

def plot_varianta(alpha:np.ndarray,std=True,P=80):
#nr de componente standardizate tb sa ajunga la un anume procent din
    #construim container
    fig=plt.figure(figsize=(8,6))
    ax=fig.add_subplot(1,1,1)
    ax.set_title("Plot_varianta",fontdict={'fontsize':16})
    ax.set_xlabel("Componenta",fontdict={'fontsize':12,'color':'b'})

    ax.set_ylabel("Varianta", fontdict={'fontsize': 12, 'color': 'b'})


    m=len(alpha)
    x = np.arange(1, m + 1)
    ax.plot(x,alpha)
    ax.set_xticks(x)
    ax.scatter(x,alpha,color='r',alpha=0.5)
#Criterii de selectie a componentelor semnificative
#Criteriul acoperirii simple

    procent=np.cumsum(alpha*100/sum(alpha))
    k1=np.where(procent>P)[0][0]+1

#trasare linie orizontale
    ax.axhline(alpha[k1-1],color='g',label='Varianta acoperita > ' +str(P))

    #Kaiser
    if std:
        k2=np.where(alpha>1)[0][-1]+1
        ax.axhline(1,color='c',label='Kaiser')
    else:
        k2=None

    #seminar 5
    eps=alpha[:m-1] - alpha[1:] #de la 1 pana la sfarsit
    d=eps[:m-2]-eps[1:]

    if np.any(d<0):
        k3=np.where(d<0)[0][0]+2 # produce un tuplu, indicii vectorului coresp valorilor <0
    # ca sa extrag primul element din vector si +1 ptc s-au decalat elementele
    # + 2
    # [ 1.766  0.093 -0.078  0.146 -0.096 -0.152  0.244 -0.03  -0.102]
    # [2,4,5,7,8]
        print(k3)
        ax.axhline(alpha[k3-1],color='m',label='Cattel (punct elbos)')



    #marcam in grafic

    print(eps)
    print(d)


    ax.legend()
    #ax.plot(alpha)
    #plt.show() #vizualizeaza in fereastra modala
    #return k1,k2, k3
    return {"Varianta":k1,"Kaiser":k2,"Cattell":k3}

def show():
    plt.show()

def corelograma(df:pd.DataFrame, titlu='Corelatii factoriale', vmin=1, annot=True,cmap="RdYLBu"): #val min si max pt intercorelare?

    fig=plt.figure(figsize=(9,6))
    ax=fig.add_subplot(1,1,1)
    ax.set_title(titlu,fontdict={'fontsize':16})
    heatmap(df, vmin=vmin, vmax=1,annot=annot,ax=ax)

def scatter_plot(df:pd.DataFrame,titlu="Scoruri",ax_x="C1",ax_y="C2",etichetare=True, corelatii=False): #scoruri sau corelatii intre componente si variabile
    #desenare fara param
    #defineste raport inaltime si latime
    fig=plt.figure(figsize=(9,6))
    ax=fig.add_subplot(1,1,1,aspect=1)
    ax.set_title(titlu,fontdict={"fontsize":16})
    ax.set_xlabel(ax_x,fontdict={"fontsize":12,"color":'b'})
    ax.set_ylabel(ax_y,fontdict={"fontsize":12,"color":'b'})
    ax.scatter(df[ax_x],df[ax_y],c="r",alpha=0.5)
    if corelatii:
        pas=0.05
        tetha=np.arange(0,2*np.pi,pas)
        ax.plot(np.cos(tetha),np.sin(tetha))
        ax.plot(0.7*np.cos(tetha),0.7*np.sin(tetha),color="g")

        ax.axhline(0,color="b")
        ax.axvline(0,color="b")

    if etichetare:
        n=len(df)
        for i in range(n):
            ax.text(df[ax_x].iloc[i],df[ax_y].iloc[i],df.index[i])