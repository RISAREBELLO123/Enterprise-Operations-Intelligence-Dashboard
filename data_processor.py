import pandas as pd
import numpy as np
import os
from datetime import datetime

def clean_and_validate(input_path, output_path):
    print(f"Loading data from {input_path}...")
    df = pd.read_csv(input_path)
    initial_count = len(df)
    
    # 1. Data Cleaning
    print("Performing data cleansing...")
    
    # Remove duplicates
    df = df.drop_duplicates(subset=['Order_ID'], keep='first')
    dup_removed = initial_count - len(df)
    
    # Handle missing values
    # For 'Region', we'll fill with 'Unknown' (or we could use mode)
    df['Region'] = df['Region'].fillna('Unknown')
    
    # Standardize types
    df['Date'] = pd.to_datetime(df['Date'])
    
    # 2. Data Validation (Business Rules)
    print("Validating business rules...")
    
    # Rule 1: Revenue must be positive (except perhaps for returns, but here we assume sales)
    # If revenue is <= 0 and Status is Delivered, that's a data quality issue
    revenue_check = (df['Total_Revenue'] <= 0) & (df['Status'] == 'Delivered')
    df.loc[revenue_check, 'Total_Revenue'] = df['Units_Sold'] * df['Unit_Price']
    
    # Rule 2: Profit margin check
    # Ensure profit is consistent with Revenue - Cost
    df['Total_Profit'] = (df['Total_Revenue'] - (df['Units_Sold'] * df['Unit_Cost'])).round(2)
    
    # Rule 3: Delay days cannot be negative
    df['Operational_Delay_Days'] = df['Operational_Delay_Days'].clip(lower=0)
    
    # 3. Feature Engineering
    print("Feature engineering...")
    df['Month'] = df['Date'].dt.month
    df['Year'] = df['Date'].dt.year
    df['Day_of_Week'] = df['Date'].dt.day_name()
    df['Late_Delivery'] = df['Operational_Delay_Days'] > 5
    
    # Save cleaned data
    df.to_csv(output_path, index=False)
    
    print("\n--- Data Operations Report ---")
    print(f"Initial Records: {initial_count}")
    print(f"Duplicates Removed: {dup_removed}")
    print(f"Cleaned Records: {len(df)}")
    print(f"Data Integrity Check: {'PASSED' if df.isnull().sum().sum() == 0 else 'FAILED'}")
    print(f"Processed file saved to: {output_path}")

if __name__ == "__main__":
    raw_data = 'data/raw_operational_data.csv'
    processed_data = 'data/processed_operational_data.csv'
    clean_and_validate(raw_data, processed_data)
