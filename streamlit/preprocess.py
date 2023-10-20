import streamlit as st
import pandas as pd


@st.cache_data(persist=True)
def preprocess(data: pd.DataFrame) -> pd.DataFrame:
    object_to_dtype = {
        "host_since": "datetime64[ns]",
        "host_response_rate": "float",
        "host_acceptance_rate": "float",
        "host_is_superhost": "bool",
        "host_has_profile_pic": "bool",
        "host_identity_verified": "bool",
        "instant_bookable": "bool",
        "has_availability": "bool",
    }

    for col, dtype in object_to_dtype.items():
        if dtype == "float":
            data[col] = data[col].str.replace("%", "").astype(dtype)
        elif dtype == "bool":
            data[col] = data[col].map({"t": True, "f": False}).astype(dtype)
        elif dtype == "datetime64[ns]":
            data[col] = pd.to_datetime(data[col])
        else:
            raise ValueError(f"Unknown dtype: {dtype}")

    data["price"] = data["price"].str.replace(r"[\$|,]", "", regex=True).astype(float)
    data["amenities"] = data["amenities"].str.replace(r"\[|\]|\"", "")

    data_cleaned = data[
        (data["price"] < data["price"].quantile(0.95)) & (data["minimum_nights"] <= 365)
    ]

    # Extract numerical value from `bathrooms_text` column
    data_cleaned["bathrooms"] = (
        data["bathrooms_text"].str.extract("(\d+\.?\d*)", expand=False).astype(float)
    )

    # Create new column `bathrooms_is_shared` indicating if bathroom is shared or not
    data_cleaned["bathrooms_is_shared"] = data["bathrooms_text"].str.contains(
        "shared", case=False
    )

    # Fill NAs for bedrooms with median value of bedrooms by neighbourhood
    data_cleaned["bedrooms"] = data_cleaned.groupby("neighbourhood_cleansed")[
        "bedrooms"
    ].transform(lambda x: x.fillna(x.median()))

    list_of_amenities = (
        data_cleaned["amenities"]
        .str.split(", ")
        .explode()
        .value_counts()
        .to_frame()
        .reset_index()
    )

    top_20_amenities = list_of_amenities.head(20)["index"].to_list()

    data_cleaned["num_amenities"] = (
        data_cleaned["amenities"]
        .apply(lambda x: x.split(", "))
        .apply(lambda y: len(set(y).intersection(set(top_20_amenities))))
    )

    return data_cleaned
