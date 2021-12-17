import streamlit as st
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
import plotly.graph_objects as go
import plotly.express as px
import matplotlib.pyplot as plt
import json

#start handler
class csvHandler:
    def __init__(self,fileName):
        self.fileName = fileName
        df = pd.read_csv(fileName)
        self.data = {}
        for i in df:
            self.data[i]=df[i].tolist()
        self.dataFrame = df
    def csvToJson(self,jsonFile):
        df = pd.read_csv(self.fileName)
        li = []
        for i in range(len(df)):
            row = {}
            for j in df:
                try :
                    a = float(df[j][i])
                except:
                    a = str(df[j][i]) 
                row[j] = a
            li.append(row)
        with open("{}.json".format(jsonFile), "w") as write_file:
            json.dump(li,write_file)

class jsonHandler:
    def __init__(self,fileName):
        self.fileName = fileName
        with open(fileName, "r") as read_file:
            self.data = json.load(read_file)
        dic = {}
        key_li = list(self.data[0].keys())
        for key in key_li:
            dic[key] = []
        for i in self.data:
            for key in key_li:
                dic[key].append(i[key])
        self.dataFrame = pd.DataFrame(dic)
    def jsonToCsv(self,csvFile):
        self.dataFrame.to_csv('{}.csv'.format(csvFile),index=False)
#end handler

st.set_page_config(layout="wide")

st.title('PRODUKSI MINYAK MENTAH')
#st.header('Feriyanto 12220007')
ch_ = csvHandler('produksi_minyak_mentah.csv')
jh_ = jsonHandler('kode_negara_lengkap.json')

st.sidebar.title("Pengaturan")
left_col, right_col = st.columns(2)


#bagian a
left_col.header('Bagian A')
df_ = ch_.dataFrame
df_info = jh_.dataFrame
negara_li = df_info['name'].tolist()

negara = left_col.selectbox('Pilih negara : ',negara_li) 

kode = df_info[df_info['name']==negara]['alpha-3'].tolist()[0]


left_col.subheader('Kode negara : ',kode)
left_col.subheader('Negara : ',negara)

x_ = df_[df_['kode_negara']==kode]['tahun'].tolist()
y_ = df_[df_['kode_negara']==kode]['produksi'].tolist()

reg = LinearRegression()
reg.fit(np.array(x_).reshape(-1,1),np.array(y_))
m = reg.coef_[0]
c = reg.intercept_
y_trend = [m*x+c for x in x_]
if c >= 0:
    equation = 'y={m:.2f}x+{c:.2f}'.format(m=m,c=c)
else:
    equation = 'y={m:.2f}x{c:.2f}'.format(m=m,c=c)

dic = {'tahun':x_,'produksi':y_}
left_col.subheader("Tabel produksi minyak mentah ",negara)
left_col.dataframe(dic)
#st.write(pd.DataFrame(dic))

#plotting = left_col.selectbox('Pilih tipe plotting : ',['tipe 1','tipe 2'])

dic['trendline'] = y_trend
fig = px.scatter(pd.DataFrame(dic),x='tahun',y='produksi',trendline='lowess',trendline_options=dict(frac=0.1),title='Data Produksi {}'.format(negara))
right_col.subheader('Data Produksi',negara)
right_col.plotly_chart(fig)

#bagian b
#col2
st.write()
st.write()
left_col.header('Bagian B')
left_col.subheader("Jumlah Produksi Minyak Mentah Terbesar")

B = st.sidebar.number_input("Banyak negara dengan jumlah produksi terbesar (Bagian B)", min_value=1, max_value=None)
T = st.sidebar.number_input("Tahun produksi (Bagian B)", min_value=1971, max_value=2015)

df = df_
dfJ = df_info

df = df[df['tahun']==T]
kode_negara = df[df['tahun']==T]['kode_negara'].tolist()
# produksi = df[df['tahun']==T]['produksi'].tolist()

produksi_maks = []
negara_pertahun = []

kode_negara = list(dict.fromkeys(kode_negara))
for kode in kode_negara:
    try:
        produksi = df[df['kode_negara']==kode]['produksi'].tolist()
        negara = dfJ[dfJ['alpha-3']==kode]['name'].tolist()[0]
        produksi_maks.append(max(produksi))
        negara_pertahun.append(negara)
    except:
        continue
        
dic = {'negara':negara_pertahun,'produksi_maks':produksi_maks}
df__ = pd.DataFrame(dic)
df__ = df__.sort_values('produksi_maks',ascending=False).reset_index()

plt.clf() # clear the figure

#tulisan nanti lu aja ya, gua update ke github dulu

plt.title('{B} Negara dengan Produksi Terbesar pada Tahun {T}'.format(B=B,T=T))
plt.bar(df__['negara'][:B],df__['produksi_maks'][:B],width=0.9, bottom=None, align="center",
            color="green", edgecolor="aquamarine", data=None, zorder=3)
plt.grid(True, color="grey", linewidth="0.7", linestyle="-.", zorder=0)
#plt.xlabel()
plt.ylabel('produksi_maksimum')
plt.xticks(rotation=30, ha='right')

#st.write('Input banyak negara dan tahun di kiri')
left_col.pyplot(plt)

#bagian c
#col3
st.write()
right_col.subheader("Bagian C")
right_col.subheader('Jumlah Produksi Terbesar Kumulatif Keseluruhan Tahun')

B_ = st.sidebar.number_input("Banyak negara dengan produksi terbesar kumulatif (Bagian C)", min_value=1, max_value=None)

df = df_
dfJ = df_info

kode_negara = df['kode_negara'].tolist()
kode_negara = list(dict.fromkeys(kode_negara))

produksi_total = []
negara_ = []

for kode in kode_negara:
    try:
        produksi = df[df['kode_negara']==kode]['produksi'].tolist()
        negara = dfJ[dfJ['alpha-3']==kode]['name'].tolist()[0]
        produksi_total.append(np.sum(np.array(produksi)))
        negara_.append(negara)
    except:
        continue
        
dic = {'negara':negara_,'produksi_total':produksi_total}
df__ = pd.DataFrame(dic)
df__ = df__.sort_values('produksi_total',ascending=False).reset_index()

plt.clf() # clear the figure

#tulisan nanti lu aja ya, gua update ke github dulu

plt.title('{B} Negara dengan Produksi Terbesar Kumulatif'.format(B=B_))
plt.bar(df__['negara'][:B_],df__['produksi_total'][:B_],width=0.9, bottom=None, align="center",
            color="green", edgecolor="aquamarine", data=None, zorder=3)
plt.grid(True, color="grey", linewidth="0.7", linestyle="-.", zorder=0)
#plt.xlabel()
plt.ylabel('produksi_total')
plt.xticks(rotation=30, ha='right')

st.write('Input banyak negara di sidebar kiri (Bagian C)')
right_col.pyplot(plt)

#bagian d
st.write()
st.write()
st.header('Bagian D')
st.subheader('INFORMASI')

T_ = st.sidebar.number_input("Summary Tahun Produksi", min_value=1971, max_value=2015)

df = ch_.dataFrame
dfJ = jh_.dataFrame

tahun = list(dict.fromkeys(df['tahun'].tolist()))

dic_maks = {'negara':[],
            'kode_negara':[],
            'region':[],
            'sub_region':[],
            'produksi':[],
            'tahun':tahun}
dic_min = {'negara':[],
            'kode_negara':[],
            'region':[],
            'sub_region':[],
            'produksi':[],
            'tahun':tahun}
dic_zero = {'negara':[],
            'kode_negara':[],
            'region':[],
            'sub_region':[],
            'produksi':[],
            'tahun':tahun}

for t in tahun:
    df_per_tahun = df[df['tahun']==t]
    produksi = np.array(df_per_tahun['produksi'].tolist())
    maks_prod = max(produksi)
    min_prod = min([p for p in produksi if p != 0])
    zero_prod = min([p for p in produksi if p == 0])
    # maksimum
    kode_negara = df_per_tahun[df_per_tahun['produksi']==maks_prod]['kode_negara'].tolist()[0]
    if kode_negara == 'WLD':
        kode_negara = 'WLF'
    dic_maks['negara'].append(dfJ[dfJ['alpha-3']==kode_negara]['name'].tolist()[0])
    dic_maks['kode_negara'].append(kode_negara)
    dic_maks['region'].append(dfJ[dfJ['alpha-3']==kode_negara]['region'].tolist()[0])
    dic_maks['sub_region'].append(dfJ[dfJ['alpha-3']==kode_negara]['sub-region'].tolist()[0])
    dic_maks['produksi'].append(maks_prod)
    # minimum != 0
    kode_negara = df_per_tahun[df_per_tahun['produksi']==min_prod]['kode_negara'].tolist()[0]
    if kode_negara == 'WLD':
        kode_negara = 'WLF'
    dic_min['negara'].append(dfJ[dfJ['alpha-3']==kode_negara]['name'].tolist()[0])
    dic_min['kode_negara'].append(kode_negara)
    dic_min['region'].append(dfJ[dfJ['alpha-3']==kode_negara]['region'].tolist()[0])
    dic_min['sub_region'].append(dfJ[dfJ['alpha-3']==kode_negara]['sub-region'].tolist()[0])
    dic_min['produksi'].append(min_prod)
    # zero == 0
    kode_negara = df_per_tahun[df_per_tahun['produksi']==zero_prod]['kode_negara'].tolist()[0]
    if kode_negara == 'WLD':
        kode_negara = 'WLF'
    dic_zero['negara'].append(dfJ[dfJ['alpha-3']==kode_negara]['name'].tolist()[0])
    dic_zero['kode_negara'].append(kode_negara)
    dic_zero['region'].append(dfJ[dfJ['alpha-3']==kode_negara]['region'].tolist()[0])
    dic_zero['sub_region'].append(dfJ[dfJ['alpha-3']==kode_negara]['sub-region'].tolist()[0])
    dic_zero['produksi'].append(zero_prod)

df_maks = pd.DataFrame(dic_maks)
df_min = pd.DataFrame(dic_min)
df_zero = pd.DataFrame(dic_zero)

st.write('Info Produksi Maksimum Tahun ke-{}'.format(T_))
st.write(df_maks[df_maks['tahun']==T_])

st.write('Tabel Maks per Tahun')
st.write(df_maks)

st.write('Info Produksi Minimum (Not Zero) Tahun ke-{}'.format(T_))
st.write(df_min[df_min['tahun']==T_])

st.write('Tabel Min (Not Zero) per Tahun')
st.write(df_min)

st.write('Info Produksi Zero Tahun ke-{}'.format(T_))
st.write(df_zero[df_zero['tahun']==T_])

st.write('Tabel Zero per Tahun')
st.write(df_zero)
