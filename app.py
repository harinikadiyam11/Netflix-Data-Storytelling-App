import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Netflix Data Storytelling App", layout="wide")

st.title("🎬 Netflix Data Storytelling App")

# Load dataset
df = pd.read_csv("netflix_titles.csv")

# Dataset Introduction
st.header("1. Dataset Introduction")
st.write("""
This project presents a data story about Netflix movies and TV shows.
It analyzes content type, ratings, countries, release years, and genres.
""")

st.write("Rows and Columns:", df.shape)
st.markdown(df.head().to_html(), unsafe_allow_html=True)

st.divider()

# Data Cleaning
st.header("2. Data Cleaning")

st.write("Missing Values Before Cleaning:")
st.markdown(df.isnull().sum().to_frame("Missing Values").to_html(), unsafe_allow_html=True)

df["director"] = df["director"].fillna("Unknown")
df["cast"] = df["cast"].fillna("Unknown")
df["country"] = df["country"].fillna("Unknown")
df["date_added"] = df["date_added"].fillna("Unknown")
df["rating"] = df["rating"].fillna("Not Rated")

df.drop_duplicates(inplace=True)

st.success("Missing values handled and duplicate records removed successfully ✅")

st.divider()

# Sidebar Filters
st.sidebar.header("Interactive Filters")

selected_type = st.sidebar.multiselect(
    "Select Content Type",
    options=df["type"].unique(),
    default=df["type"].unique()
)

selected_rating = st.sidebar.multiselect(
    "Select Rating",
    options=df["rating"].unique(),
    default=df["rating"].unique()
)

filtered_df = df[
    (df["type"].isin(selected_type)) &
    (df["rating"].isin(selected_rating))
]

# EDA
st.header("3. Exploratory Data Analysis")

col1, col2, col3 = st.columns(3)

col1.metric("Total Titles", len(filtered_df))
col2.metric("Movies", len(filtered_df[filtered_df["type"] == "Movie"]))
col3.metric("TV Shows", len(filtered_df[filtered_df["type"] == "TV Show"]))

st.divider()

# Visualizations
st.header("4. Visualizations")

st.subheader("1. Movies vs TV Shows")
type_count = filtered_df["type"].value_counts().reset_index()
type_count.columns = ["Type", "Count"]

fig1 = px.pie(
    type_count,
    names="Type",
    values="Count",
    title="Movies vs TV Shows"
)
st.plotly_chart(fig1, use_container_width=True)

st.subheader("2. Top 10 Countries Producing Netflix Content")
country_count = filtered_df["country"].value_counts().head(10).reset_index()
country_count.columns = ["Country", "Count"]

fig2 = px.bar(
    country_count,
    x="Country",
    y="Count",
    title="Top 10 Countries by Netflix Content"
)
st.plotly_chart(fig2, use_container_width=True)

st.subheader("3. Netflix Content Release Trend")
year_count = filtered_df["release_year"].value_counts().sort_index().reset_index()
year_count.columns = ["Release Year", "Count"]

fig3 = px.line(
    year_count,
    x="Release Year",
    y="Count",
    title="Netflix Content Release Trend"
)
st.plotly_chart(fig3, use_container_width=True)

st.subheader("4. Rating Distribution")
rating_count = filtered_df["rating"].value_counts().reset_index()
rating_count.columns = ["Rating", "Count"]

fig4 = px.bar(
    rating_count,
    x="Rating",
    y="Count",
    title="Rating Distribution"
)
st.plotly_chart(fig4, use_container_width=True)

st.subheader("5. Top 10 Genres on Netflix")
genres = filtered_df["listed_in"].str.split(", ").explode()
genre_count = genres.value_counts().head(10).reset_index()
genre_count.columns = ["Genre", "Count"]

fig5 = px.bar(
    genre_count,
    x="Genre",
    y="Count",
    title="Top 10 Netflix Genres"
)
st.plotly_chart(fig5, use_container_width=True)

st.divider()

# Insights
st.header("5. Insights and Findings")

st.write("""
- Netflix has more Movies than TV Shows.
- The United States contributes the highest number of Netflix titles.
- Content production increased strongly in recent years.
- TV-MA and TV-14 are common ratings on Netflix.
- International Movies, Dramas, and Comedies are popular content genres.
""")

st.divider()

# Conclusion
st.header("6. Final Conclusion / Recommendations")

st.write("""
Netflix should continue investing in international content and popular genres like dramas,
comedies, and documentaries. The platform can also focus more on TV Shows to improve
long-term viewer engagement.
""")

st.success("Netflix Data Storytelling App Completed Successfully ✅")