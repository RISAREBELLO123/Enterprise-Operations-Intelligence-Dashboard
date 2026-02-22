import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import sqlite3
from queries import get_connection, get_all_data, get_forecast_data, get_high_risk_transactions, get_category_performance

# Page config
st.set_page_config(page_title="Ops Intelligence Dashboard", layout="wide", initial_sidebar_state="expanded")

# Custom CSS for Premium "Claude Analytics" Look
st.markdown("""
    <style>
    /* Main background */
    .stApp {
        background-color: #0d1117;
        color: #c9d1d9;
    }
    
    /* Sidebar */
    [data-testid="stSidebar"] {
        background-color: #010409;
        border-right: 1px solid #30363d;
    }
    
    /* Cards */
    .metric-card {
        background-color: #161b22;
        padding: 20px;
        border-radius: 8px;
        border: 1px solid #30363d;
        margin-bottom: 20px;
    }
    
    .metric-title {
        color: #8b949e;
        font-size: 0.85rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.05rem;
        margin-bottom: 10px;
    }
    
    .metric-value {
        color: #f0f6fc;
        font-size: 1.8rem;
        font-weight: 700;
        margin-bottom: 5px;
    }
    
    .metric-delta {
        font-size: 0.85rem;
        font-weight: 500;
    }
    
    .delta-up { color: #3fb950; }
    .delta-down { color: #f85149; }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        background-color: transparent;
        border-bottom: 1px solid #30363d;
    }
    
    .stTabs [data-baseweb="tab"] {
        color: #8b949e;
        font-weight: 500;
    }
    
    .stTabs [aria-selected="true"] {
        color: #58a6ff !important;
        border-bottom-color: #58a6ff !important;
    }

    h1, h2, h3 {
        color: #f0f6fc;
        font-family: 'Inter', sans-serif;
    }
    
    .status-indicator {
        display: inline-block;
        width: 8px;
        height: 8px;
        border-radius: 50%;
        background-color: #3fb950;
        margin-right: 8px;
    }
    </style>
    """, unsafe_allow_html=True)

@st.cache_data
def load_data_from_sql():
    conn = get_connection()
    df = get_all_data(conn)
    df['Date'] = pd.to_datetime(df['Date'])
    forecast_df = get_forecast_data(conn)
    forecast_df['Date'] = pd.to_datetime(forecast_df['Date'])
    conn.close()
    return df, forecast_df

try:
    df, forecast_df = load_data_from_sql()
except Exception as e:
    st.error(f"Error connecting to database: {e}")
    st.stop()

# Sidebar
st.sidebar.markdown("### Operations Control")
st.sidebar.markdown("---")
region_filter = st.sidebar.multiselect("Select Region", options=df['Region'].unique(), default=df['Region'].unique())
category_filter = st.sidebar.multiselect("Select Category", options=df['Category'].unique(), default=df['Category'].unique())

filtered_df = df[(df['Region'].isin(region_filter)) & (df['Category'].isin(category_filter))]

# Header
st.markdown(f"<h1><span class='status-indicator'></span>Enterprise Operations Intelligence Dashboard</h1>", unsafe_allow_html=True)
st.markdown("<p style='color: #8b949e; margin-top: -15px;'>Real-time monitoring and analytics for enterprise logistics</p>", unsafe_allow_html=True)

# Row 1: Key Metrics (Custom HTML for Claude Style)
def metric_block(label, value, delta, is_up=True):
    delta_class = "delta-up" if is_up else "delta-down"
    delta_prefix = "+" if is_up else ""
    return f"""
    <div class="metric-card">
        <div class="metric-title">{label}</div>
        <div class="metric-value">{value}</div>
        <div class="metric-delta {delta_class}">{delta_prefix}{delta}</div>
    </div>
    """

c1, c2, c3, c4 = st.columns(4)
total_revenue = filtered_df['Total_Revenue'].sum()
total_profit = filtered_df['Total_Profit'].sum()
avg_delay = filtered_df['Operational_Delay_Days'].mean()
risk_count = len(filtered_df[filtered_df['Risk_Score'] == 'High Risk'])

with c1: st.markdown(metric_block("Total Revenue", f"${total_revenue/1e6:.1f}M", "5.2%", True), unsafe_allow_html=True)
with c2: st.markdown(metric_block("Net Profit", f"${total_profit/1e6:.1f}M", "3.1%", True), unsafe_allow_html=True)
with c3: st.markdown(metric_block("Avg Delay (Days)", f"{avg_delay:.1f}d", "-0.5d", False), unsafe_allow_html=True)
with c4: st.markdown(metric_block("Risk Alerts", f"{risk_count}", f"{(risk_count/len(filtered_df)*100):.1f}%", False), unsafe_allow_html=True)

# Tabs
tab1, tab2, tab3 = st.tabs(["Executive Summary", "Operations Deep-Dive", "Predictive Insights"])

with tab1:
    st.markdown("### Revenue Trends")
    ts_rev = filtered_df.set_index('Date')['Total_Revenue'].resample('M').sum().reset_index()
    fig_rev = px.line(ts_rev, x='Date', y='Total_Revenue', template="plotly_dark", color_discrete_sequence=['#58a6ff'])
    fig_rev.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', margin=dict(t=20, b=20, l=0, r=0))
    st.plotly_chart(fig_rev, use_container_width=True)
    
    col_x, col_y = st.columns(2)
    with col_x:
        fig_reg = px.pie(filtered_df, values='Total_Revenue', names='Region', hole=0.5, template="plotly_dark", color_discrete_sequence=px.colors.qualitative.Pastel)
        fig_reg.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig_reg, use_container_width=True)
    with col_y:
        conn = get_connection()
        cat_perf = get_category_performance(conn)
        conn.close()
        fig_cat = px.bar(cat_perf, x='Category', y='total_profit', template="plotly_dark", color_discrete_sequence=['#58a6ff'])
        fig_cat.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig_cat, use_container_width=True)

with tab2:
    st.markdown("### Efficiency Analysis")
    col_a, col_b = st.columns([2, 1])
    
    with col_a:
        fig_delay = px.histogram(filtered_df, x='Operational_Delay_Days', color='Status', barmode='overlay', template="plotly_dark")
        fig_delay.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig_delay, use_container_width=True)
        
    with col_b:
        st.markdown("**High Risk Records**")
        conn = get_connection()
        risk_table = get_high_risk_transactions(conn, limit=12)
        conn.close()
        st.dataframe(risk_table[['Order_ID', 'Region', 'Operational_Delay_Days']], use_container_width=True)

with tab3:
    st.markdown("### Forecast Modeling")
    actual_last_year = df.set_index('Date')['Total_Revenue'].resample('W').sum().tail(52).reset_index()
    actual_last_year['Type'] = 'Actual'
    forecast_df['Type'] = 'Forecast'
    combined = pd.concat([actual_last_year, forecast_df.rename(columns={'Forecasted_Revenue': 'Total_Revenue'})])
    
    fig_forecast = px.line(combined, x='Date', y='Total_Revenue', color='Type', template="plotly_dark", color_discrete_map={'Actual': '#58a6ff', 'Forecast': '#d18c3c'})
    fig_forecast.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig_forecast, use_container_width=True)
    
    st.markdown("<div style='background-color: #161b22; padding: 15px; border-radius: 8px; border: 1px solid #30363d;'><span style='color: #d18c3c; font-weight: bold;'>Insight:</span> APAC growth trend remains strong, however anomaly detection alerts have increased in the EMEA logistics corridor.</div>", unsafe_allow_html=True)

st.markdown("---")
st.markdown("<p style='text-align: center; color: #8b949e; font-size: 0.8rem;'>Operations Intelligence Framework v1.0 | Senior Associate Dashboard</p>", unsafe_allow_html=True)
