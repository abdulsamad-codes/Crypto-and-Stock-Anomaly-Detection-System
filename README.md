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

## Project Structure

- **/app**: Python Flask application (Server, Static, Templates)
- **/database**: SQL Scripts (Schema, Population) and Data Exports
- **/docs**: ERDs, Project Reports, and Lab Manual Implementations
- **/php_module**: Classic PHP/MySQL CRUD integration for Teacher Verification
- **/tools**: Data generation and processing utilities

## Setup Instructions
1. Clone the repository.
2. Run `database/schema.sql` and `database/population.sql` in MySQL Workbench.
3. Install dependencies: `pip install -r requirements.txt`.
4. Update database credentials in `app/app.py`.
5. Run the dashboard: `python app/app.py`.

### XAMPP Usage (PHP)
To use the PHP module:
1. Copy the `php_module` folder into your `C:\xampp\htdocs\`.
2. Start Apache and MySQL in XAMPP.
3. Access at `http://localhost/php_module/index.php`.
4. If your MySQL has no password, update `php_module/insert.php` to use `""`.
