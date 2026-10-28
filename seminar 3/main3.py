import numpy as np
import pandas as pd

#functia de la cerinta 5

def calcul_medie(df:pd.DataFrame):
    x=df.values
    medie = np.average(x[:, :-1], axis=0, weights=x[:, -1])
    return pd.Series(medie,df.columns[:-1])


df_industrie_alimentara = pd.read_csv("data_in/IndustriaAlimentara.csv", index_col=0)
activitati = list(df_industrie_alimentara.columns.values)[1:]

#cerinta 1
#localitatile cu nr de angajati per industrie>0

s_totaluri = df_industrie_alimentara[activitati].sum(axis=1)
print(s_totaluri)
df_cerinta1=df_industrie_alimentara[s_totaluri>0]
#intoarce serie de tip boolean

df_cerinta1.to_csv("data_out/Cerinta1.csv")

#cerinta 2
#procent de angajati pe fiecare activitate
df_industrie_alimentara["Total"]=s_totaluri

df_cerinta2=df_industrie_alimentara[activitati].apply(
    func = lambda x: x/x.sum() ,
    axis=1
)

print(df_cerinta2.head(3))

df_cerinta2.insert(0,"Localitate", df_industrie_alimentara["Localitate"])
df_cerinta2.to_csv("data_out/Cerinta2.csv")

#cerinta 3

#calculare pondere in pop totala

df_populatie=pd.read_csv("data_in/PopulatieLocalitati.csv",index_col=0)
df_industrie_alimentara_populatie=df_industrie_alimentara.merge(df_populatie[["Judet","Populatie"]], left_index=True, right_index=True)
s_cerinta3=df_industrie_alimentara["Total"]/df_industrie_alimentara_populatie["Populatie"]
s_cerinta3.name="Pondere"
s_cerinta3.round(5).to_csv("data_out/Cerinta3.csv")

#cerinta 4
#pt fiecare judet ce industrie e mai importanta (cu cei mai multi angajati)

df_industrie_alimentara_judet=df_industrie_alimentara_populatie[activitati+["Judet","Populatie"]].groupby(by="Judet").sum()
print(df_industrie_alimentara_judet.head(3))

#pe ce coloana inregistram maximul
s_cerinta4=df_industrie_alimentara_judet[activitati].apply(
    lambda x: x.index[x.argmax()],
    axis=1
)

s_cerinta4.name="Activitate"
s_cerinta4.to_csv("data_out/Cerinta4.csv")

#cerinta5
#grupare la nivel de regiuni
df_coduri=pd.read_csv("data_in/Coduri_Judete.csv",index_col=0)
#jonctiune intre
#localitate
df_industrie_alimentara_localitate_regiune=df_industrie_alimentara_populatie.merge(df_coduri, left_on="Judet", right_index=True)

print(df_industrie_alimentara_localitate_regiune.head(3))

df_cerinta5=df_industrie_alimentara_localitate_regiune[activitati+["Regiune","Populatie"]].groupby(by="Regiune").apply(
    func = calcul_medie,
    include_groups=False
)

df_cerinta5.to_csv("data_out/Cerinta5.csv")
