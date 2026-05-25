from flask import Flask, render_template, jsonify
import mysql.connector
import pandas as pd

import os
import random

app = Flask(__name__)

# --- DATABASE CONFIGURATION ---
# Check if running on Vercel (Production) or Local
IS_VERCEL = "VERCEL" in os.environ

db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'AAdd541@$',
    'database': 'crypto_anomaly_db'
}

def get_db_connection():
    if IS_VERCEL:
        return None  # No local MySQL on Vercel
    return mysql.connector.connect(**db_config)

# --- MOCK DATA FOR CLOUD DEMO ---
def get_mock_data():
    assets = [
        {'asset_id': 1, 'name': 'Bitcoin', 'symbol': 'BTC', 'type': 'Crypto'},
        {'asset_id': 2, 'name': 'Ethereum', 'symbol': 'ETH', 'type': 'Crypto'},
        {'asset_id': 3, 'name': 'NVIDIA', 'symbol': 'NVDA', 'type': 'Stock'},
        {'asset_id': 17, 'name': 'Tesla', 'symbol': 'TSLA', 'type': 'Stock'}
    ]
    alerts = [
        {'alert_id': 101, 'asset_id': 1, 'symbol': 'BTC', 'severity': 'Critical', 'anomaly_type': 'Flash Crash', 'alert_message': 'Emergency: BTC price dropped 8.2% in 5 minutes. High sell volume detected.'},
        {'alert_id': 102, 'asset_id': 3, 'symbol': 'NVDA', 'severity': 'Warning', 'anomaly_type': 'Volume Spike', 'alert_message': 'NVDA trading volume 3x above average. Analyzing price stability...'}
    ]
    stats = {'assets': 4, 'rows': '15,240', 'anomalies': 12}
    return assets, alerts, stats

@app.route('/')
def index():
    if IS_VERCEL:
        assets, alerts, stats = get_mock_data()
        return render_template('dashboard.html', assets=assets, alerts=alerts, stats=stats)
    
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
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
        return render_template('dashboard.html', assets=assets, alerts=alerts, 
                             stats={'assets': asset_count, 'rows': row_count, 'anomalies': anomaly_count})
    except Exception as e:
        return f"Database Error: {e}", 500
    finally:
        if conn: conn.close()

@app.route('/stream')
def stream():
    if IS_VERCEL:
        _, alerts, _ = get_mock_data()
        return render_template('stream.html', alerts=alerts)
    
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
    conn.close()
    return render_template('stream.html', alerts=alerts)

@app.route('/analysis/<int:asset_id>')
def analysis(asset_id):
    if IS_VERCEL:
        assets, _, _ = get_mock_data()
        asset = next((a for a in assets if a['asset_id'] == asset_id), assets[0])
        return render_template('analysis.html', asset=asset)
    
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM assets WHERE asset_id = %s", (asset_id,))
    asset = cursor.fetchone()
    conn.close()
    return render_template('analysis.html', asset=asset)

@app.route('/config')
def config():
    return render_template('config.html')

@app.route('/classic_php')
def classic_php_info():
    # Redirecting to the PHP entry point (assuming user runs XAMPP)
    # On Vercel, we can just show a demo message
    return "<h1>Classic PHP Module</h1><p>To view the PHP CRUD, ensure you have XAMPP/WAMP running and access <b>/php_module/index.php</b> directly. This module demonstrates standard index.php and mysqli integration as per lab guidelines.</p><a href='/'>Back to Dashboard</a>"

@app.route('/api/prices/<int:asset_id>')
def get_prices(asset_id):
    if IS_VERCEL:
        labels = [f"12:{i:02d}" for i in range(10, 50, 2)]
        values = [random.uniform(60000, 65000) if asset_id == 1 else random.uniform(100, 200) for _ in range(20)]
        return jsonify({'labels': labels, 'values': values})

    conn = None
    try:
        conn = get_db_connection()
        query = "SELECT timestamp, price_close FROM price_history WHERE asset_id = %s ORDER BY timestamp ASC"
        df = pd.read_sql(query, conn, params=(asset_id,))
        labels = pd.to_datetime(df['timestamp']).dt.strftime('%H:%M').tolist() if not df.empty else []
        values = df['price_close'].tolist() if not df.empty else []
        return jsonify({'labels': labels, 'values': values})
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        if conn: conn.close()

if __name__ == '__main__':
    app.run(debug=True)
