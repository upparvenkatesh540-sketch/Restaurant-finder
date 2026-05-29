# =========================================================
# FOODIE HUB AI - COMPLETE FINAL CODE
# =========================================================

import streamlit as st
import pandas as pd
import plotly.express as px
import random
from datetime import datetime

# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="Foodie Hub AI",
    page_icon="🍕",
    layout="wide"
)

# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown("""
<style>

.main {
    background-color: #f5f5f5;
}

/* NAVBAR */

.navbar {
    background: linear-gradient(to right,#fc8019,#ff4b2b);
    padding: 20px;
    border-radius: 15px;
    text-align: center;
    color: white;
    margin-bottom: 20px;
}

/* HERO */

.hero {
    background: linear-gradient(to right,#ff512f,#dd2476);
    padding: 40px;
    border-radius: 25px;
    text-align: center;
    color: white;
    margin-bottom: 30px;
}

/* LOGIN */

.login-container {
    background: linear-gradient(to right,#ff512f,#dd2476);
    padding: 60px;
    border-radius: 25px;
    text-align: center;
    color: white;
}

.login-box {
    background-color: white;
    padding: 30px;
    border-radius: 20px;
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

/* CHAT BOX */

.chat-box {
    background-color: white;
    padding: 20px;
    border-radius: 20px;
    margin-bottom: 20px;
}

/* BOOKING */

.booking-box {
    background-color: #fff3e0;
    padding: 25px;
    border-radius: 20px;
    margin-top: 20px;
}

/* BUTTON */

.stButton button {
    background-color: #ff4b2b;
    color: white;
    border-radius: 10px;
    border: none;
    padding: 10px 18px;
    font-weight: bold;
}

/* FOOTER */

.footer {
    margin-top: 40px;
    text-align: center;
    color: gray;
}

</style>
""", unsafe_allow_html=True)

# =========================================================
# SESSION STATE
# =========================================================

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "favorites" not in st.session_state:
    st.session_state.favorites = []

# =========================================================
# LOGIN PAGE
# =========================================================

if not st.session_state.logged_in:

    st.markdown("""
    <div class="login-container">

    <h1>🍕 Foodie Hub AI</h1>

    <h3>Smart Restaurant Recommendation System</h3>

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
        location = st.text_input("📍 Enter Location")

        if st.button("Enter Website"):

            if name and phone and location:

                st.session_state.logged_in = True
                st.session_state.name = name
                st.session_state.location = location

                st.rerun()

            else:
                st.error("Please fill all fields")

# =========================================================
# MAIN WEBSITE
# =========================================================

else:

    # =====================================================
    # LOAD DATASET
    # =====================================================

    df = pd.read_csv("restaurant dataset.csv")

    # =====================================================
    # CLEAN DATA
    # =====================================================

    df["Rating"] = pd.to_numeric(
        df["Rating"],
        errors="coerce"
    )

    df["Average_Price"] = pd.to_numeric(
        df["Average_Price"],
        errors="coerce"
    )

    df = df.dropna(
        subset=["Rating", "Average_Price"]
    )

    # =====================================================
    # IMAGE COLUMN
    # =====================================================

    if "Image_URL" not in df.columns:

        sample_image = (
            "https://images.unsplash.com/photo-1504674900247-0877df9cc836"
        )

        df["Image_URL"] = sample_image

    # =====================================================
    # NAVBAR
    # =====================================================

    st.markdown("""
    <div class="navbar">

    <h1>🍔 FOODIE HUB AI</h1>

    </div>
    """, unsafe_allow_html=True)

    menu = st.radio(
        "Navigation",
        [
            "🏠 Home",
            "🍽 Restaurants",
            "📊 Dashboard",
            "🤖 AI Chatbot",
            "❤️ Favorites"
        ],
        horizontal=True
    )

    # =====================================================
    # HERO
    # =====================================================

    st.markdown(f"""
    <div class="hero">

    <h1>🍽 Welcome {st.session_state.name}</h1>

    <h3>📍 {st.session_state.location}</h3>

    </div>
    """, unsafe_allow_html=True)

    # =====================================================
    # HOME
    # =====================================================

    if menu == "🏠 Home":

        st.image(
            "https://images.unsplash.com/photo-1504674900247-0877df9cc836",
            use_container_width=True
        )

        st.title("🔥 Discover Amazing Restaurants")

        st.write("""
        Welcome to Foodie Hub AI 🍕

        Explore restaurants, analytics,
        booking system and AI chatbot.
        """)

        st.snow()

    # =====================================================
    # RESTAURANTS
    # =====================================================

    elif menu == "🍽 Restaurants":

        st.title("🍽 Find Best Restaurants")

        col1, col2, col3 = st.columns(3)

        with col1:

            food_type = st.selectbox(
                "🍜 Select Cuisine",
                sorted(df["Cuisine"].unique())
            )

        with col2:

            budget = st.slider(
                "💰 Select Budget",
                int(df["Average_Price"].min()),
                int(df["Average_Price"].max()),
                500
            )

        with col3:

            search = st.text_input(
                "🔍 Search Restaurant"
            )

        # FILTER

        filtered = df[
            (df["Cuisine"] == food_type) &
            (df["Average_Price"] <= budget)
        ]

        if search:

            filtered = filtered[
                filtered["Restaurant_Name"]
                .str.contains(search, case=False)
            ]

        filtered = filtered.sort_values(
            by="Rating",
            ascending=False
        )

        filtered = filtered.head(8)

        # DISPLAY

        if not filtered.empty:

            cols = st.columns(2)

            for idx, row in filtered.iterrows():

                with cols[idx % 2]:

                    st.image(
                        row["Image_URL"],
                        use_container_width=True
                    )

                    st.markdown(f"""
                    <div class="restaurant-card">

                    <h2>{row['Restaurant_Name']}</h2>

                    <p>🍜 Cuisine:
                    {row['Cuisine']}</p>

                    <p>⭐ Rating:
                    {row['Rating']}</p>

                    <p>💰 Price:
                    ₹{row['Average_Price']}</p>

                    <p>📍 Area:
                    {row['Area']}</p>

                    <p>🚚 Delivery:
                    {row['Delivery_Available']}</p>

                    </div>
                    """, unsafe_allow_html=True)

                    # FAVORITE

                    if st.button(
                        f"❤️ Favorite {row['Restaurant_Name']}",
                        key=f"fav{idx}"
                    ):

                        st.session_state.favorites.append(
                            row["Restaurant_Name"]
                        )

                        st.success("Added To Favorites")

                    # =================================================
                    # GOOGLE MAPS LOCATION
                    # =================================================

                    maps_query = (
                        f"{row['Area']} Bangalore"
                    )

                    maps_url = (
                        f"https://www.google.com/maps/search/"
                        f"{maps_query}"
                    )

                    st.markdown(
                        f"[📍 Open Restaurant Location]({maps_url})"
                    )

                    # =================================================
                    # BOOK BUTTON
                    # =================================================

                    if st.button(
                        f"🪑 Book {row['Restaurant_Name']}",
                        key=f"book{idx}"
                    ):

                        st.session_state.selected_restaurant = row[
                            "Restaurant_Name"
                        ]

            # =================================================
            # BOOKING SECTION
            # =================================================

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

                quantity = st.number_input(
                    "🍽 Food Quantity",
                    1,
                    10,
                    1
                )

                booking_date = st.date_input(
                    "📅 Booking Date"
                )

                booking_time = st.time_input(
                    "⏰ Booking Time"
                )

                payment = st.selectbox(
                    "💳 Payment Method",
                    ["UPI", "Card", "Cash"]
                )

                if st.button("✅ Confirm Booking"):

                    booking_id = random.randint(
                        10000,
                        99999
                    )

                    st.balloons()

                    receipt = f"""
BOOKING RECEIPT

Booking ID:
{booking_id}

Restaurant:
{st.session_state.selected_restaurant}

Customer:
{st.session_state.name}

Location:
{st.session_state.location}

People:
{people}

Food Quantity:
{quantity}

Payment Method:
{payment}

Booking Date:
{booking_date}

Booking Time:
{booking_time}

Generated:
{datetime.now()}
"""

                    st.success(receipt)

                    st.download_button(
                        "📥 Download Receipt",
                        receipt,
                        file_name="booking_receipt.txt"
                    )

        else:

            st.warning(
                "No restaurants found"
            )

    # =====================================================
    # DASHBOARD
    # =====================================================

    elif menu == "📊 Dashboard":

        st.title("📊 Restaurant Analytics")

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

            <h2>{len(df['Cuisine'].unique())}</h2>

            <p>Total Cuisines</p>

            </div>
            """, unsafe_allow_html=True)

        fig1 = px.histogram(
            df,
            x="Cuisine",
            color="Cuisine"
        )

        st.plotly_chart(
            fig1,
            use_container_width=True
        )

        fig2 = px.scatter(
            df,
            x="Average_Price",
            y="Rating",
            color="Cuisine",
            hover_name="Restaurant_Name"
        )

        st.plotly_chart(
            fig2,
            use_container_width=True
        )

    # =====================================================
    # AI CHATBOT
    # =====================================================

    elif menu == "🤖 AI Chatbot":

        st.title("🤖 Foodie AI Assistant")

        st.markdown("""
        <div class="chat-box">

        Ask AI anything about restaurants 🍕

        </div>
        """, unsafe_allow_html=True)

        user_query = st.text_input(
            "💬 Ask Something"
        )

        if st.button("Ask AI"):

            query = user_query.lower()

            found = False

            # BEST RESTAURANT

            if (
                "best restaurant" in query
                or "top restaurant" in query
            ):

                best = df.sort_values(
                    by="Rating",
                    ascending=False
                ).iloc[0]

                st.success(f"""
                ⭐ Best Restaurant

                🍽️ {best['Restaurant_Name']}

                🍜 Cuisine:
                {best['Cuisine']}

                ⭐ Rating:
                {best['Rating']}
                """)

                found = True

            # CHEAP RESTAURANT

            elif (
                "cheap" in query
                or "budget" in query
            ):

                cheap = df.sort_values(
                    by="Average_Price"
                ).iloc[0]

                st.success(f"""
                💰 Cheapest Restaurant

                🍽️ {cheap['Restaurant_Name']}

                🍜 Cuisine:
                {cheap['Cuisine']}

                💰 Price:
                ₹{cheap['Average_Price']}
                """)

                found = True

            # CUISINE SEARCH

            cuisines = df["Cuisine"].dropna().unique()

            for cuisine in cuisines:

                if cuisine.lower() in query:

                    cuisine_df = df[
                        df["Cuisine"]
                        .str.contains(
                            cuisine,
                            case=False,
                            na=False
                        )
                    ]

                    if not cuisine_df.empty:

                        best = cuisine_df.sort_values(
                            by="Rating",
                            ascending=False
                        ).iloc[0]

                        st.success(f"""
                        🍜 Best {cuisine} Restaurant

                        🍽️ {best['Restaurant_Name']}

                        ⭐ Rating:
                        {best['Rating']}

                        💰 Price:
                        ₹{best['Average_Price']}

                        📍 Area:
                        {best['Area']}
                        """)

                        found = True
                        break

            # DELIVERY

            if (
                not found and
                "delivery" in query
            ):

                delivery_df = df[
                    df["Delivery_Available"]
                    .astype(str)
                    .str.contains(
                        "Yes",
                        case=False,
                        na=False
                    )
                ]

                if not delivery_df.empty:

                    best = delivery_df.sort_values(
                        by="Rating",
                        ascending=False
                    ).iloc[0]

                    st.success(f"""
                    🚚 Best Delivery Restaurant

                    🍽️ {best['Restaurant_Name']}

                    ⭐ Rating:
                    {best['Rating']}
                    """)

                    found = True

            # RATING

            if (
                not found and
                "rating" in query
            ):

                avg = round(
                    df["Rating"].mean(),
                    2
                )

                st.success(f"""
                ⭐ Average Restaurant Rating:
                {avg}
                """)

                found = True

            # DEFAULT

            if not found:

                st.info("""
                🤖 Try Asking:

                • Best restaurant
                • Cheap restaurants
                • Pizza restaurants
                • Chinese food
                • Delivery restaurants
                • Restaurant ratings
                """)

    # =====================================================
    # FAVORITES
    # =====================================================

    elif menu == "❤️ Favorites":

        st.title("❤️ Favorite Restaurants")

        if st.session_state.favorites:

            for fav in st.session_state.favorites:

                st.success(f"🍕 {fav}")

        else:

            st.info("No favorites added")

    # =====================================================
    # FOOTER
    # =====================================================

    st.markdown("""
    <div class="footer">

    <hr>

    <h4>
    Made By Venkatesh 🚀
    </h4>

    </div>
    """, unsafe_allow_html=True)

