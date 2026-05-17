from flask import Flask, render_template, jsonify
import mysql.connector
import pandas as pd

app = Flask(__name__)

# Database Configuration
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'AAdd541@$', # User will need to update this
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
        
        # Get system stats for the top cards
        cursor.execute("SELECT COUNT(*) as count FROM assets")
        asset_count = cursor.fetchone()['count']
        
        cursor.execute("SELECT COUNT(*) as count FROM price_history")
        row_count = cursor.fetchone()['count']
        
        cursor.execute("SELECT COUNT(*) as count FROM anomalies")
        anomaly_count = cursor.fetchone()['count']

        cursor.execute("SELECT * FROM assets")
        assets = cursor.fetchall()
        
        # Fetch recent alerts securely
        cursor.execute("SELECT * FROM alerts ORDER BY alert_id DESC LIMIT 5")
        alerts = cursor.fetchall()
        
        cursor.close()
        return render_template('index.html', 
                             assets=assets, 
                             alerts=alerts, 
                             stats={
                                 'assets': asset_count,
                                 'rows': row_count,
                                 'anomalies': anomaly_count
                             })
    except mysql.connector.Error as err:
        return f"Database Error: {err}. Please ensure your password is correct in app.py.", 500
    finally:
        if conn and conn.is_connected():
            conn.close()

@app.route('/api/stats/<int:asset_id>')
def get_asset_stats(asset_id):
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        # Fetch high, low, and average price for insight
        query = """
            SELECT 
                MAX(price_close) as max_p, 
                MIN(price_close) as min_p, 
                AVG(price_close) as avg_p,
                COUNT(*) as readings
            FROM price_history 
            WHERE asset_id = %s
        """
        cursor.execute(query, (asset_id,))
        stats = cursor.fetchone()
        cursor.close()
        return jsonify(stats)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
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
