import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="EcoWaste AI — Admin Dashboard",
    page_icon="♻️",
    layout="wide"
)

DEMO_DONATION = {
    "Donation ID": "D-001",
    "Donor": "ABC Restaurant",
    "Food": "Biryani",
    "Quantity": 50,
    "Unit": "portions",
    "Recipient": "Hope Community Center (DEMO)",
    "Match Score": 96,
    "Status": "Confirmed (demo)",
    "Pickup": "18:30",
    "Delivery Target": "19:00",
    "Priority": "High"
}

RECIPIENTS = [
    {"Organization": "Hope Community Center (DEMO)", "Accepted Food": "Cooked meal / Packaged food", "Capacity": 60, "Need": "High", "Distance": 2.0},
    {"Organization": "Sunrise Shelter (DEMO)", "Accepted Food": "Cooked meal / Bakery / Packaged food", "Capacity": 40, "Need": "Medium", "Distance": 1.2},
    {"Organization": "Al-Noor Community Kitchen (DEMO)", "Accepted Food": "Cooked meal / Fresh produce", "Capacity": 100, "Need": "Medium", "Distance": 4.5},
    {"Organization": "Green Leaf Welfare Center (DEMO)", "Accepted Food": "Bakery / Fresh produce / Beverages", "Capacity": 80, "Need": "Low", "Distance": 6.0},
    {"Organization": "Unity Food Support (DEMO)", "Accepted Food": "Cooked meal / Packaged food / Bakery", "Capacity": 55, "Need": "High", "Distance": 3.0},
]

if "member5_log" not in st.session_state:
    st.session_state.member5_log = [DEMO_DONATION.copy()]

st.title("♻️ EcoWaste AI")
st.subheader("Member 5 — Admin & Demo Dashboard")

st.info(
    "⚠️ PROTOTYPE: Demo data only. Organizations, donations, distances "
    "and statistics are fictional."
)

st.sidebar.header("Member 5 Controls")

if st.sidebar.button("🍛 Load Biryani Demo"):
    st.session_state.member5_log = [DEMO_DONATION.copy()]
    st.rerun()

if st.sidebar.button("🗑️ Reset Demo Data"):
    st.session_state.member5_log = []
    st.rerun()

st.sidebar.markdown("---")
st.sidebar.write("### Demo Scenario")
st.sidebar.write(
    "Donor: ABC Restaurant\n\n"
    "Food: Biryani\n\n"
    "Quantity: 50 portions\n\n"
    "Recipient: Hope Community Center\n\n"
    "Match Score: 96\n\n"
    "Pickup: 18:30\n\n"
    "Delivery Target: 19:00"
)

logs = st.session_state.member5_log
total_donations = len(logs)
total_portions = sum(item.get("Quantity", 0) for item in logs)
average_score = (
    sum(item.get("Match Score", 0) for item in logs) / total_donations
    if total_donations else 0
)

st.markdown("## 📊 Platform Statistics")
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Donations This Session", total_donations)
with col2:
    st.metric("Portions Matched", total_portions)
with col3:
    st.metric("Average Match Score", f"{average_score:.1f}")

st.markdown("## 🧾 Recent Donations")
if logs:
    st.dataframe(pd.DataFrame(logs), use_container_width=True, hide_index=True)
else:
    st.warning("No demo donations currently available.")

st.markdown("## 🏢 Demo Recipient Organizations")
recipient_df = pd.DataFrame(RECIPIENTS)
st.dataframe(recipient_df, use_container_width=True, hide_index=True)

st.markdown("## 📈 Recipient Capacity")
chart_df = recipient_df[["Organization", "Capacity"]].set_index("Organization")
st.bar_chart(chart_df)

st.markdown("## 🍛 Current Demo Result")
if logs:
    latest = logs[-1]
    result_col1, result_col2 = st.columns(2)

    with result_col1:
        st.success(f"Donation **{latest['Donation ID']}** matched successfully.")
        st.write(f"**Food:** {latest['Food']}")
        st.write(f"**Quantity:** {latest['Quantity']} {latest['Unit']}")
        st.write(f"**Recipient:** {latest['Recipient']}")

    with result_col2:
        st.write(f"**Match Score:** {latest['Match Score']}")
        st.write(f"**Priority:** {latest['Priority']}")
        st.write(f"**Pickup:** {latest['Pickup']}")
        st.write(f"**Delivery Target:** {latest['Delivery Target']}")
else:
    st.info("Click 'Load Biryani Demo' to restore the demonstration.")

st.markdown("---")
st.warning(
    "Food safety reminder: this dashboard is a prototype. Real food donations "
    "should be verified by responsible human staff before distribution."
)
st.caption(
    "EcoWaste AI — Member 5 Demo Dashboard | "
    "All displayed organizations and statistics are fictional."
)
