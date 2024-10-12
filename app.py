# coding: utf-8
import streamlit as st
import pandas as pd
import altair as alt
import plotly.express as px

st.set_page_config(
    page_title="Monthly Report",
    page_icon="🚗",
    layout="wide",
)

st.title("🚗 Monthly Driver Report")

st.markdown("")
st.markdown("")

df_data = pd.read_csv('data/data.csv')

with st.sidebar:
    st.title('✅ Driver ID')
    
    id_list = list(df_data.id.unique())[::-1]
    
    selected_id = st.selectbox('Select an ID', id_list, index=len(id_list)-1)
    df_selected_id = df_data[df_data.id == selected_id]
    df_selected_id_sorted = df_selected_id.sort_values(by="id", ascending=False)

def make_heatmap(input_df, input_y, input_x, input_color, input_color_theme):
    heatmap = alt.Chart(input_df).mark_rect().encode(
            y=alt.Y(f'{input_y}:O', axis=alt.Axis(title="Month", titleFontSize=18, titlePadding=15, titleFontWeight=900, labelAngle=0)),
            x=alt.X(f'{input_x}:O', axis=alt.Axis(title="", titleFontSize=18, titlePadding=15, titleFontWeight=900)),
            color=alt.Color(f'max({input_color}):Q',
                             legend=None,
                             scale=alt.Scale(scheme=input_color_theme)),
            stroke=alt.value('black'),
            strokeWidth=alt.value(0.25),
        ).properties(width=1200
        ).configure_axis(
        labelFontSize=12,
        titleFontSize=12
        ) 
    # height=300
    return heatmap


# Calculation abnormal behavior rate
def calculate_abnormal_rate(input_df, input_id):
  selected_id_data = input_df[input_df['id'] == input_id].reset_index()
  previous_id_data = input_df[input_df['id'] == input_id - 1].reset_index()
  selected_id_data['abnormal_rate'] = selected_id_data.abnormal.sub(previous_id_data.abnormal, fill_value=0)
  return pd.concat([selected_id_data.states, selected_id_data.id, selected_id_data.abnormal, selected_id_data.abnormal_rate], axis=1).sort_values(by="abnormal_rate", ascending=False)

#######################
# Dashboard Main Panel
col = st.columns((7, 3), gap='medium')

with col[0]:
    st.markdown('#### Total Population')
    
    heatmap = make_heatmap(df_data, 'date', 'id', 'abnormal', 'input_color_theme')
    st.altair_chart(heatmap, use_container_width=True)