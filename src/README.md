## EDA
`weather_eda.ipynb` performs exploratory data analysis of weather data in relation with the target variable - influenza case count. Several charts and visualizations are made in the notebook, including a heat map of features-vs-feature and feature-vs-target correlation matrix for one county, a line chart of temperature-vs-target for a county, and a bar chart showing the F-score of each weather feature ranked from highest to lowest.

`seasonal_decompose.ipynb` performs a seasonal decomposition of one county's case count over the entire timeline of the data. From the plot, we observe that there is annual seasonality for influenza cases, and the peaks occurs during the winter season of every year.

## Modeling

Data processing and consolidation work is done in `modeling.ipynb`. It combines data from the multiple sources, removes outliers, imputes missing values, and other preparatory steps for modeling. Subsequently, it trains four separate Random Forest models for each county in New York state - one each for estimating influenza case counts 1-week, 2-week, 3-week, and 4-week in advance. The feature-importance charts of each model are plotted to provide an overview of the most important feature contributing to estimating the case counts. The models are timestamped and stored in the Azure MySQL database for ease of retrieval.

## Predictions
`prediction.ipynb` generates predictions of influenza case counts up to 4 weeks from a specified date. To specify a date, please edit the first cell in the notebook. It retrieves the trained Random Forest models from the Azure MySQL database for prediction generation. The predictions are subsequently written to the database for persistence and display on the user-facing Streamlit web application.