# Imports
import os
import pandas as pd
import numpy as np
import zipfile
from urllib.request import urlopen
from io import BytesIO

MONTHS = {
    '01':'January',
    '02':'February',
    '03':'March',
    '04':'April',
    '05':'May',
    '06':'June',
    '07':'July',
    '08':'August',
    '09':'September',
    '10':'October',
    '11':'November',
    '12':'December',
}

##################################
# Google Mobility Data Functions #
##################################

def download_google_mobility_data(output_folder=''):
    """Downloads the google mobility data and saves it as a CSV.
    data source: https://www.google.com/covid19/mobility/
       
    Args:
        output_folder (str, optional): the folder where the data will be output. Defaults to ''.
    """
    
    # Get URL for the data
    url = 'https://www.gstatic.com/covid19/mobility/Region_Mobility_Report_CSVs.zip'
    
    # Download and extract the zipfolder
    with urlopen(url) as zipResponse:
        with zipfile.ZipFile(BytesIO(zipResponse.read())) as zipFolder:
            # Identify the United States Data
            US_files = [file for file in zipFolder.namelist() if(file[5:7] == 'US')]
            
            # Extract the US data
            for file in US_files:
                zipFolder.extract(file, path=output_folder)

                
def load_google_mobility_data(data_path=''):
    """Loads the google mobility data into a dataframe and returns the dataframe. 
    Any data that is missing a state or county is removed. 

    Args:
        data_path (str, optional): path to the folder containing the data. Defaults to ''.

    Returns:
        google_mobility_data (pd.DataFrame): The dataframe containing the google mobility data
    """
    
    # Combine all the data
    google_data = []
    for file in os.listdir(data_path):
        if file[-3:] == "csv":
            file_path = os.path.join(data_path, file)
            google_data.append(pd.read_csv(file_path))
            
    google_mobility_data = pd.concat([data for data in google_data])
    
    # Rename the columns
    google_mobility_data = google_mobility_data.rename(columns={
                                                'country_region_code':'country_code',
                                                'country_region':'country',
                                                'sub_region_1':'state',
                                                'sub_region_2':'county',
                                                'retail_and_recreation_percent_change_from_baseline':'retail_and_recreation_percent_change',
                                                'grocery_and_pharmacy_percent_change_from_baseline':'grocery_and_pharmacy_percent_change',
                                                'parks_percent_change_from_baseline':'parks_percent_change',
                                                'transit_stations_percent_change_from_baseline':'transit_stations_percent_change',
                                                'workplaces_percent_change_from_baseline':'workplaces_percent_change',
                                                'residential_percent_change_from_baseline':'residential_percent_change',
                                                })
    
    # Keep only the important columns
    google_mobility_data = google_mobility_data[['date', 'country_code', 'country', 'state', 'county', \
                                                'retail_and_recreation_percent_change', 'grocery_and_pharmacy_percent_change', \
                                                'parks_percent_change', 'transit_stations_percent_change', 'workplaces_percent_change', \
                                                'residential_percent_change', 'place_id', 'census_fips_code']]
    
    # Remove data where state or county info is null
    google_mobility_data = google_mobility_data[google_mobility_data['state'].isna() == False]
    google_mobility_data = google_mobility_data[google_mobility_data['county'].isna() == False]

    # Sort by country, state, county, and date
    google_mobility_data = google_mobility_data.sort_values(by=['country', 'state', 'county', 'date'], ascending=True, inplace=False).reset_index(drop=True)
        
    # Return the data
    return google_mobility_data


#################################
# GeoDS Mobility Data Functions #
#################################

###############
# COUNTY DATA #
###############
def download_weekly_county_data(start_date, end_date, output_folder='data', output_filename='weekly_county_data.csv', valid_fips=None):
    """Downloads geoDS mobility data from https://github.com/GeoDS/COVID19USFlows for every week between start_date and end_date. 
    start_date and end_date must both be mondays. if valid_fips is passed, the data is filtered to only the observations 
    where the fips code appears in either the origin or destination county.

    Args:
        start_date (string): string representing the first day to get data for. Must be a monday.
        end_date (string): string representing the last day to get data for. Must be a monday.
        output_folder (str, optional): Folder to output the data. Defaults to 'data'.
        output_filename (str, optional): Name of the file to be output. This should include the file extension '.csv'. Defaults to 'weekly_county_data.csv'.
        valid_fips (list, optional): A set of FIPS codes that the user wants to investigate. Defaults to None.
    """
    
    # Track months to help user know where in download process they are
    last_month = None
    current_month = pd.to_datetime(start_date).month
    
    all_data = [] 
    scale='county2county' # Download the county data
    
    # Loop through all the dates
    for date in pd.date_range(start_date, end_date, freq='7D'):
        # Get the url of the data
        day, month, year = str(date.day).zfill(2), str(date.month).zfill(2), str(date.year).zfill(4)
        url=f"https://raw.githubusercontent.com/GeoDS/COVID19USFlows-WeeklyFlows/master/weekly_flows/{scale}/weekly_{scale}_{year}_{month}_{day}.csv"
        
        # Check when month changes for user's convenience
        current_month = month
        if(current_month != last_month):
            last_month = current_month
            print(f'Gathering Data for {MONTHS[month]} {year}')
        
        # Read the data
        df = pd.read_csv(url)
        df = df[(df['geoid_o'].isin(valid_fips)) | (df['geoid_d'].isin(valid_fips))]
        
        # Append the data to the list of daily data
        all_data.append(df)
        
    
    # Concatenate the data into a single dataframe
    combined_df = pd.concat([data for data in all_data])
    
    # Save the current data as a CSV
    combined_df.to_csv(os.path.join(output_folder, output_filename))
    

def load_weekly_county_data(file_path):
    """Loads the weekly geoDS mobility data and returns it as a dataframe

    Args:
        file_path (str): path to the data

    Returns:
        geoDS_mobility_data (pd.DataFrame): dataframe containing the geoDS mobility data
    """
    # Load the data
    geoDS_mobility_data = pd.read_csv(file_path)  
        
    # Remove unnecessary columns
    geoDS_mobility_data = geoDS_mobility_data.iloc[:, 1:-2]
    
    # Return the dataframe
    return geoDS_mobility_data


##################
# FIPS Code Data #
##################

def load_fips_codes(file_path):
    """Loads data for the Fips codes of states and counties in the United States. 
    A dataframe is created for both states and counties, containing the code and the state/county name.
    

    Args:
        file_path (str): path to the data

    Returns:
        state_codes_df (pd.DataFrame): Dataframe containing a mapping of state FIPS codes.
        county_codes_df (pd.DataFrame): Dataframe containing a mapping of county FIPS codes.
    """
    # Get state codes
    state_codes_df = pd.read_csv(file_path, sep='\t', skiprows=15, nrows=50)
    state_codes_df[['code', 'state']] = state_codes_df.iloc[:,0].str.strip().str.split(' ', 1, expand=True)
    state_codes_df = state_codes_df.iloc[:, 1:]    
    
    # Get the county codes
    county_codes_df = pd.read_csv(file_path, sep='\t', skiprows=71)
    county_codes_df[['code', 'county']] = county_codes_df.iloc[:,0].str.strip().str.split(' ', 1, expand=True)
    county_codes_df = county_codes_df.iloc[:, 1:] 

    # Return the dataframes
    return state_codes_df, county_codes_df
    
    