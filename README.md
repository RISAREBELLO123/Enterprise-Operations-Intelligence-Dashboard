# 📊 Enterprise Operations Intelligence Dashboard

An end-to-end predictive analytics and monitoring system designed to bridge the gap between raw operational data and executive decision-making.

## 🚀 Features

This dashboard processes over **55,000+ operational records** to provide actionable business insights:

-   **📊 SQL Integration**: Engineered an automated data pipeline integrating SQLite for structured storage and SQL-based querying.
-   **📈 Revenue Forecasting**: Uses time-series models (Holt-Winters) to predict future revenue trends.
-   **⚠️ Risk Detection**: Implements Machine Learning (Isolation Forest) to automatically identify operational anomalies and high-risk transactions.
-   **💹 Real-time KPI Monitoring**: Interactive dashboard with dynamic filtering for regional performance, sales, and shipping efficiency.
-   **🧹 Automated Data Pipeline**: Robust data cleansing and validation engine ensuring high data integrity.

## 🛠️ Tech Stack

-   **Language**: Python
-   **Database**: SQLite | SQL
-   **Data Analysis**: Pandas, NumPy
-   **Machine Learning**: Scikit-Learn, Statsmodels
-   **Visualization**: Plotly, Streamlit

## 📂 Project Structure

-   `app.py`: Main Streamlit application file.
-   `database.py`: Script to initialize SQLite from CSV data.
-   `queries.py`: SQL helper functions for data analysis.
-   `data_generator.py`: Script to generate synthetic operational data.
-   `data_processor.py`: Data cleansing and feature engineering pipeline.
-   `models.py`: Implementation of forecasting and risk detection models.
-   `data/`: Directory containing CSV files and `operations.db`.

## 🚦 Getting Started

1.  **Install Dependencies**:
    ```bash
    pip install pandas numpy scikit-learn statsmodels plotly streamlit
    ```
2.  **Run the Dashboard**:
    ```bash
    streamlit run app.py
    ```

---
*Created for the Data Operations & Business Intelligence space.*
