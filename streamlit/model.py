import streamlit as st
from streamlit_extras.grid import grid
from streamlit_extras.row import row
import pandas as pd
import numpy as np
import joblib


@st.cache_resource
def load_model(city):
    model = joblib.load(f"./models/{city}_random_forest.joblib")
    return model


def create_selectbox(row_item: row, data: pd.DataFrame, column: str, label: str = None):
    options = column + "_" + data[column].dropna().unique()

    if label is None:
        label = column.replace("_", " ").capitalize()

    selectbox = row_item.selectbox(
        label=label,
        options=options,
        format_func=lambda x: x.split("_")[-1],
    )

    return selectbox, options


def get_user_input(data: pd.DataFrame):
    list_of_amenities = sorted(
        (
            data["amenities"]
            .str.split(", ")
            .explode()
            .value_counts()
            .to_frame()
            .reset_index()
            .head(20)
        )["index"].tolist()
    )

    host_verification_time_options = [
        "host_verification_email",
        "host_verification_phone",
        "host_verification_work_email",
    ]

    with st.form("input_form"):
        with st.expander("**Listing information**", expanded=True):
            room_details = grid(
                1, [1, 1, 1], [1, 1, 1], 1, [1, 1], vertical_align="center"
            )
            room_type, room_type_options = create_selectbox(
                room_details, data, "room_type", label="Room Type"
            )

            accommodates = room_details.number_input("Number of Guests", value=1)
            bedrooms = room_details.number_input("Number of Bedrooms", value=1)
            beds = room_details.number_input("Number of Beds", value=1)

            bathrooms = room_details.number_input("Number of Bathrooms", value=1)
            bathrooms_text, bathrooms_text_options = create_selectbox(
                room_details, data, "bathrooms_text", label="Bathrooms Type"
            )
            bathrooms_is_shared = room_details.checkbox("Bathrooms is Shared?")

            neighbourhood, neighbourhood_options = create_selectbox(
                room_details, data, "neighbourhood_cleansed", label="Neighbourhood"
            )
            amenities = room_details.multiselect(
                "Amenities", options=list_of_amenities, default=[]
            )

            num_amenities = room_details.number_input(
                "Number of amenities",
                value=len(amenities),
                min_value=0,
            )

        with st.expander("**Booking information**"):
            booking_details = grid([1, 1], [1, 1, 1], vertical_align="center")

            minimum_nights = booking_details.slider(
                "Minimum Nights", value=1, min_value=1
            )
            maximum_nights = booking_details.slider(
                "Maximum Nights", value=1, min_value=1
            )

            has_availability = booking_details.toggle("Has Availability?", value=True)
            instant_bookable = booking_details.checkbox("Is it bookable instantly?")
            availability_365 = booking_details.number_input(
                "The availability of the listing 365 days in the future", value=1
            )

        with st.expander("**Host information**"):
            host_detail = grid([1, 1, 1, 1], 1, vertical_align="center")
            host_response_time, host_response_time_options = create_selectbox(
                host_detail, data, "host_response_time", label="Host Response Time"
            )

            host_verification_time = host_detail.multiselect(
                "Host Verification",
                options=host_verification_time_options,
                format_func=lambda x: x.split("_", maxsplit=2)[-1].capitalize(),
            )

            host_acceptance_rate = (
                host_detail.slider(
                    "Host Acceptance Rate",
                    min_value=0,
                    max_value=100,
                    format="%d%%",
                )
                / 100
            )

            host_is_superhost = host_detail.toggle("Is Superhost?")

            host_listings_count = host_detail.number_input(
                "Host Listings Count", value=1
            )

        submitted = st.form_submit_button("Submit", type="primary")

    if submitted:
        columns = [
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
        ]

        columns.extend(list_of_amenities)
        columns.extend(host_verification_time_options)
        columns.extend(host_response_time_options)
        columns.extend(neighbourhood_options)
        columns.extend(room_type_options)
        columns.extend(bathrooms_text_options)

        user_input = pd.DataFrame(
            np.zeros_like(columns, dtype=int).reshape(1, -1),
            columns=columns,
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

        return submitted, user_input
    else:
        return submitted, None


def predict(model, input):
    prediction = model["model"].named_steps["model"].predict(input)
    return np.exp(prediction)
