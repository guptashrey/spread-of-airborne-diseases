import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.figure_factory as ff
import seaborn as sns
from matplotlib.backends.backend_agg import RendererAgg
from matplotlib.figure import Figure
import matplotlib
from urllib.request import urlopen
import json
import plotly.express as px

st.set_page_config(
    layout="wide",
    page_title="County Level Analysis",
    page_icon="📊")

COUNTIES = ['ALBANY', 'ALLEGANY', 'BRONX', 'BROOME', 'CATTARAUGUS', 'CAYUGA', 'CHAUTAUQUA', 'CHEMUNG', 'CHENANGO', 'CLINTON', 'COLUMBIA', 'CORTLAND', 'DELAWARE', 'DUTCHESS', 'ERIE', 'ESSEX', 'FRANKLIN', 'FULTON', 'GENESEE', 'GREENE', 'HAMILTON', 'HERKIMER', 'JEFFERSON', 'KINGS', 'LEWIS', 'LIVINGSTON', 'MADISON', 'MONROE', 'MONTGOMERY', 'NASSAU', 'NEW YORK', 'NIAGARA', 'ONEIDA', 'ONONDAGA', 'ONTARIO', 'ORANGE', 'ORLEANS', 'OSWEGO', 'OTSEGO', 'PUTNAM', 'QUEENS', 'RENSSELAER', 'RICHMOND', 'ROCKLAND', 'SARATOGA', 'SCHENECTADY', 'SCHOHARIE', 'SCHUYLER', 'SENECA', 'ST LAWRENCE', 'STEUBEN', 'SUFFOLK', 'SULLIVAN', 'TIOGA', 'TOMPKINS', 'ULSTER', 'WARREN', 'WASHINGTON', 'WAYNE', 'WESTCHESTER', 'WYOMING', 'YATES']
st. title("County Analysis")

#st.write('''### Overall Analysis Across Neighbourhoods''')

@st.cache
def load_data():
    """ Loads the required dataframe into the webapp """
    print("[INFO] Data is loaded")
    df = pd.read_csv('./data/data_for_app.csv')
    df1 = pd.read_csv('./data/temp.csv')
    return df, df1

df, df1 = load_data()

## Generate view metrics
# total_num_of_appointments = len(df)
# num_of_neighbourhoods = df.neighbourhood.nunique()
# avg_wait_peroid = round(df.days_between_appointment_and_scheduled_day.mean(),0)

# count_shows = df["showed"].value_counts()[1]
# count_no_shows = df["showed"].value_counts()[0]
# showup_percent = round( (count_shows/total_num_of_appointments)*100, 1)
# no_showup_percent = round( (count_no_shows/total_num_of_appointments)*100, 1)


# data_to_plot = {
#     "Neighbourhoods":str(num_of_neighbourhoods),
#     "Avg Waiting Peroid":str(avg_wait_peroid) + " days",
#     "Patient ShowUp %":str(showup_percent) + " %",
#     "Patient No ShowUp %":str(no_showup_percent) + " %",
# }

# ## Add view cards for basic information around data
# col1, col2, col3, col4 = st.columns(4)
# columns = [col1, col2, col3, col4]

# count = 0
# for key, value in data_to_plot.items():
#     with columns[count]:
#         st.metric(label= key, value = value)
#         count += 1

matplotlib.use("agg")
_lock = RendererAgg.lock
sns.set_style("darkgrid")

st.markdown("""---""")

with st.container():
    selected_county = st.selectbox("Select a neighbourhood", COUNTIES).strip()
    county = str.upper(selected_county) + " COUNTY"

#row1_col1, row1_col2 = st.columns(2)

#with row1_col1:
df_temp = df1[(df1['county'] == selected_county)]

st.line_chart(data = df_temp, x = "datetime", y=["Count", "tempmax"])

google_mobility_data_NY_cleaned = pd.read_csv('./data/google_mobility_data.csv').iloc[:, 1:]
google_mobility_data_NY_cleaned["county"] = [str.upper(i) for i in list(google_mobility_data_NY_cleaned["county"])]
if(google_mobility_data_NY_cleaned[google_mobility_data_NY_cleaned['county'] == county].shape[0] < len(google_mobility_data_NY_cleaned['date'].unique())):
    county_data = google_mobility_data_NY_cleaned[google_mobility_data_NY_cleaned['county'] == county].merge(google_mobility_data_NY_cleaned[google_mobility_data_NY_cleaned['county'] == 'Albany County']['date'], how='right', on='date').ffill()
else:
    county_data = google_mobility_data_NY_cleaned[google_mobility_data_NY_cleaned['county'] == county]

feat_names = ["retail_and_recreation_percent_change","grocery_and_pharmacy_percent_change","parks_percent_change","transit_stations_percent_change","workplaces_percent_change","residential_percent_change"]
st.line_chart(data = county_data, x = "date", y = feat_names)

fig = Figure()
ax = fig.subplots()
df_temp1 = df_temp[["humidity", "windspeed", "snow", "dew", "windgust", "tempmax", "feelslikemax", "severerisk", "feelslike", "temp", "feelslikemin", "tempmin", "Count"]]
corr_matrix = df_temp1.corr(method='pearson')
sns.heatmap(corr_matrix, cmap='RdBu_r', square=True, ax=ax)
st.write(fig)


# Add histogram data
x1 = np.random.randn(200) - 2
x2 = np.random.randn(200)
x3 = np.random.randn(200) + 2

# Group data together
hist_data = [x1, x2, x3]

group_labels = ['Group 1', 'Group 2', 'Group 3']

# Create distplot with custom bin_size
fig = ff.create_distplot(
        hist_data, group_labels, bin_size=[.1, .25, .5])

# Plot!
st.plotly_chart(fig, use_container_width=True)



with urlopen('https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json') as response:
    counties = json.load(response)

df = pd.read_csv("https://raw.githubusercontent.com/plotly/datasets/master/fips-unemp-16.csv",
                   dtype={"fips": str})

df = df[(df["fips"].astype(int)>36000) & (df["fips"].astype(int)<37000)]

fig = px.choropleth(df, geojson=counties, locations='fips', color='unemp',
                        color_continuous_scale="Reds",
                        range_color=(0, 12),
                        scope="usa",
                        labels={'unemp':'unemployment rate'}
                          )
fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
fig.update_geos(fitbounds="locations", visible=False)
st.plotly_chart(fig)


# col1, col2 = st.columns(2)

# with col1, _lock:
        
    # ## Plot bar chart
    # fig = Figure()
    # ax = fig.subplots()
    # df_temp = df1[(df1['county'] == selected_county) & ((df1['datetime'] >= '2020-09-01') & (df1['datetime'] <= '2021-12-31'))]
    # df_temp = df1[["datetime", "Count", "tempmax"]]

    # sns.lineplot(data=df_temp, ax=ax)

    # st.pyplot(fig)



# plt.plot(df_temp['datetime'], df_temp['Count'], color='red')
# plt.plot(df_temp['datetime'], df_temp['tempmax'], color='blue')
# plt.xticks(rotation=90)
# plt.show()

# ## Generate view metirc row 2
# # Patients from selected nieghbourhood
# df_filtered_neigh = df[df['neighbourhood'] == neighbourhood_selected].copy()
# patients_from_neigh = len(df_filtered_neigh)

# # Avg wait time for selcted neighbourhood
# waitint_time_by_neighbourhood = df.groupby('neighbourhood').days_between_appointment_and_scheduled_day.mean()
# avg_wait_selected_neigh = round(waitint_time_by_neighbourhood[neighbourhood_selected], 1)

# count_shows = df_filtered_neigh["showed"].value_counts()[1]
# count_no_shows = df_filtered_neigh["showed"].value_counts()[0]
# showup_percent = round( (count_shows/patients_from_neigh)*100, 1)
# no_showup_percent = round( (count_no_shows/patients_from_neigh)*100, 1)

# data_to_plot_row2 = {
#     "Avg Waiting time":str(avg_wait_selected_neigh) + " days",
#     "Total Patients":str(patients_from_neigh),
#     "Patient ShowUp %":str(showup_percent) + " %",
#     "Patient No ShowUp %":str(no_showup_percent) + " %",
# }

## Add view cards for basic information around data
# col1, col2, col3, col4 = st.columns(4)
# columns = [col1, col2, col3, col4]

# count = 0
# for key, value in data_to_plot_row2.items():
#     with columns[count]:
#         st.metric(label= key, value = value)
#         count += 1

## Weather Analysis by Neighbourhood
## Exploring effect of different weather parameters on patient show ups in each neighbourhood
# weather_cols = ['humidity', 'feelslikemax', 'windspeed', 'solarradiation']
# appointments_weather_df = df.groupby(['neighbourhood','showed'])[weather_cols].mean().reset_index()

# patient_no_show_weather = appointments_weather_df[appointments_weather_df["neighbourhood"] == neighbourhood_selected]
# patient_no_show_weather.showed = patient_no_show_weather.showed.astype("str")

# col1, col2 = st.columns(2)
# columns = [col1, col2]

# count = 0
# for i, col_name in enumerate(weather_cols):
#     with columns[count]:
        
#         ## Plot bar chart
#         fig = Figure()
#         ax = fig.subplots()

#         data_to_plot_weather = patient_no_show_weather.copy()[["showed", col_name]]

#         sns.barplot(data=data_to_plot_weather, x="showed", y=col_name, ax=ax, width=0.5)

#         ax.bar_label(ax.containers[0])
#         st.pyplot(fig)

#         count += 1
#         if count >= 2:
#             count = 0

#         # axs[i, j].bar(patient_no_show_weather["showed"], patient_no_show_weather[columns[col_idx]], width = 0.25)
#         # axs[i, j].set_ylabel(columns[col_idx])
#         # axs[i, j].set_xticks([0, 1], ['No Show', 'Show'])

    
# # with row_1_col1:
# #     st.subheader("Average Waiting Time For Each Neighbourhood")

# #     ## Avg waiting time for each neighbourhood
# #     waitint_time_by_neighbourhood = df.groupby('neighbourhood').days_between_appointment_and_scheduled_day.mean()

# #     fig = Figure(figsize=(6, 18))
# #     ax = fig.subplots()

# #     data_to_plott_neighbourhood_avg = pd.DataFrame(waitint_time_by_neighbourhood).reset_index().rename(columns={"neighbourhood":"Neighbourhoods", "days_between_appointment_and_scheduled_day":"Avg Weight Time"})
# #     data_to_plott_neighbourhood_avg["Avg Weight Time"] = round(data_to_plott_neighbourhood_avg["Avg Weight Time"], 1)

# #     sns.barplot(data=data_to_plott_neighbourhood_avg, x="Avg Weight Time", y="Neighbourhoods", ax=ax)
    
# #     ax.bar_label(ax.containers[0])
# #     st.pyplot(fig)
