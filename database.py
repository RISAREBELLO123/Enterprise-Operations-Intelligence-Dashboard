import sqlite3
import pandas as pd
import os

def create_database(data_dir="data", db_name="operations.db"):
    db_path = os.path.join(data_dir, db_name)
    conn = sqlite3.connect(db_path)
    
    # Load main operational data
    ops_df = pd.read_csv(os.path.join(data_dir, 'final_operational_data.csv'))
    ops_df.to_sql("operations", conn, if_exists="replace", index=False)
    
    # Load forecast data
    forecast_df = pd.read_csv(os.path.join(data_dir, 'revenue_forecast.csv'))
    forecast_df.to_sql("forecast", conn, if_exists="replace", index=False)
    
    conn.close()
    print(f"Database created successfully at {db_path}.")

if __name__ == "__main__":
    create_database()
