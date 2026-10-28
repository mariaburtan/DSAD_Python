import pandas as pd

df_confesiuni = pd.read_csv('data_in/Religious.csv', index_col=0) #na_values
#print(df_confesiuni,type(df_confesiuni));

confesiuni=list(df_confesiuni)[1:] #facem o lista de la a doua coloana in colo
#sa inlocuim valorile lipsa

#to_list metoda
df_coduri_loc=pd.read_csv('data_in/Coduri_Localitati.csv', index_col=0)
df_confesiuni_loc=df_confesiuni[confesiuni].merge(df_coduri_loc, left_index=True, right_index=True)
#df referinta data frame tip viziune, preia

df_confesiuni_jud=df_confesiuni_loc[confesiuni+["County"]].groupby(by=['County']).sum()
#intre paranteze patrate pt initializatorul de lista
df_confesiuni_jud.to_csv('data_out/Confesiuni_jud.csv')


#facem join judete cu regiuni
df_coduri_jud=pd.read_csv('data_in/Coduri_Judete.csv',index_col=0)
df_confesiuni_jud_reg=df_confesiuni_jud.merge(df_coduri_jud, left_index=True, right_on="IndicativJudet") #creem pe baza cheii IndicativJudet
print(df_coduri_jud.columns)
print(df_coduri_jud.index.name)
print(df_coduri_jud.head())

df_confesiuni_reg=df_confesiuni_jud_reg[confesiuni+["Regiune"]].groupby(by=['Regiune']).sum()
df_confesiuni_reg.to_csv('data_out/Confesiuni_reg.csv')


#TEMA PE MACROREGIUNI
df_confesiuni_p=df_confesiuni[confesiuni].apply(lambda x:x*100/x.sum(),axis=1) #apply este aplicat pe serii; functia produce ponderea

print(df_confesiuni_p)

df_confesiuni_p.insert(0,"Localitate", df_confesiuni["City"])
df_confesiuni_p.to_csv('data_out/Confesiuni_p.csv')

df_confesiuni_p=df_confesiuni_jud[confesiuni].apply(func=lambda x:x*100/x.sum(),axis=1)
df_confesiuni_p.to_csv('data_out/Confesiuni_jud_p.csv')


