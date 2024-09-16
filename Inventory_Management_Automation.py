import pandas as pd
import numpy as np
from sqlalchemy import create_engine
from sklearn.linear_model import LinearRegression
import smtplib
from email.mime.text import MIMEText
import schedule
import time

# Database setup
engine = create_engine('sqlite:///inventory.db')

# Load inventory data
def load_data():
    df = pd.read_sql('inventory', engine)
    return df

# Track current stock levels
def track_stock(df):
    df['stock_level'] = df['initial_stock'] - df['sales']
    return df

# Predict stock-out events
def predict_stock_out(df):
    df['days_to_stock_out'] = df['stock_level'] / df['daily_sales']
    return df

# Generate reordering triggers
def generate_reorder_triggers(df):
    reorder_points = df['reorder_point']
    stock_levels = df['stock_level']
    reorder_triggers = df[stock_levels <= reorder_points]
    return reorder_triggers

# Send notification
def send_notification(reorder_triggers):
    msg = MIMEText(reorder_triggers.to_string())
    msg['Subject'] = 'Reorder Notification'
    msg['From'] = 'your_email@example.com'
    msg['To'] = 'recipient@example.com'
    
    with smtplib.SMTP('smtp.example.com') as server:
        server.login('your_email@example.com', 'your_password')
        server.sendmail(msg['From'], [msg['To']], msg.as_string())

# Main function to run the workflow
def run_inventory_management():
    df = load_data()
    df = track_stock(df)
    df = predict_stock_out(df)
    reorder_triggers = generate_reorder_triggers(df)
    if not reorder_triggers.empty:
        send_notification(reorder_triggers)

# Schedule the script to run daily
schedule.every().day.at("00:00").do(run_inventory_management)

# Keep the script running
while True:
    schedule.run_pending()
    time.sleep(1)