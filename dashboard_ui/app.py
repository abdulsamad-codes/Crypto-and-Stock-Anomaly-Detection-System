from flask import Flask, render_template, jsonify
import mysql.connector
import pandas as pd

app = Flask(__name__)

# Database Configuration
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'your_password', # User will need to update this
    'database': 'crypto_anomaly_db'
}

def get_db_connection():
    return mysql.connector.connect(**db_config)

@app.route('/')
def index():
    # Fetch assets for the sidebar/dropdown
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM assets")
        assets = cursor.fetchall()
        
        # Fetch recent alerts securely
        cursor.execute("SELECT * FROM alerts ORDER BY alert_id DESC LIMIT 5")
        alerts = cursor.fetchall()
        
        cursor.close()
        return render_template('index.html', assets=assets, alerts=alerts)
    except mysql.connector.Error as err:
        return f"Database Error: {err}. Please ensure your password is correct in app.py.", 500
    finally:
        if conn and conn.is_connected():
            conn.close()

@app.route('/api/prices/<int:asset_id>')
def get_prices(asset_id):
    conn = None
    try:
        conn = get_db_connection()
        query = "SELECT timestamp, price_close FROM price_history WHERE asset_id = %s ORDER BY timestamp ASC"
        df = pd.read_sql(query, conn, params=(asset_id,))
        
        # Format for Chart.js
        # Convert timestamp to string if it exists, else empty list
        labels = []
        values = []
        if not df.empty:
            labels = pd.to_datetime(df['timestamp']).dt.strftime('%Y-%m-%d %H:%M').tolist()
            values = df['price_close'].tolist()

        data = {
            'labels': labels,
            'values': values
        }
        return jsonify(data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        if conn and conn.is_connected():
            conn.close()

if __name__ == '__main__':
    app.run(debug=True)
