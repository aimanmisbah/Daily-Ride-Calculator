import streamlit as st
import pandas as pd
from io import BytesIO
from datetime import date

# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Ride Ledger",
    page_icon="🚗",
    layout="wide"
)

# ============================================================
# SESSION STORAGE
# ============================================================

if "rides" not in st.session_state:
    st.session_state.rides = []


# ============================================================
# TITLE
# ============================================================

st.title("🚗 Ride Ledger")
st.caption("Enter each ride, save it, and build your daily report.")


# ============================================================
# INPUT SECTION
# ============================================================

st.subheader("🚗 Ride Information")

col1, col2, col3 = st.columns(3)

with col1:
    ride_date = st.date_input(
        "Date",
        value=date.today()
    )

    pickup = st.text_input(
        "Area of Pickup",
        placeholder="e.g. Clifton"
    )

    drop = st.text_input(
        "Area of Drop",
        placeholder="e.g. DHA"
    )

    distance = st.number_input(
        "Distance Covered (Km)",
        min_value=0.0,
        value=0.0,
        step=0.1
    )

with col2:
    received = st.number_input(
        "Received Amount",
        min_value=0.0,
        value=0.0,
        step=1.0
    )

    service_payment = st.number_input(
        "Service Payment",
        min_value=0.0,
        value=0.0,
        step=0.01
    )

    gst = st.number_input(
        "GST",
        min_value=0.0,
        value=0.0,
        step=0.01
    )

    ride_fare_gst = st.number_input(
        "Ride Fare GST",
        min_value=0.0,
        value=0.0,
        step=0.01
    )

with col3:
    fuel_consumption = st.number_input(
        "Vehicle Fuel Consumption (Km/L)",
        min_value=0.01,
        value=13.0,
        step=0.1
    )

    fuel_rate = st.number_input(
        "Fuel Rate",
        min_value=0.0,
        value=367.75,
        step=0.01
    )


# ============================================================
# CALCULATIONS
# ============================================================

total_deduction = (
    service_payment
    + gst
    + ride_fare_gst
)

net_amount = received - total_deduction

if distance > 0:
    rate_km = received / distance
else:
    rate_km = 0

# IMPORTANT:
# Use exact fuel liters for fuel amount.
exact_fuel_liters = (
    distance / fuel_consumption
    if distance > 0 and fuel_consumption > 0
    else 0
)

# Rounded only for display
fuel_per_ride = round(exact_fuel_liters, 2)

# Fuel amount uses exact value
fuel_amount = exact_fuel_liters * fuel_rate

saving = net_amount - fuel_amount


# ============================================================
# CALCULATED RESULTS
# ============================================================

st.subheader("📊 Current Ride Calculation")

r1, r2, r3, r4 = st.columns(4)

with r1:
    st.metric(
        "Total Deduction",
        f"Rs. {total_deduction:,.2f}"
    )

with r2:
    st.metric(
        "Net Amount",
        f"Rs. {net_amount:,.2f}"
    )

with r3:
    st.metric(
        "Rate / Km",
        f"Rs. {rate_km:,.2f}"
    )

with r4:
    st.metric(
        "Fuel per Ride",
        f"{fuel_per_ride:.2f} L"
    )

r5, r6 = st.columns(2)

with r5:
    st.metric(
        "Fuel Amount",
        f"Rs. {fuel_amount:,.2f}"
    )

with r6:
    st.metric(
        "Saving",
        f"Rs. {saving:,.2f}"
    )


# ============================================================
# ADD RIDE
# ============================================================

st.divider()

if st.button(
    "➕ Add Ride",
    type="primary",
    use_container_width=True
):

    # Validation
    if distance <= 0:
        st.error("Distance must be greater than 0.")

    elif received < 0:
        st.error("Received Amount cannot be negative.")

    elif fuel_consumption <= 0:
        st.error("Fuel Consumption must be greater than 0.")

    else:

        ride = {
            "Date": ride_date,
            "Area of Pickup": pickup,
            "Area of Drop": drop,
            "Distance Covered (Km)": distance,
            "Received Amount": received,
            "Service Payment": service_payment,
            "GST": gst,
            "Ride Fare GST": ride_fare_gst,
            "Total Deduction": total_deduction,
            "Net Amount": net_amount,
            "Rate/Km": rate_km,
            "Fuel Consumption (Km/L)": fuel_consumption,

            # Store the exact value internally
            "Fuel Consumption per Ride (L)": exact_fuel_liters,

            "Fuel Rate": fuel_rate,
            "Fuel Amount": fuel_amount,
            "Saving": saving
        }

        st.session_state.rides.append(ride)

        st.success(
            f"✅ Ride #{len(st.session_state.rides)} saved successfully!"
        )

        st.rerun()


# ============================================================
# SAVED RIDES
# ============================================================

st.divider()

st.subheader("📋 Saved Rides")

if len(st.session_state.rides) == 0:

    st.info(
        "No rides have been added yet. "
        "Enter your first ride and click '➕ Add Ride'."
    )

else:

    df = pd.DataFrame(st.session_state.rides)

    display_df = df.copy()

    # Round values for display
    display_df[
        "Fuel Consumption per Ride (L)"
    ] = display_df[
        "Fuel Consumption per Ride (L)"
    ].round(2)

    display_df[
        "Distance Covered (Km)"
    ] = display_df[
        "Distance Covered (Km)"
    ].round(2)

    display_df[
        "Rate/Km"
    ] = display_df[
        "Rate/Km"
    ].round(2)

    display_df[
        "Fuel Consumption (Km/L)"
    ] = display_df[
        "Fuel Consumption (Km/L)"
    ].round(2)

    display_df[
        "Received Amount"
    ] = display_df[
        "Received Amount"
    ].round(2)

    display_df[
        "Service Payment"
    ] = display_df[
        "Service Payment"
    ].round(2)

    display_df[
        "GST"
    ] = display_df[
        "GST"
    ].round(2)

    display_df[
        "Ride Fare GST"
    ] = display_df[
        "Ride Fare GST"
    ].round(2)

    display_df[
        "Total Deduction"
    ] = display_df[
        "Total Deduction"
    ].round(2)

    display_df[
        "Net Amount"
    ] = display_df[
        "Net Amount"
    ].round(2)

    display_df[
        "Fuel Rate"
    ] = display_df[
        "Fuel Rate"
    ].round(2)

    display_df[
        "Fuel Amount"
    ] = display_df[
        "Fuel Amount"
    ].round(2)

    display_df[
        "Saving"
    ] = display_df[
        "Saving"
    ].round(2)

    st.dataframe(
        display_df,
        use_container_width=True,
        hide_index=True
    )


# ============================================================
# DELETE LAST RIDE
# ============================================================

if len(st.session_state.rides) > 0:

    if st.button(
        "🗑️ Delete Last Ride",
        use_container_width=True
    ):

        deleted = st.session_state.rides.pop()

        st.warning(
            f"Deleted: "
            f"{deleted['Area of Pickup']} → "
            f"{deleted['Area of Drop']}"
        )

        st.rerun()


# ============================================================
# SUMMARY
# ============================================================

if len(st.session_state.rides) > 0:

    st.divider()

    st.subheader("📊 Overall Summary")

    df = pd.DataFrame(st.session_state.rides)

    total_rides = len(df)
    total_distance = df["Distance Covered (Km)"].sum()
    total_received = df["Received Amount"].sum()
    total_service = df["Service Payment"].sum()
    total_gst = df["GST"].sum()
    total_ride_fare_gst = df["Ride Fare GST"].sum()
    total_deduction = df["Total Deduction"].sum()
    total_net = df["Net Amount"].sum()
    total_fuel = df["Fuel Amount"].sum()
    total_saving = df["Saving"].sum()

    s1, s2, s3, s4, s5 = st.columns(5)

    with s1:
        st.metric(
            "Total Rides",
            total_rides
        )

    with s2:
        st.metric(
            "Distance",
            f"{total_distance:,.2f} Km"
        )

    with s3:
        st.metric(
            "Received",
            f"Rs. {total_received:,.2f}"
        )

    with s4:
        st.metric(
            "Net Amount",
            f"Rs. {total_net:,.2f}"
        )

    with s5:
        st.metric(
            "Saving",
            f"Rs. {total_saving:,.2f}"
        )

    s6, s7, s8, s9, s10 = st.columns(5)

    with s6:
        st.metric(
            "Service Payment",
            f"Rs. {total_service:,.2f}"
        )

    with s7:
        st.metric(
            "GST",
            f"Rs. {total_gst:,.2f}"
        )

    with s8:
        st.metric(
            "Ride Fare GST",
            f"Rs. {total_ride_fare_gst:,.2f}"
        )

    with s9:
        st.metric(
            "Total Deduction",
            f"Rs. {total_deduction:,.2f}"
        )

    with s10:
        st.metric(
            "Fuel Amount",
            f"Rs. {total_fuel:,.2f}"
        )


# ============================================================
# DAILY SUMMARY
# ============================================================

if len(st.session_state.rides) > 0:

    st.subheader("📅 Daily Summary")

    df = pd.DataFrame(st.session_state.rides)

    daily = (
        df.groupby("Date")
        .agg(
            Rides=("Date", "count"),
            Distance_Km=("Distance Covered (Km)", "sum"),
            Received=("Received Amount", "sum"),
            Total_Deduction=("Total Deduction", "sum"),
            Net_Amount=("Net Amount", "sum"),
            Fuel_Amount=("Fuel Amount", "sum"),
            Saving=("Saving", "sum")
        )
        .reset_index()
    )

    st.dataframe(
        daily,
        use_container_width=True,
        hide_index=True
    )


# ============================================================
# MONTHLY SUMMARY
# ============================================================

if len(st.session_state.rides) > 0:

    st.subheader("📆 Monthly Summary")

    df = pd.DataFrame(st.session_state.rides)

    df["Month"] = pd.to_datetime(
        df["Date"]
    ).dt.to_period("M").astype(str)

    monthly = (
        df.groupby("Month")
        .agg(
            Rides=("Date", "count"),
            Distance_Km=("Distance Covered (Km)", "sum"),
            Received=("Received Amount", "sum"),
            Total_Deduction=("Total Deduction", "sum"),
            Net_Amount=("Net Amount", "sum"),
            Fuel_Amount=("Fuel Amount", "sum"),
            Saving=("Saving", "sum")
        )
        .reset_index()
    )

    st.dataframe(
        monthly,
        use_container_width=True,
        hide_index=True
    )


# ============================================================
# EXCEL EXPORT
# ============================================================

def create_excel():

    df = pd.DataFrame(st.session_state.rides)

    # Round only for exported display
    export_df = df.copy()

    export_df[
        "Fuel Consumption per Ride (L)"
    ] = export_df[
        "Fuel Consumption per Ride (L)"
    ].round(2)

    output = BytesIO()

    with pd.ExcelWriter(
        output,
        engine="openpyxl"
    ) as writer:

        export_df.to_excel(
            writer,
            sheet_name="Ride Details",
            index=False
        )

        # Overall summary
        overall = pd.DataFrame({
            "Metric": [
                "Total Rides",
                "Total Distance (Km)",
                "Total Received Amount",
                "Total Service Payment",
                "Total GST",
                "Total Ride Fare GST",
                "Total Deduction",
                "Total Net Amount",
                "Total Fuel Amount",
                "Total Saving"
            ],

            "Value": [
                len(df),
                df["Distance Covered (Km)"].sum(),
                df["Received Amount"].sum(),
                df["Service Payment"].sum(),
                df["GST"].sum(),
                df["Ride Fare GST"].sum(),
                df["Total Deduction"].sum(),
                df["Net Amount"].sum(),
                df["Fuel Amount"].sum(),
                df["Saving"].sum()
            ]
        })

        overall.to_excel(
            writer,
            sheet_name="Overall Summary",
            index=False
        )

        # Daily summary
        daily.to_excel(
            writer,
            sheet_name="Daily Summary",
            index=False
        )

        # Monthly summary
        monthly.to_excel(
            writer,
            sheet_name="Monthly Summary",
            index=False
        )

        # Formatting
        workbook = writer.book

        for worksheet in workbook.worksheets:

            for cell in worksheet[1]:
                cell.font = cell.font.copy(
                    bold=True
                )

            for column in worksheet.columns:

                max_length = 0
                column_letter = column[0].column_letter

                for cell in column:

                    if cell.value is not None:

                        max_length = max(
                            max_length,
                            len(str(cell.value))
                        )

                worksheet.column_dimensions[
                    column_letter
                ].width = min(
                    max_length + 2,
                    30
                )

    output.seek(0)

    return output


# ============================================================
# DOWNLOAD BUTTON
# ============================================================

if len(st.session_state.rides) > 0:

    st.divider()

    st.subheader("📥 Export Report")

    excel_file = create_excel()

    st.download_button(
        label="📥 Download Excel Report",
        data=excel_file,
        file_name="Daily_Ride_Report.xlsx",
        mime=(
            "application/vnd.openxmlformats-officedocument."
            "spreadsheetml.sheet"
        ),
        use_container_width=True
    )
