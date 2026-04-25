# Crypto & Stock Anomaly Detection System

## Project Overview
This project is a final-year Database Systems Lab initiative. It provides an automated solution for detecting financial market anomalies (flash crashes, price spikes, volume surges) using an Isolation Forest machine learning model integrated with a robust MySQL relational database.

## Team
- Abdul Samad
- Abdul Haseeb

## Key Features
- **Normalized MySQL Schema:** Designed for data integrity and ACID compliance.
- **ML-Database Integration:** Python-based pipeline that reads OHLCV data from MySQL, processes anomalies, and persists results back to the database.
- **Automated Alerts:** Triggers and stored procedures for real-time anomaly flagging.
- **Flask Dashboard:** Visualizes market data with Chart.js and manages user sessions.

## Setup Instructions
1. Clone the repository.
2. Run `database/schema.sql` in MySQL Workbench.
3. Install dependencies: `pip install -r requirements.txt`.
4. Configure database credentials in `config.py`.
