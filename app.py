# coding: utf-8
import streamlit as st
import pandas as pd
import altair as alt
import plotly.express as px
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

st.set_page_config(
    page_title="Monthly Report",
    page_icon="🚗",
    layout="wide",
)

st.title("🚗 Monthly Driver Report")

st.markdown("")
st.markdown("")

area_url = "https://raw.githubusercontent.com/seonseono/hackerthon_Baekkyung/refs/heads/main/data/data.csv"
@st.cache
def area_load_data():
    df_data = pd.read_csv(area_url, encoding='UTF8')
    return df_data
df_data = area_load_data()

with st.sidebar:
    st.title('✅ Driver ID')
    
    id_list = list(df_data.id.unique())[::-1]
    
    selected_id = st.selectbox('Select an ID', id_list, index=len(id_list)-1)
    df_selected_id = df_data[df_data.id == selected_id]
    # df_selected_id_sorted = df_selected_id.sort_values(by="id", ascending=False)


col = st.columns((7,3), gap='medium')

with col[0]:
    st.markdown('#### Abnormal Behavior Log')
    df_abnormal = df_selected_id.loc[df_selected_id.abnormal ==1, ['year', 'month', 'date', 'day', 'time', 'type']]
    df_abnormal.reset_index(drop=True, inplace=True)
    st.table(df_abnormal)

with col[1]:
    st.markdown('#### Driver Info')
    st.markdown("")
    df_info = df_selected_id[['id', 'driver_name', 'car_number', 'car_model']]
    unique_drivers = df_info.groupby('id').first().reset_index()
    unique_drivers = unique_drivers.drop(columns=['id'])
    unique_drivers.columns = ['driver name', 'car number', 'car model']
    st.table(unique_drivers)
    st.markdown("")
    st.markdown('#### Monthly Record')
    df_rate = df_selected_id[['id', 'abnormal', 'type']]
    df_rate['abnormal'] = df_rate['abnormal'].replace({0: 'normal', 1: 'abnormal'})
    abn_cnt = df_rate['abnormal'].value_counts()
    abn_rate = abn_cnt / abn_cnt.sum()*100
    labels = abn_rate.index
    sizes = abn_rate.values
    wedgeprops={'width': 0.7, 'edgecolor': 'w', 'linewidth': 5}

    plt.figure(figsize=(10, 10))
    plt.rc('font', size=30)
    plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90, counterclock=False, 
            pctdistance=0.85, colors=['#e7eedd', '#90d26d'], wedgeprops=wedgeprops)
    centre_circle = plt.Circle((0, 0), 0.5, fc='white')
    fig = plt.gcf()
    fig.gca().add_artist(centre_circle)
    plt.title("Abnormal Behavior Count")
    st.pyplot(fig)

    st.markdown("")
    st.markdown("")

    df_rate['type'] = df_rate['type'].replace({0:'normal', 1:'drowsy', 2:'phone', 3:'search'})
    abn_ty_cnt = df_rate[df_rate['type']!='normal'].value_counts()
    abn_ty_rate = abn_ty_cnt / abn_ty_cnt.sum()*100
    ty_labels = ['drowsy', 'phone', 'search']
    ty_sizes = abn_ty_rate.values
    wedgeprops={'width': 0.7, 'edgecolor': 'w', 'linewidth': 5}
    plt.figure(figsize=(10, 10))
    plt.rc('font', size=30)
    plt.pie(ty_sizes, labels=ty_labels, autopct='%1.1f%%', startangle=260, counterclock=False, 
            pctdistance=0.85, colors=['#72bf78', '#a0d683', '#def9c4'], wedgeprops=wedgeprops)
    centre_circle = plt.Circle((0, 0), 0.5, fc='white')
    fig = plt.gcf()
    fig.gca().add_artist(centre_circle)
    plt.title("Abnormal Behavior Type")
    st.pyplot(fig)
