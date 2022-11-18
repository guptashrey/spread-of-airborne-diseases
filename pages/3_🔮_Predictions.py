import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st. title("Page 2")
# COUNTIES = ['ALBANY', 'ALLEGANY', 'BRONX', 'BROOME', 'CATTARAUGUS', 'CAYUGA', 'CHAUTAUQUA', 'CHEMUNG', 'CHENANGO', 'CLINTON', 'COLUMBIA', 'CORTLAND', 'DELAWARE', 'DUTCHESS', 'ERIE', 'ESSEX', 'FRANKLIN', 'FULTON', 'GENESEE', 'GREENE', 'HAMILTON', 'HERKIMER', 'JEFFERSON', 'KINGS', 'LEWIS', 'LIVINGSTON', 'MADISON', 'MONROE', 'MONTGOMERY', 'NASSAU', 'NEW YORK', 'NIAGARA', 'ONEIDA', 'ONONDAGA', 'ONTARIO', 'ORANGE', 'ORLEANS', 'OSWEGO', 'OTSEGO', 'PUTNAM', 'QUEENS', 'RENSSELAER', 'RICHMOND', 'ROCKLAND', 'SARATOGA', 'SCHENECTADY', 'SCHOHARIE', 'SCHUYLER', 'SENECA', 'ST LAWRENCE', 'STEUBEN', 'SUFFOLK', 'SULLIVAN', 'TIOGA', 'TOMPKINS', 'ULSTER', 'WARREN', 'WASHINGTON', 'WAYNE', 'WESTCHESTER', 'WYOMING', 'YATES']
# COUNTIES = [i + " COUNTY" for i in COUNTIES]
# with st.container():
#     county = st.selectbox("Select a neighbourhood", COUNTIES).strip()
#     #county = str.upper(county) + " COUNTY"

# google_mobility_data_NY_cleaned = pd.read_csv('./data/google_mobility_data.csv').iloc[:, 1:]
# google_mobility_data_NY_cleaned["county"] = [str.upper(i) for i in list(google_mobility_data_NY_cleaned["county"])]
# if(google_mobility_data_NY_cleaned[google_mobility_data_NY_cleaned['county'] == county].shape[0] < len(google_mobility_data_NY_cleaned['date'].unique())):
#     county_data = google_mobility_data_NY_cleaned[google_mobility_data_NY_cleaned['county'] == county].merge(google_mobility_data_NY_cleaned[google_mobility_data_NY_cleaned['county'] == 'Albany County']['date'], how='right', on='date').ffill()
# else:
#     county_data = google_mobility_data_NY_cleaned[google_mobility_data_NY_cleaned['county'] == county]

# # def plot_every_feature_for_county(county):
# #     """Returns a figure that represents a plot of every feature in the google mobility
# #        data over time for the specified county. 

# #     Args:
# #         county (str): specified county name

# #     Returns:
# #         fig (matplotlib.figure.Figure): figure containing the resulting plot
# #     """
# #     feat_names = ['Retail and \nRecreation', 'Grocery and \nPharmacy', 'Parks', 'Transit \nStations', 'Work', 'Residential']
# #     colors = ['blue', 'green', 'red', 'pink', 'purple', 'orange']
    
# #     # Ensure all the dates are present for each county
# #     if(google_mobility_data_NY_cleaned[google_mobility_data_NY_cleaned['county'] == county].shape[0] < len(google_mobility_data_NY_cleaned['date'].unique())):
# #         county_data = google_mobility_data_NY_cleaned[google_mobility_data_NY_cleaned['county'] == county].merge(google_mobility_data_NY_cleaned[google_mobility_data_NY_cleaned['county'] == 'Albany County']['date'], how='right', on='date').ffill()
# #     else:
# #         county_data = google_mobility_data_NY_cleaned[google_mobility_data_NY_cleaned['county'] == county]
        
# #     # Plot the features
# #     fig = plt.figure()
    
# #     plt.plot(county_data['date'], [0]*county_data.shape[0], label='Baseline', color='black', linewidth=2)
# #     for i, (feat, name) in enumerate(zip(county_data.columns[3:], feat_names)):
# #         plt.plot(county_data['date'], county_data[feat], label=name, color=colors[i])
        
# #     plt.xlabel('Date')
# #     plt.ylabel('% Change from Baseline')
# #     plt.title(f'Mobility Changes for {county}')
# #     plt.legend(loc='right', ncol=1, shadow=True, bbox_to_anchor=(1.28, .5))
# #     plt.xticks(rotation=90)
    
# #     # Only keep every 8th tick
# #     for i, label in enumerate(fig.axes[0].xaxis.get_ticklabels()):
# #         if(i % 8 == 0):
# #             label.set_visible(True)
# #         else:
# #             label.set_visible(False)
    
# #     return fig

# # fig = plot_every_feature_for_county('Albany County')
# # st.pyplot(fig)

# feat_names = ["retail_and_recreation_percent_change","grocery_and_pharmacy_percent_change","parks_percent_change","transit_stations_percent_change","workplaces_percent_change","residential_percent_change"]
# st.line_chart(data = county_data, x = "date", y = feat_names)