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

# =========================================================
# CUSTOM DESIGN - CLEAN PREMIUM THEME
# =========================================================

st.markdown(
    """
    <style>

    /* =====================================================
       MAIN BACKGROUND
       ===================================================== */

    .stApp {
        background:
            linear-gradient(
                135deg,
                #f5f9ff 0%,
                #eef5ff 45%,
                #f8fbff 100%
            );
    }

    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
        max-width: 1400px;
    }


    /* =====================================================
       SIDEBAR
       ===================================================== */

    section[data-testid="stSidebar"] {

        background:
            linear-gradient(
                180deg,
                #ffffff 0%,
                #f4f8ff 100%
            );

        border-right:
            1px solid #dce7f5;

        box-shadow:
            5px 0 25px rgba(44, 83, 130, 0.08);
    }

    section[data-testid="stSidebar"] .block-container {
        padding-top: 1.5rem;
    }


    /* =====================================================
       HEADINGS
       ===================================================== */

    h1 {
        color: #163a63 !important;

        font-size: 2.8rem !important;

        font-weight: 800 !important;

        letter-spacing: -1px;
    }

    h2 {
        color: #193f68 !important;

        font-weight: 750 !important;
    }

    h3 {
        color: #234b73 !important;

        font-weight: 700 !important;
    }


    /* =====================================================
       NORMAL TEXT
       ===================================================== */

    p {
        color: #52677e;
    }


    /* =====================================================
       METRIC CARDS - 3D EFFECT
       ===================================================== */

    div[data-testid="stMetric"] {

        background:
            linear-gradient(
                145deg,
                #ffffff,
                #f4f8fd
            );

        border:
            1px solid #dce7f3;

        border-radius:
            20px;

        padding:
            22px;

        min-height:
            135px;

        box-shadow:
            0 8px 18px rgba(43, 82, 125, 0.10),
            0 2px 4px rgba(43, 82, 125, 0.06);

        transition:
            all 0.25s ease;
    }


    div[data-testid="stMetric"]:hover {

        transform:
            translateY(-5px);

        box-shadow:
            0 16px 30px rgba(43, 82, 125, 0.16);
    }


    div[data-testid="stMetricLabel"] {

        color:
            #66809b !important;

        font-size:
            0.9rem !important;

        font-weight:
            650 !important;
    }


    div[data-testid="stMetricValue"] {

        color:
            #164a7a !important;

        font-size:
            2rem !important;

        font-weight:
            800 !important;
    }


    /* =====================================================
       BUTTONS
       ===================================================== */

    .stButton > button {

        border:
            1px solid #c7dbf2;

        border-radius:
            12px;

        background:
            linear-gradient(
                145deg,
                #ffffff,
                #edf5ff
            );

        color:
            #17558c;

        font-weight:
            700;

        box-shadow:
            0 5px 12px rgba(50, 100, 150, 0.10);

        transition:
            all 0.2s ease;
    }


    .stButton > button:hover {

        background:
            linear-gradient(
                145deg,
                #edf6ff,
                #dcecff
            );

        border-color:
            #9fc5eb;

        color:
            #0d477d;

        transform:
            translateY(-2px);

        box-shadow:
            0 9px 18px rgba(50, 100, 150, 0.15);
    }


    /* =====================================================
       INPUT FIELDS
       ===================================================== */

    input,
    textarea,
    div[data-baseweb="select"] > div {

        border-radius:
            11px !important;

        background:
            #ffffff !important;

        border:
            1px solid #d3e0ed !important;

        color:
            #203d59 !important;
    }


    input:focus,
    textarea:focus {

        border-color:
            #4d96dc !important;

        box-shadow:
            0 0 0 2px rgba(77,150,220,0.12) !important;
    }


    /* =====================================================
       DATAFRAME
       ===================================================== */

    div[data-testid="stDataFrame"] {

        border-radius:
            18px;

        overflow:
            hidden;

        border:
            1px solid #d9e5f1;

        box-shadow:
            0 8px 20px rgba(45, 80, 115, 0.08);
    }


    /* =====================================================
       EXPANDERS
       ===================================================== */

    div[data-testid="stExpander"] {

        border:
            1px solid #dce7f2 !important;

        border-radius:
            16px !important;

        background:
            rgba(255,255,255,0.80);

        box-shadow:
            0 6px 16px rgba(45, 80, 115, 0.07);
    }


    /* =====================================================
       ALERTS
       ===================================================== */

    div[data-testid="stAlert"] {

        border-radius:
            14px !important;

        border:
            1px solid #d7e4f0 !important;

        box-shadow:
            0 5px 15px rgba(45, 80, 115, 0.06);
    }


    /* =====================================================
       SIDEBAR NAVIGATION
       ===================================================== */

    section[data-testid="stSidebar"]
    div[role="radiogroup"] label {

        border-radius:
            12px;

        padding:
            10px 12px;

        margin:
            5px 0;

        color:
            #385673;

        transition:
            all 0.2s ease;
    }


    section[data-testid="stSidebar"]
    div[role="radiogroup"] label:hover {

        background:
            #eaf3ff;

        transform:
            translateX(3px);
    }


    /* =====================================================
       DIVIDER
       ===================================================== */

    hr {

        border:
            none !important;

        height:
            1px;

        background:
            linear-gradient(
                90deg,
                transparent,
                #cbdceb,
                transparent
            );
    }


    /* =====================================================
       FILE UPLOADER
       ===================================================== */

    section[data-testid="stFileUploaderDropzone"] {

        border-radius:
            15px;

        background:
            #ffffff;

        border:
            1px dashed #b9cee3;
    }


    /* =====================================================
       SELECTBOX / DROPDOWN
       ===================================================== */

    div[data-baseweb="select"] {

        border-radius:
            11px;
    }


    /* =====================================================
       CHECKBOX
       ===================================================== */

    div[data-testid="stCheckbox"] {

        color:
            #365775;
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

    st.title("🚗 RideLedger")

    st.caption(
        "Manage your rides, earnings and expenses in one place."
    )

    login_tab, signup_tab = st.tabs(
        ["🔐 Login", "✨ Create Account"]
    )


    # -----------------------------------------------------
    # LOGIN
    # -----------------------------------------------------

    with login_tab:

        st.subheader("Welcome back 👋")

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

        st.subheader("Create your account 🚀")

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
                                        "username": signup_username
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


    st.divider()

    st.caption(
        "🔒 Your ride data is protected by Supabase."
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

    st.title("🚗")
    st.caption("RideLedger")

    st.divider()

    st.write(f"### 👋 Hello, {username}")

    if user:
        st.caption(user.email)

    st.divider()

    page = st.radio(
        "Navigation",
        [
            "🏠 Dashboard",
            "➕ Add Ride",
            "📋 Ride History",
            "📊 Reports"
        ],
        label_visibility="collapsed"
    )

    st.divider()

    if st.button("🚪 Logout", use_container_width=True):
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
# MAIN HEADER
# =========================================================

st.title("🚗 RideLedger")

st.subheader(f"Welcome back, {username} 👋")

st.write("Your driving overview")

st.caption(
    "Track rides, earnings, expenses and savings — all in one place."
)

st.divider()

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

    st.header("📊 Dashboard")

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

            st.metric(
                "🚗 Total Rides",
                f"{total_rides:,}"
            )

        with c2:

            st.metric(
                "🛣️ Total Distance",
                f"{total_distance:,.1f} km"
            )

        with c3:

            st.metric(
                "💰 Total Received",
                f"Rs {total_received:,.0f}"
            )


        st.write("")


        c1, c2, c3 = st.columns(3)

        with c1:

            st.metric(
                "💵 Net Amount",
                f"Rs {total_net:,.0f}"
            )

        with c2:

            st.metric(
                "⛽ Fuel Cost",
                f"Rs {total_fuel:,.0f}"
            )

        with c3:

            st.metric(
                "📈 Total Saving",
                f"Rs {total_saving:,.0f}"
            )


        # -------------------------------------------------
        # RECENT RIDES
        # -------------------------------------------------

        st.divider()

        st.subheader("🕐 Recent Rides")

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

    st.header("➕ Add New Ride")

    st.caption(
        "Enter your ride details below. "
        "RideLedger will calculate your earnings automatically."
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

    st.header("📋 Ride History")

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


        st.divider()

        st.subheader("🗑️ Delete a Ride")

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

    st.header("📊 Reports & Analytics")

    if rides:

        df = pd.DataFrame(rides)


        # -------------------------------------------------
        # OVERALL
        # -------------------------------------------------

        st.subheader("💰 Overall Summary")

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

        st.divider()

        st.subheader("📅 Daily Summary")

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

        st.subheader("📆 Monthly Summary")

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

        st.subheader("📥 Export")

        output = BytesIO()

        with pd.ExcelWriter(
            output,
            engine="openpyxl"
        ):

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

st.divider()

st.caption(
    "🚗 RideLedger • Smart ride tracking and reporting"
)
