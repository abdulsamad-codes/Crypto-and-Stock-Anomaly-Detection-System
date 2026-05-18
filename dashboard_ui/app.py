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
    # Page 1: Global Nerve Center
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        # Stats for Nerve Center
        cursor.execute("SELECT COUNT(*) as count FROM assets")
        asset_count = cursor.fetchone()['count']
        cursor.execute("SELECT COUNT(*) as count FROM price_history")
        row_count = cursor.fetchone()['count']
        cursor.execute("SELECT COUNT(*) as count FROM anomalies")
        anomaly_count = cursor.fetchone()['count']

        cursor.execute("SELECT * FROM assets")
        assets = cursor.fetchall()
        
        cursor.execute("SELECT * FROM alerts ORDER BY alert_id DESC LIMIT 10")
        alerts = cursor.fetchall()
        
        cursor.close()
        return render_template('dashboard.html', 
                             assets=assets, 
                             alerts=alerts, 
                             stats={'assets': asset_count, 'rows': row_count, 'anomalies': anomaly_count})
    except mysql.connector.Error as err:
        return f"Database Error: {err}", 500
    finally:
        if conn and conn.is_connected():
            conn.close()

@app.route('/stream')
def stream():
    # Page 2: Live Anomaly Stream
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT a.*, an.severity, an.type as anomaly_type, asset.symbol, asset.asset_id 
        FROM alerts a
        JOIN anomalies an ON a.anomaly_id = an.anomaly_id
        JOIN assets asset ON an.asset_id = asset.asset_id
        ORDER BY a.alert_id DESC
    """)
    alerts = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('stream.html', alerts=alerts)

@app.route('/analysis/<int:asset_id>')
def analysis(asset_id):
    # Page 3: Deep Dive
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM assets WHERE asset_id = %s", (asset_id,))
    asset = cursor.fetchone()
    cursor.close()
    conn.close()
    return render_template('analysis.html', asset=asset)

@app.route('/config')
def config():
    # Page 4: Configuration
    return render_template('config.html')

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
