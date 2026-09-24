import os

import pandas as pd
import plotly.express as px
import psycopg2
import streamlit as st
from dotenv import load_dotenv


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="Dubai Real Estate Analytics",
    page_icon="🏙️",
    layout="wide",
    initial_sidebar_state="expanded"
)


# =========================================================
# LOAD ENVIRONMENT VARIABLES
# =========================================================

load_dotenv()


# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown("""
<style>

    /* Main background */
    .stApp {
        background-color: #0e1117;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background-color: #151922;
    }

    /* Main title */
    .main-title {
        font-size: 42px;
        font-weight: 700;
        margin-bottom: 5px;
        color: #f5f5f5;
    }

    .subtitle {
        font-size: 16px;
        color: #9aa4b2;
        margin-bottom: 30px;
    }

    /* KPI cards */
    .kpi-card {
        background-color: #171c26;
        border: 1px solid #252c38;
        border-radius: 14px;
        padding: 22px;
        height: 125px;
    }

    .kpi-title {
        color: #8d98a8;
        font-size: 14px;
        margin-bottom: 10px;
    }

    .kpi-value {
        color: #ffffff;
        font-size: 27px;
        font-weight: 700;
    }

    /* Section titles */
    .section-title {
        font-size: 23px;
        font-weight: 600;
        color: #f5f5f5;
        margin-top: 25px;
        margin-bottom: 15px;
    }

    /* Hide Streamlit menu/footer */
    #MainMenu {
        visibility: hidden;
    }

    footer {
        visibility: hidden;
    }

</style>
""", unsafe_allow_html=True)


# =========================================================
# DATABASE CONNECTION
# =========================================================

@st.cache_resource
def get_connection():

    # Streamlit Cloud
    try:
        db_host = st.secrets["DB_HOST"]
        db_port = st.secrets["DB_PORT"]
        db_name = st.secrets["DB_NAME"]
        db_user = st.secrets["DB_USER"]
        db_password = st.secrets["DB_PASSWORD"]

    # Local computer
    except Exception:
        db_host = os.getenv("DB_HOST")
        db_port = os.getenv("DB_PORT")
        db_name = os.getenv("DB_NAME")
        db_user = os.getenv("DB_USER")
        db_password = os.getenv("DB_PASSWORD")

    return psycopg2.connect(
        host=db_host,
        port=db_port,
        database=db_name,
        user=db_user,
        password=db_password
    )


# =========================================================
# LOAD DATA
# =========================================================

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


df = load_data()


# =========================================================
# SIDEBAR FILTERS
# =========================================================

st.sidebar.title("Filters")

st.sidebar.markdown("Customize the market analysis below.")

property_types = st.sidebar.multiselect(
    "Property Type",
    options=sorted(df["property_type"].unique()),
    default=sorted(df["property_type"].unique())
)

furnishing_options = st.sidebar.multiselect(
    "Furnishing",
    options=sorted(df["furnishing"].unique()),
    default=sorted(df["furnishing"].unique())
)

completion_options = st.sidebar.multiselect(
    "Completion Status",
    options=sorted(df["completion_status"].unique()),
    default=sorted(df["completion_status"].unique())
)


# =========================================================
# APPLY FILTERS
# =========================================================

filtered_df = df[
    df["property_type"].isin(property_types)
    & df["furnishing"].isin(furnishing_options)
    & df["completion_status"].isin(completion_options)
]


# =========================================================
# HEADER
# =========================================================

st.markdown(
    '<div class="main-title">Dubai Real Estate Analytics</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'Interactive analysis of Dubai residential property listings'
    '</div>',
    unsafe_allow_html=True
)


# =========================================================
# KPI SECTION
# =========================================================

total_properties = len(filtered_df)

average_price = (
    filtered_df["price"].mean()
    if len(filtered_df) > 0
    else 0
)

average_area = (
    filtered_df["area_sqft"].mean()
    if len(filtered_df) > 0
    else 0
)

projects = filtered_df["project_name"].nunique()


col1, col2, col3, col4 = st.columns(4)


with col1:
    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-title">TOTAL PROPERTIES</div>
            <div class="kpi-value">{total_properties:,}</div>
        </div>
        """,
        unsafe_allow_html=True
    )


with col2:
    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-title">AVERAGE PRICE</div>
            <div class="kpi-value">AED {average_price:,.0f}</div>
        </div>
        """,
        unsafe_allow_html=True
    )


with col3:
    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-title">AVERAGE AREA</div>
            <div class="kpi-value">{average_area:,.0f} sqft</div>
        </div>
        """,
        unsafe_allow_html=True
    )


with col4:
    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-title">PROJECTS</div>
            <div class="kpi-value">{projects:,}</div>
        </div>
        """,
        unsafe_allow_html=True
    )


# =========================================================
# PROPERTY TYPE
# =========================================================

st.markdown(
    '<div class="section-title">Property Market Overview</div>',
    unsafe_allow_html=True
)

property_analysis = (
    filtered_df
    .groupby("property_type")
    .agg(
        property_count=("price", "count"),
        average_price=("price", "mean")
    )
    .reset_index()
    .sort_values("property_count", ascending=False)
)


col1, col2 = st.columns(2)


with col1:

    fig = px.bar(
        property_analysis,
        x="property_type",
        y="property_count",
        title="Properties by Type",
        labels={
            "property_type": "",
            "property_count": "Properties"
        }
    )

    fig.update_layout(
        template="plotly_dark",
        plot_bgcolor="#171c26",
        paper_bgcolor="#171c26",
        margin=dict(l=20, r=20, t=50, b=20)
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


with col2:

    fig = px.bar(
        property_analysis,
        x="property_type",
        y="average_price",
        title="Average Price by Property Type",
        labels={
            "property_type": "",
            "average_price": "Average Price (AED)"
        }
    )

    fig.update_layout(
        template="plotly_dark",
        plot_bgcolor="#171c26",
        paper_bgcolor="#171c26",
        margin=dict(l=20, r=20, t=50, b=20)
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


# =========================================================
# FURNISHING + COMPLETION
# =========================================================

st.markdown(
    '<div class="section-title">Property Characteristics</div>',
    unsafe_allow_html=True
)

col1, col2 = st.columns(2)


with col1:

    furnishing_analysis = (
        filtered_df["furnishing"]
        .value_counts()
        .reset_index()
    )

    furnishing_analysis.columns = [
        "furnishing",
        "count"
    ]

    fig = px.pie(
        furnishing_analysis,
        names="furnishing",
        values="count",
        title="Furnished vs Unfurnished",
        hole=0.55
    )

    fig.update_layout(
        template="plotly_dark",
        plot_bgcolor="#171c26",
        paper_bgcolor="#171c26"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


with col2:

    completion_analysis = (
        filtered_df["completion_status"]
        .value_counts()
        .reset_index()
    )

    completion_analysis.columns = [
        "completion_status",
        "count"
    ]

    fig = px.pie(
        completion_analysis,
        names="completion_status",
        values="count",
        title="Ready vs Off-Plan",
        hole=0.55
    )

    fig.update_layout(
        template="plotly_dark",
        plot_bgcolor="#171c26",
        paper_bgcolor="#171c26"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


# =========================================================
# PRICE PER SQFT
# =========================================================

st.markdown(
    '<div class="section-title">Price Efficiency</div>',
    unsafe_allow_html=True
)

price_sqft = (
    filtered_df
    .assign(
        price_per_sqft=
        filtered_df["price"] /
        filtered_df["area_sqft"].replace(0, pd.NA)
    )
    .groupby("property_type")
    .agg(
        average_price_per_sqft=("price_per_sqft", "mean")
    )
    .reset_index()
    .sort_values(
        "average_price_per_sqft",
        ascending=False
    )
)


fig = px.bar(
    price_sqft,
    x="property_type",
    y="average_price_per_sqft",
    title="Average Price per Square Foot",
    labels={
        "property_type": "",
        "average_price_per_sqft": "AED / sqft"
    }
)

fig.update_layout(
    template="plotly_dark",
    plot_bgcolor="#171c26",
    paper_bgcolor="#171c26",
    margin=dict(l=20, r=20, t=50, b=20)
)

st.plotly_chart(
    fig,
    use_container_width=True
)


# =========================================================
# TOP LOCATIONS
# =========================================================

st.markdown(
    '<div class="section-title">Top Locations</div>',
    unsafe_allow_html=True
)

top_locations = (
    filtered_df
    .groupby("address")
    .agg(
        property_count=("price", "count"),
        average_price=("price", "mean")
    )
    .reset_index()
    .sort_values(
        "property_count",
        ascending=False
    )
    .head(10)
)


fig = px.bar(
    top_locations,
    x="property_count",
    y="address",
    orientation="h",
    title="Top 10 Locations by Number of Listings",
    labels={
        "address": "",
        "property_count": "Properties"
    }
)

fig.update_layout(
    template="plotly_dark",
    plot_bgcolor="#171c26",
    paper_bgcolor="#171c26",
    margin=dict(l=20, r=20, t=50, b=20)
)

st.plotly_chart(
    fig,
    use_container_width=True
)


# =========================================================
# FOOTER
# =========================================================

st.divider()

st.caption(
    "Dubai Real Estate Analytics • "
    "Built with Python, PostgreSQL, Supabase, SQL and Streamlit"
)