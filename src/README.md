## EDA


## Modeling

Data processing and consolidation work is done in `modeling.ipynb`. It combines data from the multiple sources, removes outliers, imputes missing values, and other preparatory steps for modeling. Subsequently, it trains four separate Random Forest models for each county in New York state - one each for estimating influenza case counts 1-week, 2-week, 3-week, and 4-week in advance. The feature-importance charts of each model are plotted to provide an overview of the most important feature contributing to estimating the case counts. The models are timestamped and stored in the Azure MySQL database for ease of retrieval.

## Predictions
`prediction.ipynb` generates predictions of influenza case counts up to 4 weeks from a specified date. To specify a date, please edit the first cell in the notebook. It retrieves the trained Random Forest models from the Azure MySQL database for prediction generation. The predictions are subsequently written to the database for persistence and display on the user-facing Streamlit web application.