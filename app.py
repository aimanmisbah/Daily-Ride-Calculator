import streamlit as st
import pandas as pd
from supabase import create_client, Client
from io import BytesIO


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="RideLedger",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="expanded"
)


# =========================================================
# CUSTOM DESIGN
# =========================================================

st.markdown(
    """
    <style>

    /* Main background */
    .stApp {
        background: #f6f8fb;
    }

    .block-container {
        max-width: 1400px;
        padding-top: 2rem;
        padding-bottom: 3rem;
    }

    /* Header */
    .hero {
        background: linear-gradient(
            135deg,
            #111827,
            #1f2937
        );
        padding: 32px;
        border-radius: 22px;
        margin-bottom: 25px;
        box-shadow: 0 12px 30px rgba(0,0,0,0.12);
    }

    .hero-title {
        color: white;
        font-size: 40px;
        font-weight: 800;
        margin: 0;
    }

    .hero-text {
        color: #d1d5db;
        font-size: 16px;
        margin-top: 8px;
    }

    /* Section title */
    .section-title {
        font-size: 25px;
        font-weight: 800;
        color: #111827;
        margin-top: 25px;
        margin-bottom: 15px;
    }

    .section-text {
        color: #6b7280;
        margin-bottom: 20px;
    }

    /* Cards */
    .card {
        background: white;
        border: 1px solid #e5e7eb;
        border-radius: 18px;
        padding: 22px;
        box-shadow: 0 5px 18px rgba(0,0,0,0.05);
    }

    .card-label {
        color: #6b7280;
        font-size: 13px;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: .5px;
    }

    .card-value {
        color: #111827;
        font-size: 27px;
        font-weight: 800;
        margin-top: 7px;
    }

    /* Login */
    .login-container {
        max-width: 500px;
        margin: auto;
        padding-top: 50px;
    }

    .login-logo {
        text-align: center;
        font-size: 60px;
    }

    .login-title {
        text-align: center;
        font-size: 36px;
        font-weight: 800;
        color: #111827;
    }

    .login-subtitle {
        text-align: center;
        color: #6b7280;
        margin-bottom: 30px;
    }

    /* Footer */
    .footer {
        text-align: center;
        color: #9ca3af;
        padding-top: 40px;
        font-size: 13px;
    }

    /* Buttons */
    .stButton > button {
        border-radius: 10px;
        font-weight: 700;
        min-height: 42px;
    }

    /* Inputs */
    .stTextInput input,
    .stNumberInput input {
        border-radius: 9px;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# =========================================================
# SUPABASE
# =========================================================

SUPABASE_URL = st.secrets["SUPABASE_URL"]
SUPABASE_KEY = st.secrets["SUPABASE_KEY"]

supabase: Client = create_client(
    SUPABASE_URL,
    SUPABASE_KEY
)


# =========================================================
# SESSION STATE
# =========================================================

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "user" not in st.session_state:
    st.session_state.user = None

if "access_token" not in st.session_state:
    st.session_state.access_token = None

if "refresh_token" not in st.session_state:
    st.session_state.refresh_token = None


# =========================================================
# RESTORE LOGIN SESSION
# =========================================================

if (
    st.session_state.access_token
    and st.session_state.refresh_token
):

    try:

        supabase.auth.set_session(
            st.session_state.access_token,
            st.session_state.refresh_token
        )

        current_user = supabase.auth.get_user()

        if current_user and current_user.user:

            st.session_state.user = current_user.user
            st.session_state.logged_in = True

    except Exception:

        st.session_state.logged_in = False
        st.session_state.user = None


# =========================================================
# LOGIN / SIGNUP
# =========================================================

if not st.session_state.logged_in:

    st.markdown(
        '<div class="login-container">',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="login-logo">🚗</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="login-title">RideLedger</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="login-subtitle">'
        'Manage your rides, earnings and expenses'
        '</div>',
        unsafe_allow_html=True
    )

    login_tab, signup_tab = st.tabs(
        ["🔐 Login", "✨ Create Account"]
    )

    # -----------------------------------------------------
    # LOGIN
    # -----------------------------------------------------

    with login_tab:

        st.markdown("### Welcome back 👋")

        login_email = st.text_input(
            "Email",
            placeholder="Enter your email",
            key="login_email"
        )

        login_password = st.text_input(
            "Password",
            type="password",
            placeholder="Enter your password",
            key="login_password"
        )

        if st.button(
            "🔐 Login",
            type="primary",
            use_container_width=True
        ):

            if not login_email or not login_password:

                st.error(
                    "Please enter your email and password."
                )

            else:

                try:

                    response = (
                        supabase.auth
                        .sign_in_with_password(
                            {
                                "email": login_email,
                                "password": login_password
                            }
                        )
                    )

                    if response.user and response.session:

                        st.session_state.user = response.user

                        st.session_state.access_token = (
                            response.session.access_token
                        )

                        st.session_state.refresh_token = (
                            response.session.refresh_token
                        )

                        st.session_state.logged_in = True

                        st.success(
                            "Login successful! 🎉"
                        )

                        st.rerun()

                    else:

                        st.error(
                            "Login failed."
                        )

                except Exception as e:

                    st.error(
                        f"Login failed: {e}"
                    )

    # -----------------------------------------------------
    # SIGNUP
    # -----------------------------------------------------

    with signup_tab:

        st.markdown("### Create your account 🚀")

        signup_username = st.text_input(
            "Username",
            placeholder="Choose a username",
            key="signup_username"
        )

        signup_email = st.text_input(
            "Email",
            placeholder="Enter your email",
            key="signup_email"
        )

        signup_password = st.text_input(
            "Password",
            type="password",
            placeholder="Create a password",
            key="signup_password"
        )

        signup_confirm = st.text_input(
            "Confirm Password",
            type="password",
            placeholder="Repeat your password",
            key="signup_confirm"
        )

        if st.button(
            "✨ Create Account",
            type="primary",
            use_container_width=True
        ):

            if not signup_username:

                st.error(
                    "Please choose a username."
                )

            elif not signup_email:

                st.error(
                    "Please enter your email."
                )

            elif not signup_password:

                st.error(
                    "Please create a password."
                )

            elif signup_password != signup_confirm:

                st.error(
                    "Passwords do not match."
                )

            elif len(signup_password) < 6:

                st.error(
                    "Password must contain at least 6 characters."
                )

            else:

                try:

                    response = (
                        supabase.auth
                        .sign_up(
                            {
                                "email": signup_email,
                                "password": signup_password,
                                "options": {
                                    "data": {
                                        "username":
                                            signup_username
                                    }
                                }
                            }
                        )
                    )

                    if response.user:

                        if response.session:

                            st.session_state.user = (
                                response.user
                            )

                            st.session_state.access_token = (
                                response.session.access_token
                            )

                            st.session_state.refresh_token = (
                                response.session.refresh_token
                            )

                            st.session_state.logged_in = True

                            st.success(
                                "Account created successfully! 🎉"
                            )

                            st.rerun()

                        else:

                            st.success(
                                "Account created! "
                                "Please check your email "
                                "to confirm your account."
                            )

                    else:

                        st.error(
                            "Could not create the account."
                        )

                except Exception as e:

                    st.error(
                        f"Signup failed: {e}"
                    )

    st.markdown(
        '<div class="footer">'
        '🔒 Your ride data is protected by Supabase.'
        '</div>',
        unsafe_allow_html=True
    )

    st.stop()


# =========================================================
# USER INFORMATION
# =========================================================

user = st.session_state.user

username = "Driver"

if user:

    try:

        username = user.user_metadata.get(
            "username",
            "Driver"
        )

    except Exception:

        username = "Driver"


# =========================================================
# SIDEBAR
# =========================================================

# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.title("🚗 RideLedger")

    st.divider()

    st.write(f"Hello, {username}")

    page = st.radio(
        "Navigation",
        [
            "🏠 Dashboard",
            "➕ Add Ride",
            "📋 Ride History",
            "📊 Reports"
        ]
    )

    st.divider()

    if st.button("🚪 Logout"):

        try:
            supabase.auth.sign_out()
        except Exception:
            pass

        st.session_state.logged_in = False
        st.session_state.user = None
        st.session_state.access_token = None
        st.session_state.refresh_token = None

        st.rerun()

# =========================================================
# HEADER
# =========================================================

# =========================================================
# HEADER
# =========================================================

st.title("🚗 RideLedger")

st.subheader(f"Welcome back, {username} 👋")

st.caption(
    "Track your rides, earnings and expenses in one place."
)

st.write("")


# =========================================================
# QUICK OVERVIEW
# =========================================================

if rides:

    df = pd.DataFrame(rides)

    total_rides = len(df)

    total_distance = df["distance_covered"].sum()

    total_received = df["received_amount"].sum()

    total_net = df["net_amount"].sum()

    total_saving = df["saving"].sum()

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.metric(
            "🚗 Total Rides",
            f"{total_rides:,}"
        )

    with c2:
        st.metric(
            "🛣️ Distance",
            f"{total_distance:,.1f} km"
        )

    with c3:
        st.metric(
            "💰 Earnings",
            f"Rs {total_received:,.0f}"
        )

    with c4:
        st.metric(
            "📈 Savings",
            f"Rs {total_saving:,.0f}"
        )

    st.write("")

    st.info(
        "💡 Keep adding your rides to build a complete "
        "picture of your earnings, expenses and savings."
    )

else:

    st.info(
        "🚗 Welcome to RideLedger! "
        "Add your first ride to start tracking your earnings."
    )
# =========================================================
# LOAD RIDES
# =========================================================

try:

    response = (
        supabase
        .table("rides")
        .select("*")
        .eq("user_id", user.id)
        .order("ride_date", desc=True)
        .order("id", desc=True)
        .execute()
    )

    rides = response.data or []

except Exception as e:

    rides = []

    st.error(
        f"Could not load rides: {e}"
    )


# =========================================================
# DASHBOARD
# =========================================================

if page == "🏠 Dashboard":

    st.markdown(
        '<div class="section-title">'
        '📊 Dashboard'
        '</div>',
        unsafe_allow_html=True
    )

    if rides:

        df = pd.DataFrame(rides)

        total_rides = len(df)

        total_distance = df[
            "distance_covered"
        ].sum()

        total_received = df[
            "received_amount"
        ].sum()

        total_net = df[
            "net_amount"
        ].sum()

        total_fuel = df[
            "fuel_amount"
        ].sum()

        total_saving = df[
            "saving"
        ].sum()

        # -------------------------------------------------
        # TOP CARDS
        # -------------------------------------------------

        c1, c2, c3 = st.columns(3)

        with c1:

            st.markdown(
                f"""
                <div class="card">
                    <div class="card-label">
                        🚗 Total Rides
                    </div>

                    <div class="card-value">
                        {total_rides:,}
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

        with c2:

            st.markdown(
                f"""
                <div class="card">
                    <div class="card-label">
                        🛣️ Total Distance
                    </div>

                    <div class="card-value">
                        {total_distance:,.1f} km
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

        with c3:

            st.markdown(
                f"""
                <div class="card">
                    <div class="card-label">
                        💰 Total Received
                    </div>

                    <div class="card-value">
                        Rs {total_received:,.0f}
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

        st.write("")

        c1, c2, c3 = st.columns(3)

        with c1:

            st.markdown(
                f"""
                <div class="card">
                    <div class="card-label">
                        💵 Net Amount
                    </div>

                    <div class="card-value">
                        Rs {total_net:,.0f}
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

        with c2:

            st.markdown(
                f"""
                <div class="card">
                    <div class="card-label">
                        ⛽ Fuel Cost
                    </div>

                    <div class="card-value">
                        Rs {total_fuel:,.0f}
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

        with c3:

            st.markdown(
                f"""
                <div class="card">
                    <div class="card-label">
                        📈 Total Saving
                    </div>

                    <div class="card-value">
                        Rs {total_saving:,.0f}
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

        # -------------------------------------------------
        # RECENT RIDES
        # -------------------------------------------------

        st.markdown(
            '<div class="section-title">'
            '🕐 Recent Rides'
            '</div>',
            unsafe_allow_html=True
        )

        recent = df.head(5)

        recent_columns = [
            "ride_date",
            "area_of_pickup",
            "area_of_drop",
            "distance_covered",
            "received_amount",
            "net_amount",
            "saving"
        ]

        recent_columns = [
            column
            for column in recent_columns
            if column in recent.columns
        ]

        st.dataframe(
            recent[recent_columns],
            use_container_width=True,
            hide_index=True
        )

    else:

        st.info(
            "🚗 You don't have any rides yet. "
            "Go to **Add Ride** to record your first ride."
        )


# =========================================================
# ADD RIDE
# =========================================================

elif page == "➕ Add Ride":

    st.markdown(
        '<div class="section-title">'
        '➕ Add New Ride'
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="section-text">'
        'Enter your ride details below. '
        'RideLedger will calculate your earnings automatically.'
        '</div>',
        unsafe_allow_html=True
    )

    with st.form("ride_form"):

        c1, c2, c3 = st.columns(3)

        with c1:

            ride_date = st.date_input(
                "📅 Date"
            )

            pickup = st.text_input(
                "📍 Area of Pickup",
                placeholder="e.g. Clifton"
            )

            drop = st.text_input(
                "🏁 Area of Drop",
                placeholder="e.g. DHA"
            )

        with c2:

            distance = st.number_input(
                "🛣️ Distance Covered (km)",
                min_value=0.0,
                step=0.1
            )

            received = st.number_input(
                "💰 Received Amount",
                min_value=0.0,
                step=0.01
            )

            service_payment = st.number_input(
                "💳 Service Payment",
                min_value=0.0,
                step=0.01
            )

        with c3:

            gst = st.number_input(
                "🧾 GST",
                min_value=0.0,
                step=0.01
            )

            ride_fare_gst = st.number_input(
                "🧾 Ride Fare GST",
                min_value=0.0,
                step=0.01
            )

            fuel_consumption = st.number_input(
                "⛽ Fuel Consumption (km/L)",
                min_value=0.0,
                step=0.1
            )

            fuel_rate = st.number_input(
                "💵 Fuel Rate",
                min_value=0.0,
                step=0.01
            )

        submitted = st.form_submit_button(
            "🚀 Save Ride",
            type="primary",
            use_container_width=True
        )

    # -----------------------------------------------------
    # SAVE RIDE
    # -----------------------------------------------------

    if submitted:

        if distance <= 0:

            st.error(
                "Distance must be greater than 0."
            )

        else:

            total_deduction = (
                service_payment
                + gst
                + ride_fare_gst
            )

            net_amount = (
                received
                - total_deduction
            )

            rate_per_km = (
                received / distance
                if distance > 0
                else 0
            )

            fuel_consumption_per_ride = (
                distance / fuel_consumption
                if fuel_consumption > 0
                else 0
            )

            fuel_amount = (
                fuel_consumption_per_ride
                * fuel_rate
            )

            saving = (
                net_amount
                - fuel_amount
            )

            ride_data = {

                "user_id": user.id,

                "ride_date": str(ride_date),

                "area_of_pickup": pickup,

                "area_of_drop": drop,

                "distance_covered": distance,

                "received_amount": received,

                "service_payment": service_payment,

                "gst": gst,

                "ride_fare_gst": ride_fare_gst,

                "total_deduction": total_deduction,

                "net_amount": net_amount,

                "rate_per_km": rate_per_km,

                "fuel_consumption": fuel_consumption,

                "fuel_consumption_per_ride":
                    fuel_consumption_per_ride,

                "fuel_rate": fuel_rate,

                "fuel_amount": fuel_amount,

                "saving": saving
            }

            try:

                (
                    supabase
                    .table("rides")
                    .insert(ride_data)
                    .execute()
                )

                st.success(
                    "🎉 Ride saved successfully!"
                )

                st.rerun()

            except Exception as e:

                st.error(
                    f"Could not save ride: {e}"
                )


# =========================================================
# RIDE HISTORY
# =========================================================

elif page == "📋 Ride History":

    st.markdown(
        '<div class="section-title">'
        '📋 Ride History'
        '</div>',
        unsafe_allow_html=True
    )

    if rides:

        df = pd.DataFrame(rides)

        display_columns = [
            "id",
            "ride_date",
            "area_of_pickup",
            "area_of_drop",
            "distance_covered",
            "received_amount",
            "service_payment",
            "gst",
            "ride_fare_gst",
            "total_deduction",
            "net_amount",
            "rate_per_km",
            "fuel_consumption",
            "fuel_consumption_per_ride",
            "fuel_rate",
            "fuel_amount",
            "saving"
        ]

        display_columns = [
            column
            for column in display_columns
            if column in df.columns
        ]

        st.dataframe(
            df[display_columns],
            use_container_width=True,
            hide_index=True
        )

        st.markdown(
            '<div class="section-title">'
            '🗑️ Delete a Ride'
            '</div>',
            unsafe_allow_html=True
        )

        ride_options = {}

        for ride in rides:

            label = (
                f"#{ride['id']} | "
                f"{ride['ride_date']} | "
                f"{ride.get('area_of_pickup', '')} → "
                f"{ride.get('area_of_drop', '')}"
            )

            ride_options[label] = ride["id"]

        selected_ride = st.selectbox(
            "Select ride",
            list(ride_options.keys())
        )

        if st.button(
            "🗑️ Delete Selected Ride"
        ):

            selected_id = ride_options[
                selected_ride
            ]

            try:

                (
                    supabase
                    .table("rides")
                    .delete()
                    .eq("id", selected_id)
                    .eq("user_id", user.id)
                    .execute()
                )

                st.success(
                    "Ride deleted successfully."
                )

                st.rerun()

            except Exception as e:

                st.error(
                    f"Could not delete ride: {e}"
                )

    else:

        st.info(
            "📋 No rides saved yet."
        )


# =========================================================
# REPORTS
# =========================================================

elif page == "📊 Reports":

    st.markdown(
        '<div class="section-title">'
        '📊 Reports & Analytics'
        '</div>',
        unsafe_allow_html=True
    )

    if rides:

        df = pd.DataFrame(rides)

        # -------------------------------------------------
        # OVERALL
        # -------------------------------------------------

        st.markdown(
            '<div class="section-title">'
            '💰 Overall Summary'
            '</div>',
            unsafe_allow_html=True
        )

        total_rides = len(df)

        total_distance = df[
            "distance_covered"
        ].sum()

        total_received = df[
            "received_amount"
        ].sum()

        total_deduction = df[
            "total_deduction"
        ].sum()

        total_net = df[
            "net_amount"
        ].sum()

        total_fuel = df[
            "fuel_amount"
        ].sum()

        total_saving = df[
            "saving"
        ].sum()

        c1, c2, c3, c4 = st.columns(4)

        c1.metric(
            "🚗 Total Rides",
            f"{total_rides:,}"
        )

        c2.metric(
            "🛣️ Distance",
            f"{total_distance:,.1f} km"
        )

        c3.metric(
            "💰 Received",
            f"Rs {total_received:,.2f}"
        )

        c4.metric(
            "💳 Deductions",
            f"Rs {total_deduction:,.2f}"
        )

        c1, c2, c3 = st.columns(3)

        c1.metric(
            "💵 Net Amount",
            f"Rs {total_net:,.2f}"
        )

        c2.metric(
            "⛽ Fuel Cost",
            f"Rs {total_fuel:,.2f}"
        )

        c3.metric(
            "📈 Saving",
            f"Rs {total_saving:,.2f}"
        )

        # -------------------------------------------------
        # DAILY
        # -------------------------------------------------

        st.markdown(
            '<div class="section-title">'
            '📅 Daily Summary'
            '</div>',
            unsafe_allow_html=True
        )

        daily = (
            df.groupby("ride_date")
            .agg(
                Rides=("id", "count"),
                Distance=("distance_covered", "sum"),
                Received=("received_amount", "sum"),
                Deduction=("total_deduction", "sum"),
                Net=("net_amount", "sum"),
                Fuel=("fuel_amount", "sum"),
                Saving=("saving", "sum")
            )
            .reset_index()
        )

        st.dataframe(
            daily,
            use_container_width=True,
            hide_index=True
        )

        # -------------------------------------------------
        # MONTHLY
        # -------------------------------------------------

        st.markdown(
            '<div class="section-title">'
            '📆 Monthly Summary'
            '</div>',
            unsafe_allow_html=True
        )

        monthly_df = df.copy()

        monthly_df["ride_date"] = pd.to_datetime(
            monthly_df["ride_date"]
        )

        monthly_df["Month"] = (
            monthly_df["ride_date"]
            .dt.to_period("M")
            .astype(str)
        )

        monthly = (
            monthly_df.groupby("Month")
            .agg(
                Rides=("id", "count"),
                Distance=("distance_covered", "sum"),
                Received=("received_amount", "sum"),
                Deduction=("total_deduction", "sum"),
                Net=("net_amount", "sum"),
                Fuel=("fuel_amount", "sum"),
                Saving=("saving", "sum")
            )
            .reset_index()
        )

        st.dataframe(
            monthly,
            use_container_width=True,
            hide_index=True
        )

        # -------------------------------------------------
        # EXCEL
        # -------------------------------------------------

        st.markdown(
            '<div class="section-title">'
            '📥 Export'
            '</div>',
            unsafe_allow_html=True
        )

        output = BytesIO()

        with pd.ExcelWriter(
            output,
            engine="openpyxl"
        ) as writer:

            df.to_excel(
                writer,
                index=False,
                sheet_name="Rides"
            )

            daily.to_excel(
                writer,
                index=False,
                sheet_name="Daily Summary"
            )

            monthly.to_excel(
                writer,
                index=False,
                sheet_name="Monthly Summary"
            )

        st.download_button(
            label="📥 Download Excel Report",
            data=output.getvalue(),
            file_name="RideLedger_Report.xlsx",
            mime=(
                "application/vnd.openxmlformats-officedocument"
                ".spreadsheetml.sheet"
            ),
            use_container_width=True
        )

    else:

        st.info(
            "📊 Add some rides first to generate reports."
        )


# =========================================================
# FOOTER
# =========================================================

st.markdown(
    """
    <div class="footer">
        🚗 RideLedger • Smart ride tracking and reporting
    </div>
    """,
    unsafe_allow_html=True
)
