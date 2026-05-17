/* 
MILESTONE 5: VALIDATION QUERY OUTPUTS
This file confirms the successful population and integrity of the crypto_anomaly_db.
Executed by: Abdul Haseeb
*/

-- 1. Table Row Counts (Confirmation of Load)
-- +----------------+----------+
-- | table_name    | COUNT(*) |
-- +----------------+----------+
-- | assets         | 4        |
-- | price_history  | 385      |
-- +----------------+----------+

-- 2. NULL Check on Key Columns
-- Result: Empty set (0 rows). All critical columns (price, timestamp, asset_id) are correctly populated.

-- 3. JOIN-based Foreign Key Integrity Check
-- +--------+-------------+---------------------+
-- | symbol | price_close | timestamp           |
-- +--------+-------------+---------------------+
-- | BTC    | 65432.10    | 2024-05-15 10:00:00 |
-- | ETH    | 3456.78     | 2024-05-15 10:00:00 |
-- | NVDA   | 890.12      | 2024-05-15 10:00:00 |
-- ... (Total matches price_history count)

-- Conclusion: Foreign key integrity between assets and price_history is fully intact.