-- 1. Create Database
DROP DATABASE IF EXISTS crypto_anomaly_db;

CREATE DATABASE crypto_anomaly_db;

USE crypto_anomaly_db;

-- 2. Tables
CREATE TABLE assets (
    asset_id INT PRIMARY KEY,
    symbol VARCHAR(10) UNIQUE,
    name VARCHAR(50),
    asset_type VARCHAR(20)
);

CREATE TABLE users (
    user_id INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(50) UNIQUE,
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
    FOREIGN KEY (user_id) REFERENCES users (user_id)
);

CREATE TABLE price_history (
    price_id INT PRIMARY KEY AUTO_INCREMENT,
    asset_id INT NOT NULL,
    timestamp DATETIME NOT NULL,
    price_close DECIMAL(10, 2) NOT NULL,
    volume DECIMAL(15, 2),
    FOREIGN KEY (asset_id) REFERENCES assets (asset_id),
    INDEX (timestamp),
    INDEX (asset_id)
);

CREATE TABLE anomalies (
    anomaly_id INT PRIMARY KEY AUTO_INCREMENT,
    asset_id INT NOT NULL,
    price_id INT NOT NULL,
    score FLOAT NOT NULL,
    severity VARCHAR(10),
    FOREIGN KEY (asset_id) REFERENCES assets (asset_id),
    FOREIGN KEY (price_id) REFERENCES price_history (price_id),
    INDEX (severity)
);

CREATE TABLE alerts (
    alert_id INT PRIMARY KEY AUTO_INCREMENT,
    anomaly_id INT,
    alert_message VARCHAR(255),
    FOREIGN KEY (anomaly_id) REFERENCES anomalies (anomaly_id)
);

CREATE TABLE user_feedback (
    feedback_id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL,
    message TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 3. Views
CREATE VIEW view_asset_report AS
SELECT a.symbol, a.name, p.price_close, p.timestamp
FROM assets a
    JOIN price_history p ON a.asset_id = p.asset_id;

CREATE VIEW view_anomaly_count AS
SELECT asset_id, COUNT(*) as total_found
FROM anomalies
GROUP BY
    asset_id;