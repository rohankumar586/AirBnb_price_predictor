import os
import streamlit as st
import pandas as pd
import preprocess as preprocess
import plots as plots
import model as model

# Set the page title and icon
st.set_page_config(page_title="Airbnb EDA", page_icon=":house:", layout="wide")


@st.cache_data(persist=True)
def load_data(city):
    data = pd.read_csv(f"./data/{city}")
    data = preprocess.preprocess(data)
    return data


# Get filename of cities in data folder
cities = sorted(os.listdir("./data"))
city_names = [city.split(".")[0].capitalize() for city in cities]
cities = dict(zip(city_names, cities))

# Create a selectbox to choose a city
with st.sidebar:
    st.title("Navigation")
    st.markdown(
        """
    ## This application provides various visualizations for Airbnb data analysis. 
    ### Select a city from the dropdown menu to view specific insights.
    """
    )
    st.header("Select a city")
    city = st.selectbox("Cities", cities, index=2, help="Select a city to view data")

if city:
    # Set the title
    st.title(f"Airbnb Analysis: {city.capitalize()}")
    with st.container():
        city_name, file = city, cities[city]

        rf, features_to_drop = model.load_model(city_name)

        data = load_data(file)
        print(
            f"Data loaded for {city_name}. {data.shape[0]} rows and {data.shape[1]} columns."  # noqa: E501
        )

        # Tabs to select different plots
        tab_1, tab_2, tab_3, tab_4, tab_5, tab_6 = st.tabs(
            [
                "📊 Price Distribution",
                "📌 Map of Listings",
                "🍁 Price by Neighbourhood",
                "🏡 Price by Room Type",
                "📶 Price by Amenities",
                "🤑 Predict price",
            ]
        )

        with tab_1:
            st.markdown("## Price Distribution Overview")
            st.markdown(
                "This tab shows the overall distribution of listing prices within the selected city."  # noqa: E501
            )
            st.plotly_chart(
                plots.price_distribution(data, city_name), use_container_width=True
            )

        with tab_2:
            map = plots.visualize_on_map(data)

            st.components.v1.html(map, height=500)

        with tab_3:
            st.markdown("## Neighborhood Analysis")
            st.markdown(
                """
                Explore how listing prices vary by neighborhood. 
                Insights include the count of listings, price distribution, and average prices per neighborhood.
                """  # noqa: E501
            )

            # Organizing content in columns
            col1, col2 = st.columns(2)

            price_by_neighbourhood = plots.price_by_neighbourhood(data, city_name)
            with col1:
                st.plotly_chart(price_by_neighbourhood[0], use_container_width=True)

            with col2:
                st.plotly_chart(price_by_neighbourhood[1], use_container_width=True)

            st.plotly_chart(price_by_neighbourhood[2], use_container_width=True)

        with tab_4:
            st.markdown("## Room Type Analysis")
            st.markdown(
                """
                Explore how listing prices vary by room type. 
                Insights include the count of listings and price distribution by room type.
                """  # noqa: E501
            )

            price_by_room_type = plots.price_by_room_type(data, city_name)

            col1, col2 = st.columns(2)

            with col1:
                st.plotly_chart(price_by_room_type[0], use_container_width=True)

            with col2:
                st.plotly_chart(price_by_room_type[1], use_container_width=True)

        with tab_5:
            st.markdown("## Amenities Analysis")
            st.markdown(
                """
                Explore how listing prices vary by amenities. 
                Insights include the count of listings and price distribution by amenities for the top 20 amenities.
                """  # noqa: E501
            )

            price_by_amenities = plots.price_by_amenities(data, city_name)

            st.plotly_chart(price_by_amenities[0], use_container_width=True)

            st.plotly_chart(price_by_amenities[1], use_container_width=True)

        with tab_6:
            st.markdown("## Predict the price of a listing")
            st.markdown(
                """
                Enter the details of the listing you want to predict the price for. 
                The model will predict the price based on the input provided.
                """  # noqa: E501
            )

            submitted, user_input = model.get_user_input(data, features_to_drop)

            if submitted:
                # st.dataframe(user_input.T, use_container_width=True)

                currency_prefix, prediction = model.predict(rf, user_input, city_name)
                st.markdown(
                    f"""
                    #### Predicted Price: {currency_prefix}{prediction:.2f} / night
                    """
                )
