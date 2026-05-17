-- Milestone 5: Data Population (DML)
-- Project: Crypto & Stock Anomaly Detection System
-- Prepared by: Abdul Haseeb

-- 1. Use the correct database
USE crypto_anomaly_db;

-- 2. Bulk Load Data (Milestone 5 Requirement)
-- Note: Replace 'E:/path/to/' with your actual absolute path if running in MySQL Workbench
-- We are loading the real-time data generated in Milestone 3

-- Load Assets
LOAD DATA INFILE 'E:/Study Material/4th Semester All Data/Sir Ali Hassan (Database Systems (Lab))/Crypto-and-Stock-Anomaly-Detection-System/data_exports/assets.csv' INTO
TABLE assets FIELDS TERMINATED BY ',' ENCLOSED BY '"' LINES TERMINATED BY '\r\n' IGNORE 1 ROWS;

-- Load Price History
LOAD DATA INFILE 'E:/Study Material/4th Semester All Data/Sir Ali Hassan (Database Systems (Lab))/Crypto-and-Stock-Anomaly-Detection-System/data_exports/price_history.csv' INTO
TABLE price_history FIELDS TERMINATED BY ',' ENCLOSED BY '"' LINES TERMINATED BY '\r\n' IGNORE 1 ROWS (
    timestamp,
    price_close,
    volume,
    asset_id
);

-- 3. Required DML Operations
-- UPDATE operation with a WHERE condition
UPDATE assets SET name = 'Bitcoin (BTC)' WHERE symbol = 'BTC';

-- DELETE operation with a WHERE condition
-- (Deleting a dummy price record or a test row)
DELETE FROM price_history WHERE volume < 0;

-- 4. Validation Queries (Teacher's Requirements)
-- Confirm row counts for each table
SELECT 'assets' as table_name, COUNT(*)
FROM assets
UNION ALL
SELECT 'price_history', COUNT(*)
FROM price_history;

-- NULL check on key columns
SELECT *
FROM price_history
WHERE
    price_close IS NULL
    OR timestamp IS NULL;

-- JOIN-based check to confirm foreign key integrity
SELECT a.symbol, p.price_close, p.timestamp
FROM assets a
    JOIN price_history p ON a.asset_id = p.asset_id
LIMIT 10;