import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import folium
from folium import plugins, branca

sns.set_style("whitegrid")
sns.set_context("talk")


# @st.cache_data(persist=True)
def price_distribution(data: pd.DataFrame, city: str) -> plt.Axes:
    fig = plt.figure(figsize=(12, 4))
    ax = sns.histplot(data=data, x="price", color="r", bins=20, kde=True)
    ax.set_title(f"Price distribution in {city.capitalize()}")
    ax.set_xlabel("Price")

    plt.tight_layout()
    return fig


# @st.cache_data(persist=True)
def price_by_neighbourhood(data: pd.DataFrame, city: str):
    num_listings_by_neighborhood = (
        data["neighbourhood_cleansed"].value_counts().reset_index()
    )
    # .rename(columns={"index": "neighbourhood", "neighbourhood_cleansed": "count"})

    # num_listings_by_neighborhood.style.background_gradient(
    #     sns.light_palette("red", as_cmap=True)
    # ).set_properties(**{"text-align": "center"}).set_table_styles(
    #     [
    #         dict(selector="th", props=[("text-align", "center")]),
    #         dict(
    #             selector="caption",
    #             props=[("font-size", "14px"), ("font-weight", "bold")],
    #         ),
    #     ],
    # ).set_caption(
    #     f"Number of listings by neighborhood in {city.capitalize()}"
    # ).relabel_index(
    #     {0: "Neighborhood", 1: "# of listings"},
    #     axis="columns",
    # )

    # Then, we see the price of listings in the top 15 neighbourhoods
    st.write(num_listings_by_neighborhood)
    fig_1 = plt.figure(figsize=(10, 12))
    ax = sns.boxplot(
        data=data[
            data["neighbourhood_cleansed"].isin(
                num_listings_by_neighborhood.iloc[:15]["neighbourhood"].values
            )
        ],
        y="neighbourhood_cleansed",
        x="price",
        order=num_listings_by_neighborhood.iloc[:15]["neighbourhood"].values,
        palette="Reds_r",
    )
    ax.set_title(
        f"Distribution of price in {city.capitalize()} by neighbourhood (top 15)"
    )
    ax.set_ylabel("Neighbourhood")
    ax.set_xlabel("Price")

    # Finally, we plot the mean price of listings in the top 15 neighbourhoods
    avg_price_by_neighborhood = (
        (
            data[
                data["neighbourhood_cleansed"].isin(
                    num_listings_by_neighborhood.iloc[:15]["neighbourhood"].values
                )
            ]
            .groupby("neighbourhood_cleansed")["price"]
            .agg(["mean", "count"])
        )
        .reindex(index=num_listings_by_neighborhood.iloc[:15]["neighbourhood"].values)
        .reset_index()
    )

    fig_2 = plt.figure(figsize=(10, 12))
    ax = sns.barplot(
        avg_price_by_neighborhood,
        y="neighbourhood_cleansed",
        x="mean",
        order=num_listings_by_neighborhood.iloc[:15]["neighbourhood"].values,
        palette="Reds_r",
    )

    for i in range(15):
        ax.text(
            0,
            i,
            f"N={avg_price_by_neighborhood.iloc[i]['count']}",
            va="center",
            fontsize=12,
        )

    ax.set_title(
        f"Average price of listings in {city.capitalize()} by neighbourhood (top 15)"
    )
    ax.set_ylabel("Neighbourhood")
    ax.set_xlabel("Average price")

    return num_listings_by_neighborhood, fig_1, fig_2


# @st.cache_data(persist=True)
def price_by_room_type(data: pd.DataFrame, city: str):
    # First, we check the `room_type` column
    num_listings_by_room_type = (
        data["room_type"]
        .value_counts()
        .to_frame()
        .reset_index()
        .rename(columns={"index": "room_type", "room_type": "count"})
    )

    # num_listings_by_room_type.style.background_gradient(
    #     sns.light_palette("red", as_cmap=True)
    # ).set_properties(**{"text-align": "center"}).set_table_styles(
    #     [
    #         dict(selector="th", props=[("text-align", "center")]),
    #         dict(
    #             selector="caption",
    #             props=[("font-size", "14px"), ("font-weight", "bold")],
    #         ),
    #     ],
    # ).set_caption(
    #     f"Number of listings by room type in {city.capitalize()}"
    # ).relabel_index(
    #     {0: "Room type", 1: "# of listings"},
    #     axis="columns",
    # )

    fig = plt.figure(figsize=(12, 10))
    ax = sns.violinplot(
        data=data,
        x="room_type",
        y="price",
        hue="room_type",
        order=num_listings_by_room_type.room_type.values,
    )
    ax.set_title(f"Distribution of price in {city.capitalize()} listings by room type")
    ax.set_ylabel("Price")
    ax.set_xlabel("Room type")

    return num_listings_by_room_type, fig


@st.cache_resource
def visualize_on_map(data: pd.DataFrame):
    map = folium.Map(
        location=[data["latitude"].mean(), data["longitude"].mean()],
        zoom_start=12,
        max_zoom=20,
        tiles=None,
    )

    folium.TileLayer("cartodbpositron", opacity=0.8, control=False).add_to(map)

    # Create a color scale based on the price of listings in data
    vmin = data["price"].quantile(0.05)
    vmax = data["price"].quantile(0.95)

    colors = ["green", "lightgreen", "yellow", "orange", "red"]
    price_scale = branca.colormap.LinearColormap(
        colors,
        vmin=vmin,
        vmax=vmax,
        caption="Price",
        index=[
            vmin,
            (vmin + vmax) / 4,
            (vmin + vmax) / 2,
            3 * (vmin + vmax) / 4,
            vmax,
        ],
    )

    price_scale = price_scale.to_step(15)

    price_scale.add_to(map)

    listings_group = plugins.MarkerCluster(name="Listings", control=False)
    map.add_child(listings_group)

    room_type = {}
    for r_type in data["room_type"].unique():
        room_type[r_type] = plugins.FeatureGroupSubGroup(listings_group, name=r_type)

    for idx, row in data.iterrows():
        popup_html = f"""
        <div style='font-family: Helvetica, Arial, sans-serif;'>
            <h4 style='margin-bottom: 10px; color: #333;'>{row["name"]}</h4>
            <div style='font-size: 14px; color: #888; margin-bottom: 10px;'>
                <p style='margin: 2px 0;'><b>Price:</b> ${row["price"]}</p>
                <p style='margin: 2px 0;'><b>Neighbourhood:</b> {row["neighbourhood_cleansed"]}</p>
                <p style='margin: 2px 0;'><b>Room type:</b> {row["room_type"]}</p>
                <p style='margin: 2px 0;'><b>Rating:</b> {row["review_scores_rating"]}</p>
                <p style='margin: 2px 0;'><b>Minimum nights:</b> {row["minimum_nights"]}</p>
            </div>
            <a href="{row['listing_url']}" target="_blank" style='color: #007BFF; text-decoration: none; display: inline-block; margin-bottom: 10px;'>View on Airbnb</a>
            <div style='width: 80%; height: 200px; overflow: hidden; border-radius: 10px; box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1); display: flex; justify-content: center'>
                <img src="{row['picture_url']}" alt='Listing image' style='height: 100%; width: 100%; object-fit: cover; border-radius: 10px;'>
            </div>
        </div>
        """  # noqa: E501

        popup = folium.Popup(
            folium.IFrame(html=popup_html, width=400, height=400), max_width=400
        )

        marker = folium.CircleMarker(
            location=[row["latitude"], row["longitude"]],
            popup=popup,
            radius=5,
            fill=True,
            fill_opacity=1,
            color=price_scale(row["price"]),
        )

        marker.add_to(room_type[row["room_type"]])

    for group in room_type.values():
        map.add_child(group)

    map.add_child(
        plugins.MiniMap(
            tile_layer="cartodbpositron", toggle_display=True, minimized=True
        )
    )
    map.add_child(folium.LayerControl(collapsed=False))
    map.add_child(plugins.Fullscreen())

    return map._repr_html_()
