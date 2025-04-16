import streamlit as st
import requests
import time
from datetime import datetime

# Constants
ALERT_FEE_THRESHOLD = 3000  # In satoshis
CHECK_INTERVAL = 10  # seconds

# Function to get recent Bitcoin transactions
def get_recent_transactions():
    url = "https://blockstream.info/api/mempool/recent"
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print("❌ Error fetching transactions:", e)
        return []

# Function to check for alerts
def check_for_alerts():
    transactions = get_recent_transactions()
    alerts = []

    for tx in transactions:
        try:
            fee = tx.get('fee', 0)  # Safely access fee
            txid = tx.get('txid', 'Unknown')  # Safely access txid
            if fee > ALERT_FEE_THRESHOLD:
                alerts.append({
                    'txid': txid,
                    'fee': fee,
                    'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                    'url': f"https://blockstream.info/tx/{txid}"
                })
        except KeyError as e:
            print(f"❌ Missing expected data in transaction: {e}")
    return alerts

# Streamlit Dashboard
st.title("Bitcoin Transaction Monitoring Dashboard")
st.subheader("🔍 Monitoring Bitcoin transactions for high-fee alerts...")

# Display alerts
alerts = check_for_alerts()

if alerts:
    st.success(f"🚨 {len(alerts)} High-Fee TX Detected!")
    for alert in alerts:
        st.markdown(f"### TXID: {alert['txid']}")
        st.markdown(f"💸 Fee: {alert['fee']} sats")
        st.markdown(f"📅 Timestamp: {alert['timestamp']}")
        st.markdown(f"🔗 [Explorer Link]({alert['url']})")
else:
    st.warning("No high-fee transactions detected in the recent pool.")

# Add refresh interval
st.text(f"⏳ Refreshing every {CHECK_INTERVAL} seconds...")
time.sleep(CHECK_INTERVAL)


