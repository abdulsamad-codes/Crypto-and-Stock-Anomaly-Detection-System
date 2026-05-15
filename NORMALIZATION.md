# Database Normalization Report - Milestone 2

## Project: Crypto & Stock Anomaly Detection System

**Developed by:** Abdul Samad & Abdul Haseeb

In this phase, we reviewed our database schema to ensure it follows standard normalization rules (1NF, 2NF, and 3NF). The goal was to remove any potential data redundancy and make sure our tables are logically structured for the anomaly detection system.

---

### 1. First Normal Form (1NF)

**Goal:** Each column should contain atomic values, and there should be no repeating groups.

After looking at our tables like `assets`, `users`, and `price_history`, we confirmed that:

- Every field contains only single values (e.g., a single symbol like 'BTC' or a single price value).
- There are no comma-separated lists or multiple values tucked into a single column.
- We have defined Primary Keys for every table to uniquely identify each row.

**Conclusion:** Our schema is already in 1NF. No major restructuring was needed here because we planned the basic attributes carefully from the start.

---

### 2. Second Normal Form (2NF)

**Goal:** Must be in 1NF and all non-key attributes must be fully dependent on the Primary Key.

In this step, we checked for "Partial Dependencies." This usually happens when a table has a composite primary key, and some columns only depend on part of that key.

- **Analysis:** Our tables mostly use single-column surrogate keys (like `price_id`, `asset_id`, `anomaly_id`).
- **Observation:** In the `price_history` table, the columns `price_close` and `volume` are tied to a specific point in time for a specific asset. By using `price_id` as a unique primary key, we ensure that every price and volume record is fully dependent on that unique ID.
- **Redundancy check:** We made sure not to store asset details like `asset_name` inside the `price_history` table. Instead, we just use the `asset_id` to link them.

**Conclusion:** Since all non-key columns depend entirely on their respective Primary Keys, the schema satisfies 2NF.

---

### 3. Third Normal Form (3NF)

**Goal:** Must be in 2NF and have no transitive dependencies (non-key columns depending on other non-key columns).

This was the most important check for our system. We looked for attributes that might depend on each other instead of the Primary Key.

- **Case Study (Anomalies Table):** We store `score` and `severity`. One might argue that `severity` depends on the `score` (e.g., if score > 0.8, severity is 'High').
- **Justification:** While the logic is derived, we decided to store `severity` as a static value for fast reporting on the dashboard without needing to recalculate the ML logic in the database every time.
- **Asset Table:** We kept `asset_type` (Crypto vs Stock) in the `assets` table. We checked if we needed a separate `asset_types` table, but since we only have two categories, we decided to keep it simple as a VARCHAR to avoid unnecessary joins.

---

### Recent Schema Updates

During the normalization review for Milestone 2, we identified a few areas where candidate keys were not properly constrained:

- **Unique Constraints:** We added `UNIQUE` constraints to `assets.symbol` and `users.username`. This prevents 1NF violations where duplicate logical records could exist under different Primary Keys.
- **Constraint Enforcement:** By adding these to [schema.sql](schema.sql), we ensure the database physically enforces the rules we defined in our logical design.
