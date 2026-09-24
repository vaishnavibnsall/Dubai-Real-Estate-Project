import os

import pandas as pd
import psycopg2
import streamlit as st
from dotenv import load_dotenv


# Load environment variables
load_dotenv()


# Page configuration
st.set_page_config(
    page_title="Dubai Real Estate Dashboard",
    page_icon="🏙️",
    layout="wide"
)


# Database connection
@st.cache_resource
def get_connection():
    return psycopg2.connect(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        database=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD")
    )


# Load property data
@st.cache_data
def load_data():
    conn = get_connection()

    query = """
        SELECT
            f.price,
            f.bedroom,
            f.bathroom,
            f.area_sqft,
            f.purpose,
            f.handover,
            p.property_type,
            p.furnishing,
            p.completion_status,
            l.address,
            pr.project_name
        FROM fact_property f
        JOIN dim_property p
            ON f.property_id = p.property_id
        JOIN dim_location l
            ON f.location_id = l.location_id
        JOIN dim_project pr
            ON f.project_id = pr.project_id;
    """

    df = pd.read_sql(query, conn)
    conn.close()

    return df


# Load data
df = load_data()


# Title
st.title("🏙️ Dubai Real Estate Market Dashboard")
st.caption("Analysis of 3,438 Dubai residential property listings")


# KPI cards
col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Total Properties",
    f"{len(df):,}"
)

col2.metric(
    "Average Price",
    f"AED {df['price'].mean():,.0f}"
)

col3.metric(
    "Average Area",
    f"{df['area_sqft'].mean():,.0f} sqft"
)

col4.metric(
    "Projects",
    f"{df['project_name'].nunique():,}"
)


st.divider()


# Property type analysis
st.subheader("Property Type Analysis")

property_analysis = (
    df.groupby("property_type")
    .agg(
        property_count=("price", "count"),
        average_price=("price", "mean")
    )
    .sort_values("property_count", ascending=False)
)

st.bar_chart(
    property_analysis["property_count"]
)


# Furnishing analysis
st.subheader("Furnished vs Unfurnished")

furnishing_analysis = (
    df.groupby("furnishing")
    .agg(
        property_count=("price", "count"),
        average_price=("price", "mean")
    )
)

st.dataframe(
    furnishing_analysis.style.format({
        "property_count": "{:,.0f}",
        "average_price": "AED {:,.0f}"
    }),
    use_container_width=True
)


# Completion status
st.subheader("Ready vs Off-Plan")

completion_analysis = (
    df.groupby("completion_status")
    .agg(
        property_count=("price", "count"),
        average_price=("price", "mean")
    )
)

st.dataframe(
    completion_analysis.style.format({
        "property_count": "{:,.0f}",
        "average_price": "AED {:,.0f}"
    }),
    use_container_width=True
)


# Top locations
st.subheader("Top 10 Locations")

top_locations = (
    df.groupby("address")
    .agg(
        property_count=("price", "count"),
        average_price=("price", "mean")
    )
    .sort_values("property_count", ascending=False)
    .head(10)
)

st.dataframe(
    top_locations.style.format({
        "property_count": "{:,.0f}",
        "average_price": "AED {:,.0f}"
    }),
    use_container_width=True
)