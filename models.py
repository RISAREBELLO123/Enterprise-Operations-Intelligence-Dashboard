import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest
from statsmodels.tsa.holtwinters import ExponentialSmoothing
import joblib
import os

def run_predictive_models(input_path, model_dir='models'):
    if not os.path.exists(model_dir):
        os.makedirs(model_dir)
        
    df = pd.read_csv(input_path)
    df['Date'] = pd.to_datetime(df['Date'])
    
    # 1. Anomaly Detection (Operational Risk)
    print("Running Anomaly Detection (Isolation Forest)...")
    # Features for risk: Delay Days, Complaint Score, Profit Margin
    df['Profit_Margin'] = df['Total_Profit'] / df['Total_Revenue']
    features = ['Operational_Delay_Days', 'Customer_Complaint_Score', 'Profit_Margin']
    
    # Handle any inf values from division by zero
    df_model = df[features].replace([np.inf, -np.inf], 0).fillna(0)
    
    iso_forest = IsolationForest(contamination=0.02, random_state=42)
    df['Is_Anomaly'] = iso_forest.fit_predict(df_model)
    # -1 is anomaly, 1 is normal
    df['Risk_Score'] = np.where(df['Is_Anomaly'] == -1, 'High Risk', 'Normal')
    
    # 2. Revenue Forecasting (Last 3 Months)
    print("Generating Revenue Forecast...")
    # Group by week for smoother trend
    ts_data = df.set_index('Date')['Total_Revenue'].resample('W').sum()
    
    # Simple Exponential Smoothing (Holt-Winters)
    model = ExponentialSmoothing(ts_data, trend='add', seasonal='add', seasonal_periods=52).fit()
    forecast = model.forecast(12) # 12 weeks (3 months)
    
    # Save results back to the dataframe for dashboard use
    # Note: We'll save the forecast separately as it has a future index
    forecast_df = pd.DataFrame({'Date': forecast.index, 'Forecasted_Revenue': forecast.values})
    
    # Save the processed data with Anomaly flags
    df.to_csv('data/final_operational_data.csv', index=False)
    forecast_df.to_csv('data/revenue_forecast.csv', index=False)
    
    print("Predictive models completed.")
    print(f"Anomalies detected: {len(df[df['Is_Anomaly'] == -1])}")

if __name__ == "__main__":
    run_predictive_models('data/processed_operational_data.csv')
