import streamlit as st
import pandas as pd
from supabase import create_client, Client
from io import BytesIO

# --------------------------------------------------
# PAGE SETTINGS
# --------------------------------------------------

st.set_page_config(
    page_title="RideLedger",
    page_icon="🚗",
    layout="wide"
)

st.title("🚗 RideLedger")
st.caption("Enter each ride, save it, and build your daily report.")


# --------------------------------------------------
# SUPABASE CONNECTION
# --------------------------------------------------

SUPABASE_URL = st.secrets["SUPABASE_URL"]
SUPABASE_KEY = st.secrets["SUPABASE_KEY"]

supabase: Client = create_client(
    SUPABASE_URL,
    SUPABASE_KEY
)


# --------------------------------------------------
# INPUT SECTION
# --------------------------------------------------

st.subheader("🚗 Ride Information")

col1, col2, col3 = st.columns(3)

with col1:
    ride_date = st.date_input(
        "Date"
    )

    pickup = st.text_input(
        "Area of Pickup"
    )

    drop = st.text_input(
        "Area of Drop"
    )

with col2:
    distance = st.number_input(
        "Distance Covered (km)",
        min_value=0.0,
        step=0.1
    )

    received = st.number_input(
        "Received Amount",
        min_value=0.0,
        step=0.01
    )

    service_payment = st.number_input(
        "Service Payment",
        min_value=0.0,
        step=0.01
    )

with col3:
    gst = st.number_input(
        "GST",
        min_value=0.0,
        step=0.01
    )

    ride_fare_gst = st.number_input(
        "Ride Fare GST",
        min_value=0.0,
        step=0.01
    )

    fuel_consumption = st.number_input(
        "Fuel Consumption (km/L)",
        min_value=0.0,
        step=0.1
    )

    fuel_rate = st.number_input(
        "Fuel Rate",
        min_value=0.0,
        step=0.01
    )


# --------------------------------------------------
# CALCULATIONS
# --------------------------------------------------

total_deduction = (
    service_payment
    + gst
    + ride_fare_gst
)

net_amount = (
    received
    - total_deduction
)

if distance > 0:
    rate_per_km = received / distance
else:
    rate_per_km = 0

if fuel_consumption > 0:
    fuel_consumption_per_ride = (
        distance / fuel_consumption
    )
else:
    fuel_consumption_per_ride = 0

fuel_amount = (
    fuel_consumption_per_ride
    * fuel_rate
)

saving = (
    net_amount
    - fuel_amount
)


# --------------------------------------------------
# SHOW CALCULATIONS
# --------------------------------------------------

st.subheader("📊 Ride Calculation")

c1, c2, c3, c4, c5 = st.columns(5)

c1.metric(
    "Total Deduction",
    f"Rs {total_deduction:,.2f}"
)

c2.metric(
    "Net Amount",
    f"Rs {net_amount:,.2f}"
)

c3.metric(
    "Rate / Km",
    f"Rs {rate_per_km:,.2f}"
)

c4.metric(
    "Fuel Amount",
    f"Rs {fuel_amount:,.2f}"
)

c5.metric(
    "Saving",
    f"Rs {saving:,.2f}"
)


# --------------------------------------------------
# ADD RIDE
# --------------------------------------------------

if st.button(
    "➕ Add Ride",
    type="primary",
    use_container_width=True
):

    if distance <= 0:
        st.error("Distance must be greater than 0.")

    elif received < 0:
        st.error("Received amount cannot be negative.")

    else:

        ride_data = {
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
            "fuel_consumption_per_ride": fuel_consumption_per_ride,
            "fuel_rate": fuel_rate,
            "fuel_amount": fuel_amount,
            "saving": saving
        }

        try:
            supabase.table("rides").insert(
                ride_data
            ).execute()

            st.success(
                "✅ Ride saved permanently!"
            )

            st.rerun()

        except Exception as e:
            st.error(
                f"Could not save ride: {e}"
            )


# --------------------------------------------------
# LOAD RIDES
# --------------------------------------------------

st.subheader("📋 Saved Rides")

try:

    response = (
        supabase
        .table("rides")
        .select("*")
        .order("ride_date", desc=True)
        .order("id", desc=True)
        .execute()
    )

    rides = response.data

except Exception as e:

    rides = []

    st.error(
        f"Could not load rides: {e}"
    )


# --------------------------------------------------
# DISPLAY RIDES
# --------------------------------------------------

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

    df = df[
        [
            column
            for column in display_columns
            if column in df.columns
        ]
    ]

    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True
    )

else:

    st.info(
        "No rides saved yet."
    )


# --------------------------------------------------
# DELETE LAST RIDE
# --------------------------------------------------

if rides:

    st.subheader("🗑️ Delete Ride")

    if st.button(
        "Delete Last Ride",
        type="secondary"
    ):

        last_ride = rides[0]

        try:

            (
                supabase
                .table("rides")
                .delete()
                .eq("id", last_ride["id"])
                .execute()
            )

            st.success(
                "Last ride deleted."
            )

            st.rerun()

        except Exception as e:

            st.error(
                f"Could not delete ride: {e}"
            )


# --------------------------------------------------
# OVERALL SUMMARY
# --------------------------------------------------

if rides:

    df = pd.DataFrame(rides)

    st.subheader("📈 Overall Summary")

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
        "Total Rides",
        total_rides
    )

    c2.metric(
        "Total Distance",
        f"{total_distance:,.2f} km"
    )

    c3.metric(
        "Total Received",
        f"Rs {total_received:,.2f}"
    )

    c4.metric(
        "Total Deduction",
        f"Rs {total_deduction:,.2f}"
    )

    c1, c2, c3 = st.columns(3)

    c1.metric(
        "Total Net Amount",
        f"Rs {total_net:,.2f}"
    )

    c2.metric(
        "Total Fuel Amount",
        f"Rs {total_fuel:,.2f}"
    )

    c3.metric(
        "Total Saving",
        f"Rs {total_saving:,.2f}"
    )


# --------------------------------------------------
# DAILY SUMMARY
# --------------------------------------------------

if rides:

    st.subheader("📅 Daily Summary")

    df = pd.DataFrame(rides)

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


# --------------------------------------------------
# MONTHLY SUMMARY
# --------------------------------------------------

if rides:

    st.subheader("📆 Monthly Summary")

    df = pd.DataFrame(rides)

    df["ride_date"] = pd.to_datetime(
        df["ride_date"]
    )

    df["Month"] = (
        df["ride_date"]
        .dt.to_period("M")
        .astype(str)
    )

    monthly = (
        df.groupby("Month")
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


# --------------------------------------------------
# EXCEL DOWNLOAD
# --------------------------------------------------

if rides:

    st.subheader("📥 Export")

    output = BytesIO()

    with pd.ExcelWriter(
        output,
        engine="openpyxl"
    ) as writer:

        pd.DataFrame(rides).to_excel(
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
