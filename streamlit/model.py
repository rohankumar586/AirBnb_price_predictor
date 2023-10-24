from calendar import c
import streamlit as st
import pandas as pd
import numpy as np
import joblib


@st.cache_resource
def load_model(city):
    # model = joblib.load(f"./models/{city}_random_forest.joblib")
    model = joblib.load(f"./models/{city}_random_forest.joblib")
    return model


def create_selectbox(data: pd.DataFrame, column: str, multi: bool = False):
    if multi:
        selectbox = st.multiselect(
            column.replace("_", " ").capitalize(),
            options=column + "_" + data[column].dropna().unique(),
            format_func=lambda x: x.split("_")[-1],
        )
    else:
        selectbox = st.selectbox(
            column.replace("_", " ").capitalize(),
            options=column + "_" + data[column].dropna().unique(),
            format_func=lambda x: x.split("_")[-1],
        )
    return selectbox


def get_user_input(data: pd.DataFrame):
    accommodates = st.number_input("Number of Guests", value=1)
    bathrooms = st.number_input("Number of Bathrooms", value=1)
    bedrooms = st.number_input("Number of Bedrooms", value=1)
    beds = st.number_input("Number of Beds", value=1)

    amenities_list = [
        "Bed linens",
        "Cooking basics",
        "Dedicated workspace",
        "Dishes and silverware",
        "Essentials",
        "Hair dryer",
        "Hangers",
        "Heating",
        "Hot water",
        "Iron",
        "Kitchen",
        "Long term stays allowed",
        "Microwave",
        "Oven",
        "Refrigerator",
        "Self check-in",
        "Shampoo",
        "Smoke alarm",
        "Washer",
        "Wifi",
    ]

    amenities = st.multiselect("Amenities", options=amenities_list, default=["Wifi"])

    room_type = create_selectbox(data, "room_type")
    neighbourhood = create_selectbox(data, "neighbourhood_cleansed")
    bathrooms_text = create_selectbox(data, "bathrooms_text")
    host_response_time = create_selectbox(data, "host_response_time")

    host_verification_time = st.multiselect(
        "Host Verification",
        options=[
            "host_verification_email",
            "host_verification_phone",
            "host_verification_work_email",
        ],
        format_func=lambda x: x.split("_", maxsplit=2)[-1].capitalize(),
    )

    """
    host_acceptance_rate',
    'host_is_superhost',
    'host_listings_count',
    'accommodates',
    'bathrooms',
    'bedrooms',
    'beds',
    'minimum_nights',
    'maximum_nights',
    'has_availability',
    'availability_365',
    'instant_bookable',
    'bathrooms_is_shared',
    'num_amenities',
    """
    host_acceptance_rate = st.number_input(
        "Host Acceptance Rate", min_value=0.0, max_value=1.0, step=0.1
    )

    host_is_superhost = st.checkbox("Is Superhost?")

    host_listings_count = st.number_input("Host Listings Count", value=1)

    minimum_nights = st.number_input("Minimum Nights", value=1)

    maximum_nights = st.number_input("Maximum Nights", value=1)

    has_availability = st.checkbox("Has Availability?")

    availability_365 = st.number_input("Availability 365", value=1)

    instant_bookable = st.checkbox("Instant Bookable?")

    bathrooms_is_shared = st.checkbox("Bathrooms is Shared?")

    num_amenities = st.number_input("Number of Amenities", value=1)

    ## Create a dataframe with user inputs
    ## Columns are:

    user_input = pd.DataFrame(
        np.zeros((1, 101)),
        columns=[
            "host_acceptance_rate",
            "host_is_superhost",
            "host_listings_count",
            "accommodates",
            "bathrooms",
            "bedrooms",
            "beds",
            "minimum_nights",
            "maximum_nights",
            "has_availability",
            "availability_365",
            "instant_bookable",
            "bathrooms_is_shared",
            "num_amenities",
            "Bed linens",
            "Cooking basics",
            "Dedicated workspace",
            "Dishes and silverware",
            "Essentials",
            "Hair dryer",
            "Hangers",
            "Heating",
            "Hot water",
            "Iron",
            "Kitchen",
            "Long term stays allowed",
            "Microwave",
            "Oven",
            "Refrigerator",
            "Self check-in",
            "Shampoo",
            "Smoke alarm",
            "Washer",
            "Wifi",
            "host_verification_email",
            "host_verification_phone",
            "host_verification_work_email",
            "host_response_time_a few days or more",
            "host_response_time_within a day",
            "host_response_time_within a few hours",
            "host_response_time_within an hour",
            "neighbourhood_cleansed_Ahuntsic-Cartierville",
            "neighbourhood_cleansed_Anjou",
            "neighbourhood_cleansed_Baie-d'Urfé",
            "neighbourhood_cleansed_Beaconsfield",
            "neighbourhood_cleansed_Côte-Saint-Luc",
            "neighbourhood_cleansed_Côte-des-Neiges-Notre-Dame-de-Grâce",
            "neighbourhood_cleansed_Dollard-des-Ormeaux",
            "neighbourhood_cleansed_Dorval",
            "neighbourhood_cleansed_Hampstead",
            "neighbourhood_cleansed_Kirkland",
            "neighbourhood_cleansed_L'Île-Bizard-Sainte-Geneviève",
            "neighbourhood_cleansed_L'Île-Dorval",
            "neighbourhood_cleansed_LaSalle",
            "neighbourhood_cleansed_Lachine",
            "neighbourhood_cleansed_Le Plateau-Mont-Royal",
            "neighbourhood_cleansed_Le Sud-Ouest",
            "neighbourhood_cleansed_Mercier-Hochelaga-Maisonneuve",
            "neighbourhood_cleansed_Mont-Royal",
            "neighbourhood_cleansed_Montréal-Est",
            "neighbourhood_cleansed_Montréal-Nord",
            "neighbourhood_cleansed_Montréal-Ouest",
            "neighbourhood_cleansed_Outremont",
            "neighbourhood_cleansed_Pierrefonds-Roxboro",
            "neighbourhood_cleansed_Pointe-Claire",
            "neighbourhood_cleansed_Rivière-des-Prairies-Pointe-aux-Trembles",
            "neighbourhood_cleansed_Rosemont-La Petite-Patrie",
            "neighbourhood_cleansed_Saint-Laurent",
            "neighbourhood_cleansed_Saint-Léonard",
            "neighbourhood_cleansed_Sainte-Anne-de-Bellevue",
            "neighbourhood_cleansed_Senneville",
            "neighbourhood_cleansed_Verdun",
            "neighbourhood_cleansed_Ville-Marie",
            "neighbourhood_cleansed_Villeray-Saint-Michel-Parc-Extension",
            "neighbourhood_cleansed_Westmount",
            "room_type_Entire home/apt",
            "room_type_Hotel room",
            "room_type_Private room",
            "room_type_Shared room",
            "bathrooms_text_0 baths",
            "bathrooms_text_1 bath",
            "bathrooms_text_1 private bath",
            "bathrooms_text_1 shared bath",
            "bathrooms_text_1.5 baths",
            "bathrooms_text_1.5 shared baths",
            "bathrooms_text_2 baths",
            "bathrooms_text_2 shared baths",
            "bathrooms_text_2.5 baths",
            "bathrooms_text_2.5 shared baths",
            "bathrooms_text_3 baths",
            "bathrooms_text_3 shared baths",
            "bathrooms_text_3.5 baths",
            "bathrooms_text_4 baths",
            "bathrooms_text_4 shared baths",
            "bathrooms_text_5 baths",
            "bathrooms_text_5 shared baths",
            "bathrooms_text_6 baths",
            "bathrooms_text_8 baths",
            "bathrooms_text_8 shared baths",
            "bathrooms_text_Half-bath",
            "bathrooms_text_Shared half-bath",
        ],
    )

    user_input["host_acceptance_rate"] = host_acceptance_rate
    user_input["host_is_superhost"] = host_is_superhost
    user_input["host_listings_count"] = host_listings_count
    user_input["accommodates"] = accommodates
    user_input["bathrooms"] = bathrooms
    user_input["bedrooms"] = bedrooms
    user_input["beds"] = beds
    user_input["minimum_nights"] = minimum_nights
    user_input["maximum_nights"] = maximum_nights
    user_input["has_availability"] = has_availability
    user_input["availability_365"] = availability_365
    user_input["instant_bookable"] = instant_bookable
    user_input["bathrooms_is_shared"] = bathrooms_is_shared
    user_input["num_amenities"] = num_amenities

    for amenity in amenities:
        user_input[amenity] = 1

    for verification in host_verification_time:
        user_input[verification] = 1

    user_input[room_type] = 1
    user_input[neighbourhood] = 1
    user_input[bathrooms_text] = 1
    user_input[host_response_time] = 1

    return user_input


def predict(model, input):
    prediction = model["model"].named_steps["model"].predict(input)
    return np.exp(prediction)
