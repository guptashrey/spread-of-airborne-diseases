## Data Folder
This folder contains the data we used for our project in case someone wants to use it without accessing the database in the cloud. There are three subfolders in this directory and below explains what each of them contains: `raw`, `processed`, and `scripts`

### Raw Data
As the `raw` folder suggests, this is where our uncleaned data is stored. Data is directly downloaded and stored here before being processed in case something in the cleaning goes wrong. The data in this folder is not used directly in any of our applications. 

### Processed Data
Naturally the `processed` folder contains all the data once it has been cleaned and is ready for use. It contains a CSV for all the major data sources we used, and is the same data we uploaded to the cloud database. This data is not used directly in our applications but serves as a nice backup in case something in the cloud database goes wrong. 

### Data Retrieval and Processing Scripts

The `scripts` folder contains the python notebooks that were used to download and clean the data. They were also used to upload the cleaned data into the database which was used for our modeling and Streamlit dashoboard. There is one notebook for each of the major data sources we used: mobility, weather, population, and Influenza data
