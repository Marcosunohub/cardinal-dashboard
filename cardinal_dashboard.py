import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Cardinal Sightings - May 2025", layout="wide")
st.title("🐦 Cardinal Observations Dashboard")

# Load data
@st.cache_data
def load_data():
    return pd.read_csv("cardinal_observations_may2025.csv")

df = load_data()

# Sidebar filters
st.sidebar.header("Filters")
selected_location = st.sidebar.multiselect(
    "Select Location(s)",
    options=sorted(df["location"].unique()),
    default=sorted(df["location"].unique())
)
selected_time = st.sidebar.multiselect(
    "Select Time of Day",
    options=sorted(df["time_of_day"].unique()),
    default=sorted(df["time_of_day"].unique())
)

# Apply filters
filtered_df = df[
    df["location"].isin(selected_location) &
    df["time_of_day"].isin(selected_time)
]

# Display filtered data
st.subheader("Filtered Observations")
st.dataframe(filtered_df, use_container_width=True)

# Plot: Daily count of cardinals
st.subheader("📈 Daily Cardinal Count")
daily_count = filtered_df.groupby("date")["count"].sum().reset_index()
fig1 = px.line(daily_count, x="date", y="count", title="Cardinal Count per Day")
st.plotly_chart(fig1, use_container_width=True)

# Plot: Count by location
st.subheader("📍 Cardinal Sightings by Location")
location_count = filtered_df.groupby("location")["count"].sum().reset_index()
fig2 = px.bar(location_count, x="location", y="count", color="location", title="Total Cardinals by Location")
st.plotly_chart(fig2, use_container_width=True)

# Plot: Count by time of day
st.subheader("🕒 Cardinal Sightings by Time of Day")
time_count = filtered_df.groupby("time_of_day")["count"].sum().reset_index()
fig3 = px.pie(time_count, values="count", names="time_of_day", title="Cardinals by Time of Day")
st.plotly_chart(fig3, use_container_width=True)
