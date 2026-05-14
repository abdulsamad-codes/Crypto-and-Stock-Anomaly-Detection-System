-- 1. Create Database
CREATE DATABASE IF NOT EXISTS crypto_anomaly_db;
USE crypto_anomaly_db;

-- 2. Tables
CREATE TABLE assets (
    asset_id INT PRIMARY KEY,
    symbol VARCHAR(10),
    name VARCHAR(50),
    asset_type VARCHAR(20)
);

CREATE TABLE users (
    user_id INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(50),
    password VARCHAR(50),
    role VARCHAR(20)
);

CREATE TABLE model_logs (
    log_id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT,
    run_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    model_version VARCHAR(20),
    records_scanned INT,
    anomalies_found INT,
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);

CREATE TABLE price_history (
    price_id INT PRIMARY KEY AUTO_INCREMENT,
    asset_id INT,
    timestamp DATETIME,
    price_close DECIMAL(10, 2),
    volume DECIMAL(15, 2),
    FOREIGN KEY (asset_id) REFERENCES assets(asset_id)
);

CREATE TABLE anomalies (
    anomaly_id INT PRIMARY KEY AUTO_INCREMENT,
    asset_id INT,
    price_id INT,
    score FLOAT,
    severity VARCHAR(10),
    FOREIGN KEY (asset_id) REFERENCES assets(asset_id),
    FOREIGN KEY (price_id) REFERENCES price_history(price_id)
);

CREATE TABLE alerts (
    alert_id INT PRIMARY KEY AUTO_INCREMENT,
    anomaly_id INT,
    alert_message VARCHAR(255),
    FOREIGN KEY (anomaly_id) REFERENCES anomalies(anomaly_id)
);

-- 3. Views
CREATE VIEW view_asset_report AS
SELECT a.symbol, a.name, p.price_close, p.timestamp
FROM assets a
JOIN price_history p ON a.asset_id = p.asset_id;

CREATE VIEW view_anomaly_count AS
SELECT asset_id, COUNT(*) as total_found
FROM anomalies
GROUP BY asset_id;