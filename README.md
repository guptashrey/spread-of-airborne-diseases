## Predictive Analytics on Spread of Influenza
**Bryce Whitney, Neha Barde, Shen Juin Lee, Shrey Gupta**

### Project Description
The ability to model and predict the spread of disease is a crucial problem after COVID-19 demonstrated the massive global ramifications of failing to control a contagious virus at the beginning. While COVID-19 is an extreme example, there are strong benefits of being able to model more common diseases such as Influenza. For hospitals this manifests in understanding how much staff and space they need to handle flu patients in a certain week, or when pharmaceutical companies should invest more in distributing vaccinations. For the population as a whole, it allows people to make more informed decisions to help teveryone avoid getting sick. 

Research has proven that mobility is one of the strongest indicators of how a disease will spread through a population at all geographic scales, whether it be locally, state-wide, or nationally. Nearly all research investigating the use of mobility data in predicting the spread of contagious diseases has highlighted the strong predictive power of mobility data. All this research shares one major flaw, which is that mobility data is the lone dataset being used in the model. We believe mobility alone doesn't fully cover the important factors dictating how disease spreads through a population. We believe data such as the weather and population of a particular region also play important roles in disease spread.  Through combing weather and population data with mobility data, we seek to explore the value these datasets can add through analysis of New York county Influenza data from 2019 to 2022. A strong ability to predict the amount of Influenza cases will allow us to inform New York Hospitals how much space and staff they will need to dedicate to flu patients and ensure the state can adapt guidelines or actions to keep as many people healthy as possible. 

### About the Data

We identified three key datasets that we believe will be beneficial in modeling and predicting the spread of Influenza: mobility data, weather data, and population data. We combined all this information together to predict our target variable, the number of Influenza cases for each New York County, for a given week. Specifically we use the features from 2 weeks beforehand to predict the number of cases in a given week. Find an in-depth description of each datset below:

#### Mobility Data
The mobility dataset used was collected from the [Google Mobility Report](https://www.google.com/covid19/mobility/). Google originally collected this data for the purposes of COVID-19, but it can be used to try and model the spread of different diseases around the same time. Data exists for every county in the U.S. for each day between 02/15/2019 and 10/15/2022. For the purposes of this project, we only use the data for New York counties. The data consists of the percent change in mobility for each of the following locations within a county.
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
The target data for this project is the number of Influenza cases in each New York county for a weekly basis. This data was gathered from the [New York State Health Department](https://health.data.ny.gov/Health/Influenza-Laboratory-Confirmed-Cases-By-County-Beg/jr8b-6gh6). Since we know Influenza tends to have an incubation period of ~2 days and is then contagious for another 3-4 days, analyzing the number of cases on a weekly basis makes more sense than doing it on a daily basis. One important note for this dataset is the CDC defines the "flu season" as October to May each year, which is when Influenza cases peak each year. For the purposes of this project, we are assuming there are no Influenza cases that occur outside the CDC-defined flu season. 

### Data Processing
Since the Influenza Data is processed at a weekly level, we need to ensure all our features are measured at a weekly level as well. This means we need to aggregate our daily data to weekly data, and expand our yearly data to weekly data. For the mobility data, we decided the percent change in mobility for a given location during the week would be equal to the average daily mobility change throughout the week. The average was used for each of the six features described above. The weather data required a little more thought. Whether the average or total sum was used depends on the nature of the feature itself. For example, temperature is a clear example where using the average temperature over the week makes more intuitive sense than using the sum of temperatures throughout the week. However, other features such as the amount of precipitation are more ambiguos to which metric makes more sense. We decided that the week's total precipitation would be more useful than the daily average. Finally, for the population data we assumed it stayed constant throughout the year. All the weeks in 2019 have the same county populations, then all the weeks in 2020 have new county populations, and so on through 2021. 


### Accessing the Data
The processed data is stored in an Azure MySQL Database in the cloud. If you would like access to this Database, please email Shen Juin Lee at shenjuin.lee[AT]duke[DOT]edu with your name and reason for accessing the data and we will be happy to provide access. 

We have provided a sample of the processed data in this repository under the `data` folder to showcase the format and information contained within each dataset. Please refer to the cloud Database if you would like complete access. 

### How to Run the Code
**1. Clone this repository**
```
git clone https://github.com/guptashrey/spread-of-airborne-diseases
```
**2. Create a conda environment:** 
```
conda create --name environ python=3.8
```
**3. Install requirements:** 
```
pip install -r requirements.txt
```
**4. Create a jupyter kernal from this environment:** 
```
python -m ipykernel install --user --name=environ
```
**5. Data Processing, EDA, and Modeling:**
* Run the `src/modeling.ipynb` file to process all the three datasets, engineer new features, handle outliers and prepare the final data for modelling. In addition, four Random Forest models are trained for each county - one each for 1-week, 2-week, 3-week, and 4-week advance case count prediction. The models are timestamped and stored in the MySQL database. Feature-importance charts are also plotted for each of the four Random Forest models that are trained.

**6. Prediction Generation:**
* Run the `src/prediction.ipynb` to load the models from the MySQL database and generate predictions for a specified timeframe. You will need to edit the first cell in the notebook to specify the beginning date of the predictions you wish to generate for.

**7. Influenza Forecast Engine:**
* Refer to the [README.md](https://github.com/guptashrey/spread-of-airborne-diseases/blob/st/README.md) at this link to run the streamlit based web application or access it [here](https://guptashrey-spread-of-airborne-diseases-streamlit-app-st-le86km.streamlit.app).
* You can find the code for the stremalit web-app [here](https://github.com/guptashrey/spread-of-airborne-diseases/tree/st)
