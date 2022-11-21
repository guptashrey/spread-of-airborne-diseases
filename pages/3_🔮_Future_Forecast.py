import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import plotly.express as px

st.set_page_config(
    layout="wide",
    page_title="Future Forecast",
    page_icon="🔮")

st.title("Future Forecast")
COUNTIES = ['ALBANY', 'ALLEGANY', 'BRONX', 'BROOME', 'CATTARAUGUS', 'CAYUGA', 'CHAUTAUQUA', 'CHEMUNG', 'CHENANGO', 'CLINTON', 'COLUMBIA', 'CORTLAND', 'DELAWARE', 'DUTCHESS', 'ERIE', 'ESSEX', 'FRANKLIN', 'FULTON', 'GENESEE', 'GREENE', 'HAMILTON', 'HERKIMER', 'JEFFERSON', 'KINGS', 'LEWIS', 'LIVINGSTON', 'MADISON', 'MONROE', 'MONTGOMERY', 'NASSAU', 'NEW YORK', 'NIAGARA', 'ONEIDA', 'ONONDAGA', 'ONTARIO', 'ORANGE', 'ORLEANS', 'OSWEGO', 'OTSEGO', 'PUTNAM', 'QUEENS', 'RENSSELAER', 'RICHMOND', 'ROCKLAND', 'SARATOGA', 'SCHENECTADY', 'SCHOHARIE', 'SCHUYLER', 'SENECA', 'ST LAWRENCE', 'STEUBEN', 'SUFFOLK', 'SULLIVAN', 'TIOGA', 'TOMPKINS', 'ULSTER', 'WARREN', 'WASHINGTON', 'WAYNE', 'WESTCHESTER', 'WYOMING', 'YATES']
COUNTIES = [i + " COUNTY" for i in COUNTIES]
with st.container():
    county = st.selectbox("Select a county", COUNTIES).strip()
    #county = str.upper(county) + " COUNTY"

df = pd.read_csv('./data/preds.csv')
df["Forecast Date"] = pd.to_datetime(df["Forecast Date"])
df["Forecasted On"] = pd.to_datetime(df["Forecasted On"])
df.sort_values(by=["Forecast Date"], inplace=True)
# st.line_chart(data = df, x = "Forecast Date", y=["Actual Cases", "Predicted Cases"])

fig = px.line(df, x="Forecast Date", y=["Actual Cases", "Predicted Cases"], markers=True)

fig.update_xaxes(gridcolor = "#262730")
fig.update_yaxes(gridcolor = "#262730")
#fig.update_yaxes(visible=False, fixedrange=True)

# # strip down the rest of the plot
# fig.update_layout(
#     plot_bgcolor="black"
# )
st.plotly_chart(fig, use_container_width=True)

df1 = df.copy()
df1=df1[["Forecast Date", "Forecasted On", "Actual Cases", "Predicted Cases", "Accuracy (%)"]]
df1 = df1[~df1["Predicted Cases"].isna()].fillna("-")
df1["Forecast Date"] = df1["Forecast Date"].astype(str)
df1["Forecasted On"] = df1["Forecasted On"].astype(str)
df1["Actual Cases"] = df1["Actual Cases"].astype(str)
df1["Predicted Cases"] = df1["Predicted Cases"].astype(str)
df1.index = df1["Forecast Date"]
df1.drop(columns=["Forecast Date"], inplace=True)

df2 = df.copy()
df2=df2[["Forecast Date", "Actual Cases", "Predicted Cases", "Residuals (W - 1)", "Residuals (W - 2)", "Residuals (W - 3)", "Residuals (W - 4)"]]
df2 = df2[(~df2["Predicted Cases"].isna()) & (~df2["Actual Cases"].isna())].fillna("-")
df2["Forecast Date"] = df2["Forecast Date"].astype(str)
df2["Actual Cases"] = df2["Actual Cases"].astype(str)
df2["Residuals (W - 1)"] = df2["Residuals (W - 1)"].astype(str)
df2["Residuals (W - 2)"] = df2["Residuals (W - 2)"].astype(str)
df2["Residuals (W - 3)"] = df2["Residuals (W - 3)"].astype(str)
df2["Residuals (W - 4)"] = df2["Residuals (W - 4)"].astype(str)
df2.index = df2["Forecast Date"]
df2.drop(columns=["Forecast Date", "Predicted Cases"], inplace=True)
#st.dataframe(df2)

row1_col1, row1_col2 = st.columns(2)

with row1_col1:
    st.subheader("Forecast Accuracy")
    st.dataframe(df1)

with row1_col2:
    st.subheader("Residuals")
    st.dataframe(df2)