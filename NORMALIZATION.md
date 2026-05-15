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
