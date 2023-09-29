# Proposal for INSY662 Group Project - Team 2

## Objective

Build a model to predict the nightly price of an Airbnb listing, given a set of features about the property and host

### Business value

This model will serve as a decision-making tool for hosts and guests, enabling hosts to set competitive prices that maximize their occupancy and revenue, and assisting guests in finding the best value for their money.

## Datasets

The dataset contains listing observations with information about the host, property, and reviews. We are planning to start with the following 5 cities:

1. Montreal, CA Listings ([Inside Airbnb: Montreal](http://insideairbnb.com/montreal)) - LA
2. Vancouver, CA Listings ([Inside Airbnb: Vancouver](http://insideairbnb.com/vancouver)) - NY
3. Boston, US Listings ([Inside Airbnb: Boston](http://insideairbnb.com/boston)) - MS
4. Munich, DE Listings ([Inside Airbnb: Munich](http://insideairbnb.com/munich)) - OS
5. Hong Kong, HK Listings ([Inside Airbnb: Hong Kong](http://insideairbnb.com/hong-kong)) - RK

### Scope

1. Data Collection: Gather Airbnb listing data from the five selected cities: Montreal, Vancouver, Boston, Munich, and Hong Kong. The data should include information about the host, property, and reviews.
2. Data Preprocessing: Clean the data by handling missing values, outliers, and incorrect data entries. Convert categorical data into a format that can be used in the model.
3. Exploratory Data Analysis (EDA): Conduct an exploratory analysis to understand the distribution of data, identify patterns and correlations, and gain insights into the factors that influence Airbnb prices in these cities.
4. Feature Engineering: Create new features that might improve the model's performance. This could include features derived from existing data, such as the distance to the city center or the number of popular attractions nearby.
5. Model Development: Develop a predictive model using machine learning techniques to forecast the nightly price of an Airbnb listing based on the given set of features.
6. Model Validation: Validate the model using a subset of the data to ensure it is accurately predicting the prices. Adjust and refine the model as necessary.
7. Model Deployment: Once the model is validated, deploy it in a suitable environment (such as Dash or Streamlit) where it can be used to make predictions on new data.
8. Documentation: Document all steps of the project, including the problem definition, data collection, data preprocessing, EDA, model development, model validation, and model deployment.
