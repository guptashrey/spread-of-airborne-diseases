# library imports
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import plotly.express as px
import json
from sqlalchemy import create_engine
import seaborn as sns

# global variables
COUNTIES = ['ALBANY', 'ALLEGANY', 'BRONX', 'BROOME', 'CATTARAUGUS', 'CAYUGA', 'CHAUTAUQUA', 'CHEMUNG', 'CHENANGO', 'CLINTON', 'COLUMBIA', 'CORTLAND', 'DELAWARE', 'DUTCHESS', 'ERIE', 'ESSEX', 'FRANKLIN', 'FULTON', 'GENESEE', 'GREENE', 'HERKIMER', 'JEFFERSON', 'KINGS', 'LEWIS', 'LIVINGSTON', 'MADISON', 'MONROE', 'MONTGOMERY', 'NASSAU', 'NEW YORK', 'NIAGARA', 'ONEIDA', 'ONONDAGA', 'ONTARIO', 'ORANGE', 'ORLEANS', 'OSWEGO', 'OTSEGO', 'PUTNAM', 'QUEENS', 'RENSSELAER', 'RICHMOND', 'ROCKLAND', 'SARATOGA', 'SCHENECTADY', 'SCHOHARIE', 'SCHUYLER', 'SENECA', 'ST LAWRENCE', 'STEUBEN', 'SUFFOLK', 'SULLIVAN', 'TIOGA', 'TOMPKINS', 'ULSTER', 'WARREN', 'WASHINGTON', 'WAYNE', 'WESTCHESTER', 'WYOMING', 'YATES']

def load_data():
    '''
    Makes connection to MYSQL database and loads the data
    '''

    # connection to mysql database
    db_config = json.load(open("db_config.json", "r"))
    db_conn_str = f'mysql+pymysql://{db_config["username"]}:{db_config["password"]}@{db_config["hostname"]}'
    sql_engine = create_engine(db_conn_str, connect_args={'ssl': {'enable_tls': True}})
    db_conn= sql_engine.connect()
    
    # reads data into pandas dataframe from given tables
    predictions = pd.read_sql("SELECT * FROM predictions", db_conn)
    features_w1 = pd.read_sql("SELECT * from features_w1", db_conn)
    features_w2 = pd.read_sql("SELECT * from features_w2", db_conn)
    features_w3 = pd.read_sql("SELECT * from features_w3", db_conn)
    features_w4 = pd.read_sql("SELECT * from features_w4", db_conn)
    return predictions, features_w1, features_w2, features_w3, features_w4

def run_ui():

    predictions, features_w1, features_w2, features_w3, features_w4 = load_data()
    predictions.sort_values(by=["Forecast Date"], inplace=True)
    features_w1.drop(columns=["index"], inplace=True)
    features_w2.drop(columns=["index"], inplace=True)
    features_w3.drop(columns=["index"], inplace=True)
    features_w4.drop(columns=["index"], inplace=True)

    # setting streamlit page configuration
    st.set_page_config(
        layout="wide",
        page_title="Future Forecast",
        page_icon="🔮")

    # adding text to page sidebar
    st.sidebar.write("This dashboard shows the number of cases predicted for the upcoming weeks. We also provide the accuracy percentage for each week’s predictions, so that the medical official can gauge the volume of resources to be deployed. For technical folks, we also provide residuals, which can be incorporated in their decision-making models for the capacity deployment decisions.")
    
    # setting page title
    st.title("Future Forecast")

    # dropdown for selecting county
    with st.container():
        selected_county = st.selectbox("Select a county", COUNTIES).strip()

    # line chart with historical and future data points
    st.subheader("Predicted case count for future weeks")

    predictions_selected = predictions[predictions["County"]==selected_county]
    fig = px.line(predictions_selected, x="Forecast Date", y=["Actual Cases", "Predicted Cases"], markers=True)
    fig.update_xaxes(gridcolor = "#262730")
    fig.update_yaxes(gridcolor = "#262730")
    st.plotly_chart(fig, use_container_width=True)

    # table with forecast values and accuracy metrics
    predictions_selected_1 = predictions_selected.copy()
    predictions_selected_1=predictions_selected_1[["Forecast Date", "Forecasted On", "Actual Cases", "Predicted Cases", "Accuracy (%)"]]
    predictions_selected_1 = predictions_selected_1[~predictions_selected_1["Predicted Cases"].isna()].fillna("-")
    predictions_selected_1["Forecast Date"] = predictions_selected_1["Forecast Date"].astype(str)
    predictions_selected_1["Forecasted On"] = predictions_selected_1["Forecasted On"].astype(str)
    predictions_selected_1["Actual Cases"] = predictions_selected_1["Actual Cases"].astype(str)
    predictions_selected_1["Predicted Cases"] = predictions_selected_1["Predicted Cases"].astype(str)
    predictions_selected_1.index = predictions_selected_1["Forecast Date"]
    predictions_selected_1.drop(columns=["Forecast Date"], inplace=True)

    # table of residuals across different forecast models
    predictions_selected_2 = predictions_selected.copy()
    predictions_selected_2=predictions_selected_2[["Forecast Date", "Actual Cases", "Predicted Cases", "Residuals (W - 1)", "Residuals (W - 2)", "Residuals (W - 3)", "Residuals (W - 4)"]]
    predictions_selected_2 = predictions_selected_2[(~predictions_selected_2["Predicted Cases"].isna()) & (~predictions_selected_2["Actual Cases"].isna())].fillna("-")
    predictions_selected_2["Forecast Date"] = predictions_selected_2["Forecast Date"].astype(str)
    predictions_selected_2["Actual Cases"] = predictions_selected_2["Actual Cases"].astype(str)
    predictions_selected_2["Residuals (W - 1)"] = predictions_selected_2["Residuals (W - 1)"].astype(str)
    predictions_selected_2["Residuals (W - 2)"] = predictions_selected_2["Residuals (W - 2)"].astype(str)
    predictions_selected_2["Residuals (W - 3)"] = predictions_selected_2["Residuals (W - 3)"].astype(str)
    predictions_selected_2["Residuals (W - 4)"] = predictions_selected_2["Residuals (W - 4)"].astype(str)
    predictions_selected_2.index = predictions_selected_2["Forecast Date"]
    predictions_selected_2.drop(columns=["Forecast Date", "Predicted Cases"], inplace=True)

    row1_col1, row1_col2 = st.columns(2)

    with row1_col1:
        st.subheader("Forecast Accuracy")
        st.dataframe(predictions_selected_1)

    with row1_col2:
        st.subheader("Residuals")
        st.dataframe(predictions_selected_2)

    st.subheader("Forecast Drivers")
    row2_col1, row2_col2 = st.columns(2)

    # plotting feature importances of 1 week, 2 weeks, 3 weeks and 4 weeks ahead forecast models
    with row2_col1:
        st.subheader("1 Week Ahead Forecast Model")
        features_w1_df = features_w1[features_w1["County"]==selected_county].drop(columns=["County"]).iloc[:10]
        fig1 = plt.figure()
        ax1 = fig1.subplots()
        sns.barplot(x=features_w1_df['Feature Importance'], y=features_w1_df['Feature Name'], ax=ax1)
        plt.xlabel('FEATURE IMPORTANCE')
        plt.ylabel('FEATURE NAMES')
        st.pyplot(fig1)
        
        st.subheader("3 Weeks Ahead Forecast Model")
        features_w3_df = features_w3[features_w3["County"]==selected_county].drop(columns=["County"]).iloc[:10]
        fig3 = plt.figure()
        ax3 = fig3.subplots()
        sns.barplot(x=features_w3_df['Feature Importance'], y=features_w3_df['Feature Name'], ax=ax3)
        plt.xlabel('FEATURE IMPORTANCE')
        plt.ylabel('FEATURE NAMES')
        st.pyplot(fig3)

    with row2_col2:
        st.subheader("2 Weeks Ahead Forecast Model")
        features_w2_df = features_w2[features_w2["County"]==selected_county].drop(columns=["County"]).iloc[:10]
        fig2 = plt.figure()
        ax2 = fig2.subplots()
        sns.barplot(x=features_w2_df['Feature Importance'], y=features_w2_df['Feature Name'], ax=ax2)
        plt.xlabel('FEATURE IMPORTANCE')
        plt.ylabel('FEATURE NAMES')
        st.pyplot(fig2)

        st.subheader("4 Weeks Ahead Forecast Model")
        features_w4_df = features_w4[features_w4["County"]==selected_county].drop(columns=["County"]).iloc[:10]
        fig4 = plt.figure()
        ax4 = fig4.subplots()
        sns.barplot(x=features_w4_df['Feature Importance'], y=features_w4_df['Feature Name'], ax=ax4)
        plt.xlabel('FEATURE IMPORTANCE')
        plt.ylabel('FEATURE NAMES')
        st.pyplot(fig4)

if __name__ == '__main__':
    run_ui()