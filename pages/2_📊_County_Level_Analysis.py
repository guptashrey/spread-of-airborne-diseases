import streamlit as st
import pandas as pd
import seaborn as sns
from matplotlib.figure import Figure
import json
import matplotlib.pyplot as plt
from sqlalchemy import create_engine

COUNTIES = ['ALBANY', 'ALLEGANY', 'BRONX', 'BROOME', 'CATTARAUGUS', 'CAYUGA', 'CHAUTAUQUA', 'CHEMUNG', 'CHENANGO', 'CLINTON', 'COLUMBIA', 'CORTLAND', 'DELAWARE', 'DUTCHESS', 'ERIE', 'ESSEX', 'FRANKLIN', 'FULTON', 'GENESEE', 'GREENE', 'HERKIMER', 'JEFFERSON', 'KINGS', 'LEWIS', 'LIVINGSTON', 'MADISON', 'MONROE', 'MONTGOMERY', 'NASSAU', 'NEW YORK', 'NIAGARA', 'ONEIDA', 'ONONDAGA', 'ONTARIO', 'ORANGE', 'ORLEANS', 'OSWEGO', 'OTSEGO', 'PUTNAM', 'QUEENS', 'RENSSELAER', 'RICHMOND', 'ROCKLAND', 'SARATOGA', 'SCHENECTADY', 'SCHOHARIE', 'SCHUYLER', 'SENECA', 'ST LAWRENCE', 'STEUBEN', 'SUFFOLK', 'SULLIVAN', 'TIOGA', 'TOMPKINS', 'ULSTER', 'WARREN', 'WASHINGTON', 'WAYNE', 'WESTCHESTER', 'WYOMING', 'YATES']

def load_data():
    # connection to mysql database
    db_config = json.load(open("db_config.json", "r"))
    db_conn_str = f'mysql+pymysql://{db_config["username"]}:{db_config["password"]}@{db_config["hostname"]}'
    sql_engine = create_engine(db_conn_str, connect_args={'ssl': {'enable_tls': True}})
    db_conn= sql_engine.connect()
    
    influenza_data = pd.read_sql("SELECT * FROM influenza_data", db_conn)
    population_data = pd.read_sql("SELECT * FROM population", db_conn)
    weather_data = pd.read_sql("SELECT * FROM weather", db_conn)
    google_mobility_data = pd.read_sql("SELECT * FROM google_mobility", db_conn)
    return influenza_data, population_data, weather_data, google_mobility_data

influenza_data, population_data, weather_data, google_mobility_data = load_data()
population_data = population_data[population_data["YEAR"]==2021]

weather_data.drop(columns=["index"], inplace=True)
weather_data.datetime = pd.to_datetime(weather_data.datetime)
weather_data = weather_data[(weather_data["datetime"]>= "2020-02-15") & (weather_data["datetime"]<= "2022-10-29")]
weather_data = pd.merge(weather_data, influenza_data[["Week Ending Date", "County", "Count"]], left_on=["datetime", "county"], right_on=["Week Ending Date", "County"], how="left").drop(columns=["Week Ending Date", "County"]).fillna(0)

google_mobility_data["county"] = [str.upper(i).replace(" COUNTY", "") for i in list(google_mobility_data["county"])]

# if(google_mobility_data[google_mobility_data['county'] == county].shape[0] < len(google_mobility_data['date'].unique())):
#     county_data = google_mobility_data[google_mobility_data['county'] == county].merge(google_mobility_data[google_mobility_data['county'] == 'Albany County']['date'], how='right', on='date').ffill()
# else:
#     county_data = google_mobility_data[google_mobility_data['county'] == county]

def run_ui():

    # setting streamlit page configuration
    st.set_page_config(
        layout="wide",
        page_title="County Level Analysis",
        page_icon="📊")
    
    # setting page title
    st. title("County Analysis")
    
    # matplotlib.use("agg")
    # _lock = RendererAgg.lock
    # sns.set_style("darkgrid")
    
    # dropdown for selecting county
    with st.container():
        selected_county = st.selectbox("Select a county", COUNTIES).strip()

    # adding population estimate and number of influenza cases metrics
    st.subheader("Population for different age buckets in a county")
    row1_col1, row1_col2, row1_col3, row1_col4 = st.columns(4)
    
    with row1_col1:
        st.markdown("Season 2019-2020")
        total_pop = population_data[population_data["CTYNAME"]==selected_county].sum()["POPESTIMATE"]
        st.metric(label= "Population", value = total_pop)
        total_num_of_influenza_cases = influenza_data[(influenza_data["Season"]=="2019-2020") & (influenza_data["County"]==selected_county)].Count.sum()
        st.metric(label= "Total Cases", value = total_num_of_influenza_cases)

    with row1_col2:
        st.markdown("Season 2020-2021")
        total_pop = population_data[population_data["CTYNAME"]==selected_county].sum()["POPESTIMATE"]
        st.metric(label= "Population", value = total_pop)
        total_num_of_influenza_cases = influenza_data[(influenza_data["Season"]=="2020-2021") & (influenza_data["County"]==selected_county)].Count.sum()
        st.metric(label= "Total Cases", value = total_num_of_influenza_cases)

    with row1_col3:
        st.markdown("Season 2021-2022")
        total_pop = population_data[population_data["CTYNAME"]==selected_county].sum()["POPESTIMATE"]
        st.metric(label= "Population", value = total_pop)
        total_num_of_influenza_cases = influenza_data[(influenza_data["Season"]=="2021-2022") & (influenza_data["County"]==selected_county)].Count.sum()
        st.metric(label= "Total Cases", value = total_num_of_influenza_cases)

    with row1_col4:
        st.markdown("Season 2022-2023")
        total_pop = population_data[population_data["CTYNAME"]==selected_county].sum()["POPESTIMATE"]
        st.metric(label= "Population", value = total_pop)
        total_num_of_influenza_cases = influenza_data[(influenza_data["Season"]=="2022-2023") & (influenza_data["County"]==selected_county)].Count.sum()
        st.metric(label= "Total Cases", value = total_num_of_influenza_cases)

    st.caption("Influenza has higher incidence numbers in 0-4 yrs and 50-64 yrs buckets but 18-49 yrs bucket are the prime vectors. cases are high where the population number for 18-49 yrs is high.")
    st.markdown("""---""")

    st.subheader("Graph of temperature in comparison to the number of cases plotted against the date range")
    df_temp = weather_data[(weather_data['county'] == selected_county)]
    st.line_chart(data = df_temp, x = "datetime", y=["Count", "tempmax"])
    st.caption("weather conditions like high temperatures teamed with humidity are more conducive to influenza spread")

    st.subheader("Graph of mobility for 6 different reasons against the date range")
    feat_names = ["retail_and_recreation_percent_change","grocery_and_pharmacy_percent_change","parks_percent_change","transit_stations_percent_change","workplaces_percent_change","residential_percent_change"]
    st.line_chart(data = google_mobility_data[google_mobility_data["county"]==selected_county], x = "date", y = feat_names)
    st.caption("influenza need vectors for the spread. Increase mobility in and out of infectious areas increases the number of vectors and infections")

    st.subheader("Correlation of count of cases with the weather conditions")
    #fig = Figure()
    fig, ax = plt.subplots(figsize=(5, 5))
    df_temp = weather_data[["humidity", "windspeed", "snow", "dew", "windgust", "tempmax", "feelslikemax", "severerisk", "feelslike", "temp", "feelslikemin", "tempmin", "Count"]]
    corr_matrix = df_temp.corr(method='pearson')
    sns.heatmap(corr_matrix, cmap='RdBu_r', square=True, ax=ax)
    st.pyplot(fig)
    st.caption("The influenza cases increase with increased windspeeds as infectious droplets travel further.")

if __name__ == '__main__':
    run_ui()