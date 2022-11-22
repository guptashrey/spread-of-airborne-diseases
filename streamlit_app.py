# library imports
import streamlit as st
import pandas as pd
from urllib.request import urlopen
import json
import plotly.express as px
from sqlalchemy import create_engine

# global variables
INFLUENZA_SEASONS=['2019-2020', '2020-2021', '2021-2022', '2022-2023']
POPULATION_YEARS=[2018, 2019, 2020, 2021]

def load_data():
    '''
    Makes connection to MYSQL database and loads the data
    '''

    # connection to mysql database
    db_config = json.load(open("db_config.json", "r"))
    db_conn_str = f'mysql+pymysql://{db_config["username"]}:{db_config["password"]}@{db_config["hostname"]}'
    sql_engine = create_engine(db_conn_str, connect_args={'ssl': {'enable_tls': True}})
    db_conn= sql_engine.connect()

    influenza_data = pd.read_sql("SELECT * FROM influenza_data", db_conn)
    population_data = pd.read_sql("SELECT * FROM population", db_conn)
    db_conn.close()
    
    return influenza_data, population_data

def run_ui():
    '''
    Renders the Streamlit Page UI
    '''
    influenza_data, population_data = load_data()

    # setting streamlit page configuration
    st.set_page_config(
        page_title="Influenza Prediction",
        page_icon="🌐",
        layout="wide")

    # setting page title
    st.title("Spread of Influenza in New York")

    # adding text to sidebar
    st.sidebar.write("Influenza is the most common viral infection with virus strains mutating every season, effectively changing the severity of the infection. In rare but possible cases this could be deadly especially for the high-risk groups. Medical service providers can face situations where they have deployed more resources than necessary or they are entirely overwhelmed.")
    st.sidebar.write("This will serve as a tool for the decision makers to promote relevant measures to curb infections in different regions through vaccination drives, masking advisories to the public, better crowd control, better resource management in terms of hospitalizations and better gauge of the possibility of the flu turning into an epidemic or a pandemic.")

    # dropdown for selecting influenza season
    with st.container():
        selected_season = st.selectbox("Select Influenza Season", INFLUENZA_SEASONS).strip()

    # adding population estimate and number of influenza cases metrics
    row1_col1, row1_col2 = st.columns(2)
    with row1_col1:
        pop_year = POPULATION_YEARS[INFLUENZA_SEASONS.index(selected_season)]
        population_data = population_data[population_data["YEAR"]==pop_year]
        total_pop = population_data.sum()["POPESTIMATE"]
        st.metric(label= "Population", value = total_pop)

    with row1_col2:
        total_num_of_influenza_cases = influenza_data[influenza_data["Season"]==selected_season].Count.sum()
        st.metric(label= "Total Cases", value = total_num_of_influenza_cases)

    # county level heatmap for number of influenza cases
    with urlopen('https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json') as response:
        counties = json.load(response)
    df_map = influenza_data.groupby(["Season", "FIPS", "County"]).sum().reset_index()
    df_map = df_map[df_map["Season"]==selected_season]

    fig = px.choropleth(df_map, geojson=counties, locations='FIPS', color='Count',
                            color_continuous_scale="Blues",
                            scope="usa",
                            hover_data=["County", "Count"]
                            )
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    fig.update_geos(fitbounds="locations", visible=False)
    st.plotly_chart(fig)

if __name__ == '__main__':
    run_ui()