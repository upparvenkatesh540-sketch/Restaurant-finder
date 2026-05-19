import streamlit as st
import pandas as pd

# Page settings
st.set_page_config(
    page_title="Smart Restaurant Finder",
    page_icon="🍽️",
    layout="wide"
)

# Background style
st.markdown("""
<style>
.main {
    background-color: #f8f9fa;
}
h1 {
    color: #ff4b4b;
    text-align: center;
}
.card {
    padding: 20px;
    border-radius: 15px;
    background-color: white;
    box-shadow: 2px 2px 10px rgba(0,0,0,0.1);
    margin-bottom: 20px;
}
</style>
""", unsafe_allow_html=True)

# Main title
st.title("🍴 Smart Restaurant Recommendation System")

# Hero banner
st.image(
    "https://images.unsplash.com/photo-1517248135467-4c7edcad34c4",
    use_container_width=True
)

st.markdown("## Discover Amazing Restaurants Near You")

# Feature section
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.image(
        "https://cdn-icons-png.flaticon.com/512/3075/3075977.png",
        width=90
    )
    st.markdown("### Top Rated")
    st.write("Best rated restaurants")

with col2:
    st.image(
        "https://cdn-icons-png.flaticon.com/512/1046/1046784.png",
        width=90
    )
    st.markdown("### Budget Friendly")
    st.write("Affordable food places")

with col3:
    st.image(
        "https://cdn-icons-png.flaticon.com/512/2921/2921822.png",
        width=90
    )
    st.markdown("### Fast Delivery")
    st.write("Quick food delivery")

with col4:
    st.image(
        "https://cdn-icons-png.flaticon.com/512/706/706164.png",
        width=90
    )
    st.markdown("### Nearby")
    st.write("Restaurants near your area")

# Load dataset
df = pd.read_csv("restaurant dataset.CSV")

# Convert numeric columns
df["Rating"] = pd.to_numeric(df["Rating"], errors="coerce")
df["Average_Price"] = pd.to_numeric(df["Average_Price"], errors="coerce")

# Remove missing values
df = df.dropna(subset=["Rating", "Average_Price"])

# Sidebar filters
st.sidebar.image(
    "https://cdn-icons-png.flaticon.com/512/706/706195.png",
    width=120
)

st.sidebar.title("🔍 Filter Restaurants")

# Cuisine filter
cuisine = st.sidebar.selectbox(
    "Select Cuisine",
    sorted(df["Cuisine"].unique())
)

# Rating filter
min_rating = st.sidebar.slider(
    "Minimum Rating",
    0.0,
    5.0,
    4.0
)

# Budget filter
max_budget = st.sidebar.slider(
    "Maximum Budget",
    int(df["Average_Price"].min()),
    int(df["Average_Price"].max()),
    500
)

# Delivery option
delivery = st.sidebar.selectbox(
    "Delivery Available",
    ["All", "Yes", "No"]
)

# Filter dataset
filtered = df[
    (df["Cuisine"] == cuisine) &
    (df["Rating"] >= min_rating) &
    (df["Average_Price"] <= max_budget)
]

if delivery != "All":
    filtered = filtered[
        filtered["Delivery_Available"] == delivery
    ]

# Top metrics
st.markdown("## 📊 Platform Statistics")

m1, m2, m3 = st.columns(3)

with m1:
    st.metric("Total Restaurants", len(df))

with m2:
    st.metric("Average Rating", round(df["Rating"].mean(), 2))

with m3:
    st.metric("Highest Budget", int(df["Average_Price"].max()))

# Restaurant recommendations
st.markdown("## 🍽️ Recommended Restaurants")

if not filtered.empty:

    for index, row in filtered.iterrows():

        st.markdown(f"""
        <div class="card">
            <h3>{row['Restaurant_Name']}</h3>
            <p>🍜 Cuisine: {row['Cuisine']}</p>
            <p>⭐ Rating: {row['Rating']}</p>
            <p>💰 Average Price: ₹{row['Average_Price']}</p>
            <p>📍 Area: {row['Area']}</p>
            <p>🚚 Delivery: {row['Delivery_Available']}</p>
        </div>
        """, unsafe_allow_html=True)

else:
    st.warning("No restaurants found for selected filters.")

# Footer image
st.image(
    "https://images.unsplash.com/photo-1555396273-367ea4eb4db5",
    use_container_width=True
)

st.markdown("### 🍕 Enjoy Delicious Food with Smart Recommendations")