import numpy as np

from matplotlib import pyplot as plt

def plot_varianta(alpha:np.ndarray,std=True,P=00):
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


    ax.legend()
    #ax.plot(alpha)
    #plt.show() #vizualizeaza in fereastra modala
    return k1,k2

def show():
    plt.show()