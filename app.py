import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta

# --- 1. APP CONFIGURATION ---
st.set_page_config(
    page_title="Adams Inn Fitness & Gym Centre", 
    page_icon="🏋️‍♂️", 
    layout="wide"
)

# Branding CSS
st.markdown("""
    <style>
    .main { background-color: #1a1a1a; }
    [data-testid="stMetricValue"] { color: #d4ff00; }
    div.stButton > button { width: 100%; border-radius: 5px; background-color: #d4ff00; color: black; font-weight: bold; border: none; }
    h1, h2, h3 { color: #d4ff00; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. DATABASE INITIALIZATION ---
# Using Session State to keep data alive while the app is open
if 'members' not in st.session_state:
    st.session_state.members = pd.DataFrame([
        {"Name": "John Adams", "Phone": "+233000000000", "Plan": "Pro ($50)", "Next Payment": "2026-03-15", "Status": "Active"}
    ])

if 'sales_total' not in st.session_state:
    st.session_state.sales_total = 0.0

# --- 3. HEADER ---
st.title("🏋️‍♂️ Adams Inn Fitness and Gym Centre")
st.write(f"Logged in as Admin | {datetime.now().strftime('%A, %d %B %Y')}")

# --- 4. DASHBOARD METRICS ---
m_revenue = sum([int(p.split('$')[1].replace(')', '')) for p in st.session_state.members['Plan']])
total_income = m_revenue + st.session_state.sales_total

col1, col2, col3 = st.columns(3)
col1.metric("Active Members", len(st.session_state.members))
col2.metric("Membership Rev.", f"${m_revenue}")
col3.metric("Daily Shop Sales", f"${st.session_state.sales_total}")

# --- 5. VISUAL ANALYTICS ---
st.subheader("📊 Business Intelligence")
chart_col1, chart_col2 = st.columns([2, 1])

with chart_col1:
    # Revenue Chart
    fig = px.bar(
        x=["Memberships", "Shop Sales"], 
        y=[m_revenue, st.session_state.sales_total],
        title="Revenue Split",
        color_discrete_sequence=['#d4ff00']
    )
    fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color="white")
    st.plotly_chart(fig, use_container_width=True)

with chart_col2:
    # Member Distribution
    if not st.session_state.members.empty:
        fig_pie = px.pie(st.session_state.members, names='Plan', title="Plan Share", hole=0.3)
        fig_pie.update_layout(paper_bgcolor='rgba(0,0,0,0)', font_color="white")
        st.plotly_chart(fig_pie, use_container_width=True)

# --- 6. MEMBER MANAGEMENT ---
st.divider()
st.subheader("📋 Member Directory")

tab1, tab2 = st.tabs(["View Members", "Add New Member"])

with tab1:
    search = st.text_input("🔍 Search by name")
    df_display = st.session_state.members.copy()
    if search:
        df_display = df_display[df_display['Name'].str.contains(search, case=False)]
    
    st.dataframe(df_display, use_container_width=True)

with tab2:
    with st.form("add_member"):
        name = st.text_input("Member Name")
        phone = st.text_input("Phone Number")
        plan = st.selectbox("Plan", ["Basic ($20)", "Pro ($50)", "Elite ($100)"])
        if st.form_submit_button("Register"):
            due = (datetime.now() + timedelta(days=30)).strftime("%Y-%m-%d")
            new_data = {"Name": name, "Phone": phone, "Plan": plan, "Next Payment": due, "Status": "Active"}
            st.session_state.members = pd.concat([st.session_state.members, pd.DataFrame([new_data])], ignore_index=True)
            st.success(f"Added {name} successfully!")
            st.rerun()

# --- 7. SHOP ---
st.divider()
st.subheader("🥤 Shop Point of Sale")
s_col1, s_col2, s_col3 = st.columns(3)
with s_col1:
    if st.button("Water ($1)"): st.session_state.sales_total += 1.0
with s_col2:
    if st.button("Protein ($5)"): st.session_state.sales_total += 5.0
with s_col3:
    if st.button("Energy Drink ($3)"): st.session_state.sales_total += 3.0

# --- 8. FOOTER ---
st.markdown("---")
st.caption("Adams Inn Fitness and Gym Centre © 2026")
