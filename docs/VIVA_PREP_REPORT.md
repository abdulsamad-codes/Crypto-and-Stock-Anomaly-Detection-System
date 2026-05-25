# VIVA PREPARATION & TECHNICAL PROJECT REPORT
## Project: Crypto & Stock Anomaly Detection System (Cyber-Themed)

This report is designed to help you ace your Viva by explaining the "Why" and "How" of every part of your project, focusing heavily on Database Logic, Backend Workflow, and the Teacher's specific requirements.

---

## 1. THE DATABASE CORE (The #1 Viva Topic)
Sir Ali Hassan will likely focus on your schema and how data flows.

### A. Schema Architecture (3NF Normalization)
*   **Assets Table:** Stores metadata about coins/stocks. (`asset_id` is PK).
*   **Price History Table:** Large-scale time-series data. Linked to Assets via `asset_id` (FK).
*   **Anomalies Table:** Results from the ML model are stored here. It identifies *which* asset had *what* problem.
*   **Alerts Table:** This is the "Notification" layer. It triggers when an anomaly is confirmed.
*   **User Feedback Table (The PHP Part):** Added specifically to show CRUD operations via PHP, linking traditional lab work with modern systems.

### B. Logic & Constraints
*   **Primary Keys (PK):** Ensure every table has a unique ID for integrity.
*   **Foreign Keys (FK):** Maintain "Referential Integrity"—you can't have a price for an asset that doesn't exist.
*   **Cascading:** If an asset is deleted, its price history is automatically purged (ON DELETE CASCADE).

### C. Advanced SQL used
*   **Stored Procedures:** Look at `database/schema.sql`. We used these to automate "Risk Calculations" and "Data Cleanup."
*   **Triggers:** Mention that we can trigger an alert the moment a price drops by more than $X amount automatically at the DB level.

---

## 2. THE BACKEND WORKFLOW (Python/Flask)
He will ask: *"How does the code talk to the database?"*

*   **MySQL Connector:** used in `app/app.py`. We use `cursor.execute(SQL_QUERY)` to fetch data.
*   **Hybrid Logic (Vercel vs Local):** 
    *   *Question:* "Why does your Vercel link work without MySQL?"
    *   *Answer:* I implemented an `IS_VERCEL` check. If true, it uses **Mock Data** (Simulated data) so the UI doesn't crash. If false (Local), it connects to the actual MySQL DB.
*   **Dynamic Routing:** The `@app.route('/analysis/<int:asset_id>')` uses a variable in the URL to fetch data for a *specific* asset from the DB.

---

## 3. THE LAB MANUAL COMPLIANCE (The PHP Module)
Since the teacher specifically asked for `index.php` and `insert.php`:

*   **The Workflow:** 
    1.  User enters feedback in a standard HTML form (`index.php`).
    2.  Data is sent via `POST` method to `insert.php`.
    3.  `insert.php` uses `mysqli_connect` and `mysqli_query` (Procedural PHP) to save it.
*   **Why PHP?** Explain that we used PHP for the "Administrative/Feedback" side to demonstrate mastery of the traditional stack he taught in the lab.

---

## 4. THE AI/LOGIC COMPONENT
*   **Isolation Forest:** We used this algorithm because it is "Unsupervised." It doesn't need to be told what an anomaly looks like; it finds "outliers" (data points that look lonely or weird) automatically.
*   **Z-Score:** We use statistical math to find price spikes that are too many standard deviations from the average.

---

## 5. TOP 10 VIVA "GOTCHA" QUESTIONS
1.  **"Can your system handle real-time data?"** 
    *   Yes, the `data_generator.py` simulates real-time ingestion, and the dashboard uses Chart.js to visualize it.
2.  **"Why did you use 3NF instead of 2NF?"**
    *   To eliminate transitive dependencies and ensure we never have "Update Anomalies."
3.  **"What is the role of `vercel.json`?"**
    *   It tells the cloud provider (Vercel) how to build our Python application and where the main "Entry Point" (`app/app.py`) is.
4.  **"Explain the connection between your ERD and your Schema."**
    *   The ERD is the blueprint; the `schema.sql` is the actual construction. Every diamond in the ERD is a relationship handled by a Foreign Key.
5.  **"How do you prevent SQL Injection?"**
    *   By using *Parameterized Queries* (e.g., `cursor.execute(query, (params,))`) instead of f-strings.

---

## 6. PROJECT FOLDER NAVIGATION GUIDE
If he asks you to open a specific part of the code:
*   **DB Logic:** `database/schema.sql`
*   **Flask Control:** `app/app.py`
*   **Premium Visuals:** `app/templates/dashboard.html`
*   **Traditional PHP:** `php_module/index.php`
*   **ERD/Reports:** `docs/`

---
**LEARNING TIP:** Spend 15 minutes reading the **[docs/TEACHER_GUIDE_IMPLEMENTATION.md](docs/TEACHER_GUIDE_IMPLEMENTATION.md)** file I made. It maps our project directly to his lab roadmaps!
