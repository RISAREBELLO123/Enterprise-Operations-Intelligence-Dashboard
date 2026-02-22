import sqlite3
import pandas as pd
import os

def get_connection(db_path="data/operations.db"):
    return sqlite3.connect(db_path)

def get_regional_summary(conn):
    """Provides a high-level summary of revenue and volume by region."""
    query = """
        SELECT Region, 
               COUNT(*) as total_transactions,
               ROUND(SUM(Total_Revenue), 2) as total_revenue,
               ROUND(AVG(Total_Revenue), 2) as avg_revenue
        FROM operations
        GROUP BY Region
        ORDER BY total_revenue DESC
    """
    return pd.read_sql(query, conn)

def get_high_risk_transactions(conn, limit=100):
    """Retrieves transactions flagged as high risk by the anomaly detection model."""
    query = f"""
        SELECT Order_ID, Region, Category, Total_Revenue, Operational_Delay_Days, Risk_Score
        FROM operations
        WHERE Risk_Score = 'High Risk'
        ORDER BY Total_Revenue DESC
        LIMIT {limit}
    """
    return pd.read_sql(query, conn)

def get_category_performance(conn):
    """Analyzes profit performance across different product categories."""
    query = """
        SELECT Category, 
               SUM(Total_Profit) as total_profit
        FROM operations
        GROUP BY Category
        ORDER BY total_profit DESC
    """
    return pd.read_sql(query, conn)

def get_all_data(conn):
    """Fetches the entire operations table for general filtering."""
    return pd.read_sql("SELECT * FROM operations", conn)

def get_forecast_data(conn):
    """Fetches the revenue forecast data."""
    return pd.read_sql("SELECT * FROM forecast", conn)
