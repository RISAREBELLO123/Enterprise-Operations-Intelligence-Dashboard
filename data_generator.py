import pandas as pd
import numpy as np
import os
from datetime import datetime, timedelta

def generate_data(num_rows=55000):
    np.random.seed(42)
    
    # 1. Timeline: Last 2 years
    end_date = datetime.now()
    start_date = end_date - timedelta(days=730)
    dates = pd.date_range(start=start_date, end=end_date, periods=num_rows)
    
    # 2. Categorical Data
    regions = ['North America', 'EMEA', 'APAC', 'LATAM']
    categories = ['Electronics', 'Industrial', 'Office Supplies', 'Logistics Services']
    channels = ['Direct Sales', 'Partner', 'Online Portal', 'Enterprise Contract']
    statuses = ['Delivered', 'Pending', 'Shipped', 'Cancelled', 'On Hold']
    
    # 3. Base Numerical Data
    units_sold = np.random.randint(1, 500, size=num_rows)
    unit_price = np.random.uniform(50.0, 5000.0, size=num_rows).round(2)
    costs = (unit_price * 0.7 * np.random.uniform(0.8, 1.2, size=num_rows)).round(2)
    revenue = (units_sold * unit_price).round(2)
    profit = (revenue - (units_sold * costs)).round(2)
    
    # 4. Operational Delays (Target for Anomaly/Risk)
    # Most orders have 1-5 days delay, some have much more
    base_delays = np.random.exponential(scale=2, size=num_rows).astype(int)
    # Add anomalies: 2% of data has massive delays
    anomaly_mask = np.random.random(num_rows) < 0.02
    base_delays[anomaly_mask] = np.random.randint(15, 60, size=anomaly_mask.sum())
    
    # 5. Customer Complaints/Sentiment
    complaint_score = np.random.choice([0, 1, 2, 3, 4, 5], p=[0.7, 0.1, 0.08, 0.05, 0.04, 0.03], size=num_rows)
    
    # Create DataFrame
    df = pd.DataFrame({
        'Order_ID': [f'ORD-{i:06d}' for i in range(num_rows)],
        'Date': dates,
        'Region': np.random.choice(regions, size=num_rows),
        'Category': np.random.choice(categories, size=num_rows),
        'Sales_Channel': np.random.choice(channels, size=num_rows),
        'Units_Sold': units_sold,
        'Unit_Price': unit_price,
        'Unit_Cost': costs,
        'Total_Revenue': revenue,
        'Total_Profit': profit,
        'Operational_Delay_Days': base_delays,
        'Status': np.random.choice(statuses, p=[0.7, 0.1, 0.1, 0.05, 0.05], size=num_rows),
        'Customer_Complaint_Score': complaint_score
    })
    
    # Introduce intentional Data Quality Issues for the "Cleansing" step
    # Add some nulls
    null_indices = np.random.choice(num_rows, size=500, replace=False)
    df.loc[null_indices, 'Region'] = np.nan
    
    # Add some duplicate IDs
    dup_indices = np.random.choice(num_rows, size=100, replace=False)
    df_dups = df.iloc[dup_indices].copy()
    df = pd.concat([df, df_dups], ignore_index=True)
    
    # Save to CSV
    output_path = '/Users/risarajeshrebello/.gemini/antigravity/scratch/enterprise-ops-intelligence/data/raw_operational_data.csv'
    df.to_csv(output_path, index=False)
    print(f"Generated {len(df)} rows of data at {output_path}")

if __name__ == "__main__":
    generate_data()
