import os
import streamlit as st
import pandas as pd
import preprocess as preprocess
import plots as plots

# Set the page title and icon
st.set_page_config(page_title="Airbnb EDA", page_icon=":house:", layout="wide")


@st.cache_data(persist=True)
def load_data(city):
    data = pd.read_csv(f"./data/{city}")
    data = preprocess.preprocess(data)
    return data


# Set the title
st.title("Airbnb Analysis")
st.subheader("INSY 662 - Group Project")

# Get filename of cities in data folder
cities = os.listdir("./data")
city_names = [city.split(".")[0].capitalize() for city in cities]
cities = dict(zip(city_names, cities))

# Create a selectbox to choose a city
city = st.selectbox("#### Select a city", cities, index=2)

if city:
    with st.container():
        city_name, file = city, cities[city]
        data = load_data(file)
        print(
            f"Data loaded for {city_name}. {data.shape[0]} rows and {data.shape[1]} columns."  # noqa: E501
        )

        # Tabs to select different plots
        tab_1, tab_2, tab_3, tab_4 = st.tabs(
            [
                "Price Distribution",
                "Price by Neighbourhood",
                "Price by Room Type",
                "Map",
            ]
        )

        with tab_1:
            st.pyplot(plots.price_distribution(data, city_name))

        with tab_2:
            price_by_neighbourhood = plots.price_by_neighbourhood(data, city_name)

            with st.expander("Count of listings by neighbourhood"):
                st.dataframe(price_by_neighbourhood[0], use_container_width=True)

            with st.expander("Price distribution by neighbourhood"):
                st.pyplot(price_by_neighbourhood[1])

            with st.expander("Average price by neighbourhood"):
                st.pyplot(price_by_neighbourhood[2])

        with tab_3:
            price_by_room_type = plots.price_by_room_type(data, city_name)

            with st.expander("Count of listings by room type"):
                st.dataframe(price_by_room_type[0], use_container_width=True)

            with st.expander("Price distribution by room type"):
                st.pyplot(price_by_room_type[1])

        with tab_4:
            map = plots.visualize_on_map(data)
            # map_html = map._repr_html_()

            st.components.v1.html(map, height=500)
