import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import plotly.figure_factory as ff
from plotly.subplots import make_subplots
import seaborn as sns
import folium
from folium import plugins, branca

sns.set_style("whitegrid")
sns.set_context("talk")

tickprefixes_city = {
    "Boston": "US$",
    "Hongkong": "HK$",
    "Montreal": "CA$",
    "Munich": "€",
    "Vancouver": "CA$",
}


@st.cache_data(persist=True)
def price_distribution(data: pd.DataFrame, city: str):
    fig = ff.create_distplot(
        [data["price"]],
        group_labels=["Price"],
        colors=["red"],
        bin_size=25,
        show_rug=False,
    )

    fig.update_layout(
        title=f"Price distribution in {city.capitalize()}",
        xaxis_title="Price",
        yaxis_title="Density",
        showlegend=False,
    )

    return fig


@st.cache_data(persist=True)
def price_by_neighbourhood(data: pd.DataFrame, city: str):
    num_listings_by_neighborhood = (
        data["neighbourhood_cleansed"]
        .value_counts()
        .to_frame()
        .reset_index()
        .rename(columns={"index": "neighbourhood", "neighbourhood_cleansed": "count"})
    )

    # -------------------------------------------------------------------------
    colors = px.colors.qualitative.Set1 * (
        len(num_listings_by_neighborhood) // len(px.colors.qualitative.Set1) + 1
    )

    fig_0 = go.Figure(
        data=[
            go.Bar(
                x=num_listings_by_neighborhood["neighbourhood"],
                y=num_listings_by_neighborhood["count"],
                marker_color=colors[: len(num_listings_by_neighborhood)],
                hovertemplate="Number of listings: %{y}<extra></extra>",
            )
        ]
    )

    fig_0.update_layout(
        title=f"Number of listings by neighbourhood in {city.capitalize()}",
        xaxis_title="Neighbourhood",
        yaxis_title="Number of listings",
        template="plotly_white",
        height=600,
        margin=dict(l=100, r=100, b=200, t=50),
    )

    # -------------------------------------------------------------------------
    # Then, we see the price of listings in the top 10 neighbourhoods
    top_neighborhoods = num_listings_by_neighborhood.iloc[:10]["neighbourhood"].values
    data_top_neighborhoods = data[
        data["neighbourhood_cleansed"].isin(top_neighborhoods)
    ]

    # Create a box plot for each of the top 10 neighborhoods
    fig_1 = go.Figure()

    for neighborhood in top_neighborhoods:
        neighborhood_data = data_top_neighborhoods[
            data_top_neighborhoods["neighbourhood_cleansed"] == neighborhood
        ]
        fig_1.add_trace(
            go.Box(
                y=neighborhood_data["price"],
                name=neighborhood,
                marker=dict(
                    color="rgb(8,81,156)",
                ),
            )
        )

    # Update layout for a cleaner presentation
    fig_1.update_layout(
        title=f"Distribution of price in {city.capitalize()} by neighbourhood (top 10)",
        yaxis_title="Price",
        xaxis_title="Neighbourhood",
        showlegend=False,
        template="plotly_white",
        height=600,
        margin=dict(l=100, r=100, b=200, t=50),
    )

    fig_1.update_yaxes(
        tickprefix=tickprefixes_city[city], showgrid=True, gridcolor="rgb(233,233,233)"
    )

    # -------------------------------------------------------------------------
    # Calculate the average price for the top 10 neighborhoods
    avg_price_by_neighborhood = (
        (
            data[
                data["neighbourhood_cleansed"].isin(
                    num_listings_by_neighborhood.iloc[:10]["neighbourhood"].values
                )
            ]
            .groupby("neighbourhood_cleansed")["price"]
            .agg(["mean", "count"])
        )
        .reindex(index=num_listings_by_neighborhood.iloc[:10]["neighbourhood"].values)
        .reset_index()
    )

    # Create a bar plot for the average price by neighbourhood
    fig_2 = go.Figure()

    fig_2.add_trace(
        go.Bar(
            x=avg_price_by_neighborhood["neighbourhood_cleansed"],
            y=avg_price_by_neighborhood["mean"],
            marker=dict(
                color="rgba(255, 153, 51, 0.6)",
                line=dict(color="rgba(255, 153, 51, 1.0)", width=3),
            ),
            hovertemplate="$%{y:.2f}<extra></extra>",
        )
    )

    # Customize layout
    fig_2.update_layout(
        title=f"Average price of listings in {city.capitalize()} by neighbourhood (top 10)",
        xaxis_title="Neighbourhood",
        yaxis_title="Average price",
        template="plotly_white",
        height=600,
        margin=dict(l=100, r=100, b=200, t=50),
    )

    # Format x-axis
    fig_2.update_yaxes(
        tickprefix=tickprefixes_city[city],
        showgrid=True,
        gridcolor="rgb(233,233,233)",
    )

    return fig_0, fig_1, fig_2


@st.cache_data(persist=True)
def price_by_room_type(data: pd.DataFrame, city: str):
    # First, we check the `room_type` column
    num_listings_by_room_type = (
        data["room_type"]
        .value_counts()
        .to_frame()
        .reset_index()
        .rename(columns={"index": "room_type", "room_type": "count"})
    )

    # -------------------------------------------------------------------------
    fig_0 = go.Figure(
        data=[
            go.Bar(
                x=num_listings_by_room_type["room_type"],
                y=num_listings_by_room_type["count"],
                text=num_listings_by_room_type["count"],
                hovertemplate="Number of listings: %{y}<extra></extra>",
                marker_color=px.colors.qualitative.Set1,
            )
        ]
    )
    fig_0.update_layout(
        title=f"Number of Listings by Room Type in {city.capitalize()}",
        xaxis_title="Room Type",
        yaxis_title="Number of Listings",
        template="plotly_white",
        height=600,
        margin=dict(l=100, r=100, b=200, t=50),
    )

    fig_0.update_yaxes(
        showgrid=True, gridcolor="rgb(233,233,233)", zerolinecolor="rgb(233,233,233)"
    )

    # -------------------------------------------------------------------------
    # Distribution of price by room type using violin plot
    fig_1 = go.Figure()

    for room in num_listings_by_room_type.room_type.values:
        fig_1.add_trace(
            go.Violin(
                y=data[data["room_type"] == room]["price"],
                name=room,
                box_visible=True,
                meanline_visible=True,
            )
        )

    fig_1.update_layout(
        title=f"Distribution of Price by Room Type in {city.capitalize()}",
        yaxis_title="Price",
        xaxis_title="Room Type",
        template="plotly_white",
        height=600,
        margin=dict(l=100, r=100, b=200, t=50),
        showlegend=False,
    )

    fig_1.update_yaxes(
        tickprefix=tickprefixes_city[city], showgrid=True, gridcolor="rgb(233,233,233)"
    )

    return fig_0, fig_1


@st.cache_data(persist=True)
def price_by_amenities(data: pd.DataFrame, city: str):
    list_of_amenities = (
        data["amenities"]
        .str.split(", ")
        .explode()
        .value_counts()
        .to_frame()
        .reset_index()
    )

    top_20_amenities = list_of_amenities.head(20)

    # -------------------------------------------------------------------------
    colors = px.colors.qualitative.Set1 * (
        len(top_20_amenities) // len(px.colors.qualitative.Set1) + 1
    )

    fig_0 = go.Figure(
        data=[
            go.Bar(
                x=top_20_amenities["index"],
                y=top_20_amenities["amenities"],
                text=top_20_amenities["amenities"],
                hovertemplate="Number of listings: %{y}<extra></extra>",
                marker_color=colors,
            )
        ]
    )

    fig_0.update_layout(
        title=f"Number of Listings by Amenities in {city.capitalize()}",
        xaxis_title="Amenities",
        yaxis_title="Number of Listings",
        template="plotly_white",
        height=600,
        margin=dict(l=100, r=100, b=200, t=50),
    )

    fig_0.update_yaxes(
        showgrid=True, gridcolor="rgb(233,233,233)", zerolinecolor="rgb(233,233,233)"
    )

    # -------------------------------------------------------------------------
    # Distribution of price by amenities using violin plot

    def create_violin_for_amenity(data, amenity):
        fig = go.Figure()

        for present in ["Yes", "No"]:
            fig.add_trace(
                go.Violin(
                    x=data["amenity"][
                        (data["amenity"] == amenity)
                        & (data["amenity_present"] == present)
                    ],
                    y=data["price"][
                        (data["amenity"] == amenity)
                        & (data["amenity_present"] == present)
                    ],
                    name=present,
                    side="negative" if present == "Yes" else "positive",
                    line_color="green" if present == "Yes" else "red",
                    meanline_visible=True,
                    hoveron="violins",
                    points=False,
                )
            )

        fig.update_layout(
            violingap=0.0, violinmode="overlay", title=amenity, yaxis_title="Price"
        )

        return fig

    # Prepare data
    data_1 = (
        data.loc[:, ["price"] + top_20_amenities["index"].tolist()[:5]]
        .melt(id_vars="price", var_name="amenity", value_name="amenity_present")
        .replace({1: "Yes", 0: "No"})
    )

    data_2 = (
        data.loc[:, ["price"] + top_20_amenities["index"].tolist()[6:11]]
        .melt(id_vars="price", var_name="amenity", value_name="amenity_present")
        .replace({1: "Yes", 0: "No"})
    )

    # Create subplots: 2 rows and 5 columns for 10 amenities
    fig_1 = make_subplots(
        rows=2, cols=5, subplot_titles=top_20_amenities["index"].tolist()[:10]
    )

    # Generate plots for each amenity
    for i, amenity in enumerate(top_20_amenities["index"].tolist()[:5], 1):
        amenity_fig = create_violin_for_amenity(data_1, amenity)
        for trace in amenity_fig.data:
            fig_1.add_trace(trace, row=1, col=i)

    for i, amenity in enumerate(top_20_amenities["index"].tolist()[6:11], 1):
        amenity_fig = create_violin_for_amenity(data_2, amenity)
        for trace in amenity_fig.data:
            fig_1.add_trace(trace, row=2, col=i)

    # Update layout
    fig_1.update_layout(
        title_text=f"Distribution of price in {city.capitalize()} for top 10 amenities",
        template="plotly_white",
        showlegend=False,
        height=800,
    )

    fig_1.update_yaxes(
        tickprefix=tickprefixes_city[city], showgrid=True, gridcolor="rgb(233,233,233)"
    )

    return fig_0, fig_1


@st.cache_resource
def visualize_on_map(data: pd.DataFrame):
    map = folium.Map(
        location=[data["latitude"].mean(), data["longitude"].mean()],
        zoom_start=12,
        max_zoom=20,
        tiles=None,
    )

    folium.TileLayer("cartodbpositron", opacity=1, control=False).add_to(map)

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
