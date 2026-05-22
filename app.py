# =========================================
# LIBRARIES
# =========================================

import streamlit as st
import pandas as pd
import random

# =========================================
# PAGE CONFIG
# =========================================

st.set_page_config(
    page_title="Foodie Hub",
    page_icon="🍕",
    layout="wide"
)

# =========================================
# CUSTOM CSS
# =========================================

st.markdown("""
<style>

.main {
    background-color: #f5f5f5;
}

/* LOGIN PAGE */

.login-container {
    background: linear-gradient(to right,#ff512f,#dd2476);
    padding: 60px;
    border-radius: 25px;
    text-align: center;
    color: white;
    margin-bottom: 30px;
}

.login-box {
    background-color: white;
    padding: 30px;
    border-radius: 20px;
    box-shadow: 0px 5px 20px rgba(0,0,0,0.15);
}

/* HERO */

.hero {
    background: linear-gradient(to right,#fc8019,#ff4b2b);
    padding: 40px;
    border-radius: 25px;
    text-align: center;
    color: white;
    margin-bottom: 30px;
}

/* RESTAURANT CARD */

.restaurant-card {
    background-color: white;
    padding: 20px;
    border-radius: 20px;
    margin-bottom: 20px;
    box-shadow: 0px 5px 15px rgba(0,0,0,0.1);
    transition: 0.3s;
}

.restaurant-card:hover {
    transform: scale(1.02);
}

/* METRIC CARD */

.metric-card {
    background: linear-gradient(to right,#ff512f,#dd2476);
    padding: 20px;
    border-radius: 20px;
    text-align: center;
    color: white;
}

/* BUTTON */

.stButton button {
    background-color: #ff4b2b;
    color: white;
    border-radius: 12px;
    border: none;
    padding: 10px 20px;
    font-weight: bold;
}

/* BOOKING BOX */

.booking-box {
    background-color: #fff3e0;
    padding: 25px;
    border-radius: 20px;
    margin-top: 20px;
}

</style>
""", unsafe_allow_html=True)

# =========================================
# SESSION STATE
# =========================================

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# =========================================
# LOGIN PAGE
# =========================================

if not st.session_state.logged_in:

    st.markdown("""
    <div class="login-container">

    <h1>🍕 Foodie Hub</h1>

    <h3>Find & Book Amazing Restaurants Nearby</h3>

    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1,2,1])

    with col2:

        st.markdown("""
        <div class="login-box">

        <h2 style="text-align:center;color:#ff4b2b;">
        Login To Continue
        </h2>

        </div>
        """, unsafe_allow_html=True)

        name = st.text_input("👤 Enter Your Name")

        phone = st.text_input("📱 Enter Phone Number")

        location = st.text_input("📍 Enter Current Location")

        if st.button("Enter Website"):

            if name and phone and location:

                st.session_state.logged_in = True
                st.session_state.name = name
                st.session_state.location = location

                st.rerun()

            else:
                st.error("Please fill all fields")

# =========================================
# MAIN WEBSITE
# =========================================

else:

    # =========================================
    # LOAD DATASET
    # =========================================

    df = pd.read_csv("restaurant dataset.csv")

    # =========================================
    # CLEAN DATA
    # =========================================

    df["Rating"] = pd.to_numeric(
        df["Rating"],
        errors="coerce"
    )

    df["Average_Price"] = pd.to_numeric(
        df["Average_Price"],
        errors="coerce"
    )

    df = df.dropna(
        subset=["Rating","Average_Price"]
    )

    # =========================================
    # HERO SECTION
    # =========================================

    st.markdown(f"""
    <div class="hero">

    <h1>🍽️ Welcome {st.session_state.name}</h1>

    <h3>📍 {st.session_state.location}</h3>

    </div>
    """, unsafe_allow_html=True)

    st.image(
        "https://images.unsplash.com/photo-1504674900247-0877df9cc836",
        use_container_width=True
    )

    # =========================================
    # FOOD TYPE + BUDGET
    # =========================================

    st.markdown("## 🍔 Find Best Restaurants")

    col1, col2 = st.columns(2)

    with col1:

        food_type = st.selectbox(
            "🍜 Select Food Type",
            sorted(df["Cuisine"].unique())
        )

    with col2:

        budget = st.slider(
            "💰 Select Your Budget",
            int(df["Average_Price"].min()),
            int(df["Average_Price"].max()),
            500
        )

    # =========================================
    # PREDICT RESTAURANTS
    # =========================================

    filtered = df[
        (df["Cuisine"] == food_type) &
        (df["Average_Price"] <= budget)
    ]

    filtered = filtered.sort_values(
        by=["Rating"],
        ascending=False
    )

    # TOP 4 RESTAURANTS
    filtered = filtered.head(4)

    # =========================================
    # DASHBOARD
    # =========================================

    st.markdown("## 📊 Dashboard")

    c1, c2, c3 = st.columns(3)

    with c1:

        st.markdown(f"""
        <div class="metric-card">

        <h2>{len(df)}</h2>

        <p>Total Restaurants</p>

        </div>
        """, unsafe_allow_html=True)

    with c2:

        st.markdown(f"""
        <div class="metric-card">

        <h2>{round(df['Rating'].mean(),2)}</h2>

        <p>Average Rating</p>

        </div>
        """, unsafe_allow_html=True)

    with c3:

        st.markdown(f"""
        <div class="metric-card">

        <h2>{len(filtered)}</h2>

        <p>Recommended Restaurants</p>

        </div>
        """, unsafe_allow_html=True)

    # =========================================
    # RESTAURANT RECOMMENDATIONS
    # =========================================

    st.markdown("## 🍕 Recommended Restaurants")

    if not filtered.empty:

        cols = st.columns(2)

        for idx, row in filtered.iterrows():

            with cols[idx % 2]:

                st.markdown(f"""
                <div class="restaurant-card">

                <h2>{row['Restaurant_Name']}</h2>

                <p>🍜 Cuisine:
                {row['Cuisine']}</p>

                <p>⭐ Rating:
                {row['Rating']}</p>

                <p>💰 Budget:
                ₹{row['Average_Price']}</p>

                <p>📍 Area:
                {row['Area']}</p>

                <p>🚚 Delivery:
                {row['Delivery_Available']}</p>

                </div>
                """, unsafe_allow_html=True)

                # SELECT RESTAURANT BUTTON

                if st.button(
                    f"Book {row['Restaurant_Name']}",
                    key=idx
                ):

                    st.session_state.selected_restaurant = row[
                        "Restaurant_Name"
                    ]

        # =========================================
        # BOOKING SECTION
        # =========================================

        if "selected_restaurant" in st.session_state:

            st.markdown("""
            <div class="booking-box">

            <h2>🪑 Booking Section</h2>

            </div>
            """, unsafe_allow_html=True)

            st.success(f"""
            Selected Restaurant:
            {st.session_state.selected_restaurant}
            """)

            people = st.number_input(
                "👥 Number of People",
                1,
                20,
                2
            )

            booking_date = st.date_input(
                "📅 Booking Date"
            )

            booking_time = st.time_input(
                "⏰ Booking Time"
            )

            if st.button("✅ Confirm Booking"):

                booking_id = random.randint(
                    10000,
                    99999
                )

                st.success(f"""
                🎉 Booking Confirmed!

                Booking ID:
                {booking_id}

                Restaurant:
                {st.session_state.selected_restaurant}

                Name:
                {st.session_state.name}

                Date:
                {booking_date}

                Time:
                {booking_time}
                """)

                st.balloons()

    else:

        st.warning(
            "No restaurants found under your budget"
        )