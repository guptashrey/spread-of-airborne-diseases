## Predictive Analytics on Spread of Influenza
**Bryce Whitney, Neha Barde, Shen Juin Lee, Shrey Gupta**

### Project Description
The ability to model and predict the spread of disease is a crucial problem after COVID-19 demonstrated the massive global ramifications of failing to control a contagious virus at the beginning. While COVID-19 is an extreme example, there are strong benefits of being able to model more common diseases such as Influenza. For hospitals this manifests in understanding how much staff and space they need to handle flu patients in a certain week, or when pharmaceutical companies should invest more in distributing vaccinations. For the population as a whole, it allows people to make more informed decisions to help teveryone avoid getting sick. 

Research has proven that mobility is one of the strongest indicators of how a disease will spread through a population at all geographic scales, whether it be locally, state-wide, or nationally. Nearly all research investigating the use of mobility data in predicting the spread of contagious diseases has highlighted the strong predictive power of mobility data. All this research shares one major flaw, which is that mobility data is the lone dataset being used in the model. We believe mobility alone doesn't fully cover the important factors dictating how disease spreads through a population. We believe data such as the weather and population of a particular region also play important roles in disease spread.  Through combing weather and population data with mobility data, we seek to explore the value these datasets can add through analysis of New York county Influenza data from 2019 to 2022. A strong ability to predict the amount of Influenza cases will allow us to inform New York Hospitals how much space and staff they will need to dedicate to flu patients and ensure the state can adapt guidelines or actions to keep as many people healthy as possible. 

### About the Data

We identified three key datasets that we believe will be beneficial in modeling and predicting the spread of Influenza: mobility data, weather data, and population data. We combined all this information together to predict our target variable, the number of Influenza cases for each New York County, for a given week. Specifically we use the features from 2 weeks beforehand to predict the number of cases in a given week. Find an in-depth description of each datset below:

#### Mobility Data
The mobility dataset used was collected from the [Google Mobility Report](https://www.google.com/covid19/mobility/).This data was originally collected for the purposes of COVID-19, but can be used to try and model the spread of different diseases around the same time. Data exists for every county in the U.S. for each day between 02/15/2019 and 10/15/2022. For the purposes of this project, we only use the data for New York counties. The data consists of the percent change in mobility for each of the following locations within a county.
- Residential and Recreation Areas
- Grocery Stores and Pharmacies
- Parks
- Transit Locations
- Workplace
- Reidential Locations

This change is compared to a baseline which was collected in February 2019 right before this dataset was compiled. The percent change in mobility can be positive or negative. Any missing values are assumed to have no change and encoded as 0.

#### Weather Data
Weather data was collected using the [Visual Crossing API](https://www.visualcrossing.com/). It was collected for every county in New York on a daily basis between January 2020 and September 2022. It includes a large variety of features such as the min, max, and average temperature, the wind spped, and the type/amount of precipitation among most other common weather measures. 

#### Population Data
Population data was also collected for every New York county from the [United States Census Bureau](https://www2.census.gov/programs-surveys/). This data consists of a single population estimate for each county for each year from 2019 - 2021. Since population doesn't tend to fluctuate much in the short-term, we think a yearly sample is more than sufficient to model any substancial changes in county populations. The population data consists of a total population estimate for each county, but also estimates the number of people who belong to different age buckets. These buckets are broken up as follows:
- People 0-4 years old
-	People 5-17 years old
-	People 18-49 years old
-	People 50-64 years old
-	People 65+ years old

#### Influenza Data

### Data Processing

### Accessing the Data
The processed data is stored in an Azure MySQL Database in the cloud. If you would like access to this Database, please email Shen Juin Lee at shenjuin.lee@duke.edu with your name and reason for accessing the data and we will be happy to provide access. 

We have provided a sample of the processed data in this repository under the `data` folder to showcase the format and information contained within each dataset. Please refer to the cloud Database if you would like complete access. 

### Running the Code
