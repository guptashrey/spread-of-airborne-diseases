# library imports
import streamlit as st
import pandas as pd
from urllib.request import urlopen
import json
import plotly.express as px
from sqlalchemy import create_engine

# setting streamlit page configuration
st.set_page_config(
    page_title="Influenza Prediction",
    page_icon="🌐",
    layout="wide")

# setting page title
st.title("Spread of Influenza in New York")

# adding text to sidebar
st.sidebar.write("Influenza is the most common viral infection with virus strains mutating every season, effectively changing the severity of the infection. In rare but possible cases this could be deadly especially for the high-risk groups. Medical service providers can face situations where they have deployed more resources than necessary or they are entirely overwhelmed.")
st.sidebar.write("The goal of this dashboard is to predict the number of cases based on passive contact tracing using mobility data, the weather conditions for a given season and the population demographics which record the highest incidences of the infection & those that face the highest burden of the disease.")
st.sidebar.write("This will serve as a tool for the decision makers to promote relevant measures to curb infections in different regions through vaccination drives, masking advisories to the public, better crowd control, better resource management in terms of hospitalizations and better gauge of the possibility of the flu turning into an epidemic or a pandemic.")

# connection to mysql database
db_config = json.load(open("db_config.json", "r"))
db_conn_str = f'mysql+pymysql://{db_config["username"]}:{db_config["password"]}@{db_config["hostname"]}'
sql_engine = create_engine(db_conn_str, connect_args={'ssl': {'enable_tls': True}})
db_conn= sql_engine.connect()

# @st.cache
# def load_data():
#     """ Loads the required dataframe into the webapp """
#     print("[INFO] Data is loaded")
#     df = pd.read_csv('./data/y_var.csv')
#     return df

influenza_data = pd.read_sql("SELECT * FROM influenza_data", db_conn)
df = influenza_data.copy()
INFLUENZA_SEASONS=['2019-2020', '2020-2021', '2021-2022', '2022-2023']
with st.container():
    selected_season = st.selectbox("Select Influenza Season", INFLUENZA_SEASONS).strip()

pop_df = pd.read_csv('./data/pop_preprocess.csv')

row1_col1, row1_col2 = st.columns(2)

## Generate view metrics
with row1_col1:
    total_pop = pop_df.sum()["pop_est"]
    st.metric(label= "Population", value = total_pop)

with row1_col2:
    total_num_of_influenza_cases = df[df["Season"]==selected_season].Count.sum()
    st.metric(label= "Total Cases", value = total_num_of_influenza_cases)

#######################
with urlopen('https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json') as response:
    counties = json.load(response)

#df = pd.read_csv("https://raw.githubusercontent.com/plotly/datasets/master/fips-unemp-16.csv", dtype={"fips": str})

#df = df[(df["fips"].astype(int)>36000) & (df["fips"].astype(int)<37000)]

df_map = df.groupby(["Season", "FIPS", "County"]).sum().reset_index()
df_map = df_map[df_map["Season"]==selected_season]

fig = px.choropleth(df_map, geojson=counties, locations='FIPS', color='Count',
                        color_continuous_scale="Blues",
                        #range_color=(0, 12),
                        scope="usa",
                        #hover_name=df_map["County"],
                        hover_data=["County", "Count"]
                        #labels={"FIPS": "County"},
                        )
fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
fig.update_geos(fitbounds="locations", visible=False)
st.plotly_chart(fig)




# total_num_of_appointments = len(df)
# unique_patient_count = df.patientid.nunique()
# avg_wait_peroid = round(df.days_between_appointment_and_scheduled_day.mean(),0)
# female_male_ratio = round(df.query('gender == "F"').gender.count() / df.query('gender == "M"').gender.count(), 1)

# count_shows = df["showed"].value_counts()[1]
# count_no_shows = df["showed"].value_counts()[0]
# showup_percent = round( (count_shows/total_num_of_appointments)*100, 1)
# no_showup_percent = round( (count_no_shows/total_num_of_appointments)*100, 1)


# data_to_plot = {
#     "Total Appointments":total_num_of_appointments,
#     "Num of ShowUp's":count_shows,
#     "Num of No ShowUp's":count_no_shows,
#     "Avg Waiting Peroid":str(avg_wait_peroid) + " days",
#     "Total Patients":unique_patient_count,
#     "Patient ShowUp %":str(showup_percent) + " %",
#     "Patient No ShowUp %":str(no_showup_percent) + " %",
#     "Female / Male Ratio":female_male_ratio,
# }

# col1, col2, col3, col4 = st.columns(4)
# columns = [col1, col2, col3, col4]

# count = 0
# for key, value in data_to_plot.items():
#     with columns[count]:
#         st.metric(label= key, value = value)
#         count += 1
#         if count >= 4:
#             count = 0

# st.markdown("""---""")

# matplotlib.use("agg")
# _lock = RendererAgg.lock
# sns.set_style("darkgrid")

# row_1_col1, row_1_col2 =  st.columns(2)
# with row_1_col1, _lock:
#     st.subheader("Patients Appointment Show (vs) NoShow")
#     ## Pie chart to explore distribution of shows and no shows
#     fig = Figure()
#     ax = fig.subplots()
#     df["showed"].value_counts().plot(kind="pie", autopct='%1.1f%%', ax=ax)
#     st.pyplot(fig)

# with row_1_col2, _lock:
#     st.subheader("Appointments by Day of Week")

#     ## bar chart to explore distribution of appointments across days of week
#     weekday_names = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
#     fig = Figure()
#     ax = fig.subplots()
#     sns.countplot(x=df.appointment_day_of_week, order=weekday_names, ax=ax)
#     st.pyplot(fig)

# st.markdown("""---""")
# row_2_col1, row_2_col2 =  st.columns(2)
# with row_2_col1, _lock:
#     st.subheader("KDE plot of age feature")
#     ## KDE plot of age
#     fig = Figure()
#     ax = fig.subplots()
#     sns.kdeplot(df["age"], bw=None, ax=ax)
#     st.pyplot(fig)

# with row_2_col2, _lock:
#     st.subheader("KDE plot of waiting time")

#     ## kde plot of days_between_appointment_and_scheduled_day
#     fig = Figure()
#     ax = fig.subplots()
#     sns.kdeplot(df["days_between_appointment_and_scheduled_day"], bw=None, ax=ax)
#     st.pyplot(fig)

# st.markdown("""---""")
# row_3_col1, row_3_col2 =  st.columns(2)
# with row_3_col1, _lock:
#     st.subheader("Waiting period (vs) ShowUp")

#     ## High wait peroid has direct relation with higher no show ups

#     ## Average of waiting peroid
#     avg_waiting_days = round(df.days_between_appointment_and_scheduled_day.mean(), 0)

#     ## Patients with less than waiting period
#     less_waiting_days = df.query(f'days_between_appointment_and_scheduled_day <= {avg_waiting_days}')
#     # Calculating percentage of people who showed up and waiting time less than AVG waiting time
#     less_waiting_percent = round((less_waiting_days.query('showed == 1').showed.count()/less_waiting_days.showed.count())*100, 1)
    
#     ## Patients with longer than waiting period
#     longer_waiting_days = df.query(f'days_between_appointment_and_scheduled_day > {avg_waiting_days}')
#     # Calculating percentage of people who showed up and waiting time longer than AVG waiting time
#     longer_wait_percent=round((longer_waiting_days.query('showed == 1').showed.count()/longer_waiting_days.showed.count())*100, 1)
    
#     # for index, value in enumerate([less_waiting_percent,longer_wait_percent]):
#     #     plt.text(value, index, str(round(value,1)))
#     fig = Figure()
#     ax = fig.subplots()

#     data_to_plott = pd.DataFrame({"Waiting Time":["LESS than average waiting time", "LONGER then average waiting time"],
#                         "ShowUp %":[less_waiting_percent, longer_wait_percent]})
#     sns.barplot(data=data_to_plott, x="Waiting Time", y="ShowUp %", ax=ax)
#     ax.bar_label(ax.containers[0])
#     st.pyplot(fig)

# with row_3_col2, _lock:
#     st.subheader("Age Group (vs) ShowUp %")

#     ## Age wrt to apoointments show up %

#     # Different age groups to explore

#     age_groups=["infants", "children", "youth", "adults", "seniors"]

#     # Total number of patients belonging to each age group
#     age_count_by_group = df.groupby("age_group").showed.count()
#     # Numbers of pateints who showed up in each age group
#     age_count_by_group_showup = df.groupby('age_group').showed.sum()
#     # Calculating show up % by each age group
#     data_to_plot_age_groups = pd.DataFrame(round((age_count_by_group_showup / age_count_by_group), 3)*100).reindex(age_groups).reset_index().rename(columns={"showed":"ShowUp %"})

#     ## Plot chart
#     fig = Figure()
#     ax = fig.subplots()

#     sns.barplot(data=data_to_plot_age_groups, x="age_group", y="ShowUp %", ax=ax)
#     ax.bar_label(ax.containers[0])
#     st.pyplot(fig)

# st.markdown("""---""")
# row_4_col1, row_4_col2 =  st.columns(2)
# with row_4_col1, _lock:
#     st.subheader("Disability (vs) ShowUp %")

#     ## Physical disablity has direct relation with higher show ups

#     # % of handicap people who showed up
#     handicap_percent = (df.query('handicap > 0 & showed == 1').showed.count() / df.query('handicap == 1').showed.count())*100
#     # % of non handicap people who showed up
#     not_handicap_percent = (df.query('handicap == 0 & showed == 1').showed.count() / df.query('handicap == 0').showed.count())*100
    
#     ## Plot the figure
#     fig = Figure()
#     ax = fig.subplots()

#     data_to_plot_handicap = pd.DataFrame({"Patients":["Handicapped", "Not Handicapped"],
#                                             "ShowUp %":[handicap_percent, not_handicap_percent]})
#     sns.barplot(data=data_to_plot_handicap, x="Patients", y="ShowUp %", ax=ax)
#     ax.bar_label(ax.containers[0])
#     st.pyplot(fig)


# with row_4_col2, _lock:
#     st.subheader("Gender Distribution")

#     ## Gender relation with higher show ups        
#     ## Plot the figure
#     fig = Figure()
#     ax = fig.subplots()
    
#     sns.countplot(data=df, x="gender",hue="showed", ax=ax)

#     for container in ax.containers:
#         ax.bar_label(container)

#     #ax.bar_label(ax.containers[0])
#     st.pyplot(fig)

# st.markdown("""---""")
# row_5_col1, row_5_col2 =  st.columns(2)
# with row_5_col1, _lock:
#     st.subheader("SMS Reminder (vs) ShowUp%")
    
#     ## SMS reminder vs Show Up %
#     sms_percent = round((df.query('sms_received == 1 & showed == 1').showed.count() / df.query('sms_received == 1').showed.count()), 3)*100
#     no_sms_percent = round((df.query('sms_received == 0 & showed == 1').showed.count() / df.query('sms_received == 0').showed.count()), 3)*100


#     data_to_plott_sms = pd.DataFrame({"Reminder":["SMS recieved", "No SMS recieved"],
#                         "ShowUp %":[no_sms_percent, sms_percent]})

#     ## Gender relation with higher show ups        
#     ## Plot the figure
#     fig = Figure()
#     ax = fig.subplots()

#     sns.barplot(data=data_to_plott_sms, x="Reminder", y="ShowUp %", ax=ax)

#     ax.bar_label(ax.containers[0])
#     st.pyplot(fig)

# st.markdown("""---""")