import time
import random
from celery import Celery
from celery.schedules import crontab
from datetime import datetime, timedelta
from sklearn.linear_model import LinearRegression
import numpy as np

app = Celery('api_gateway')

# Mock historical data (in a real app, this would come from monitoring)
historical_data = []

def predict_load():
    if len(historical_data) < 10:
        return random.randint(1, 5)  # Default to small scale
    
    # Simple linear regression for prediction
    X = np.array(range(len(historical_data))).reshape(-1, 1)
    y = np.array(historical_data)
    model = LinearRegression().fit(X, y)
    prediction = model.predict([[len(historical_data)]])[0]
    return max(1, min(10, int(prediction)))  # Cap between 1 and 10

@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    # Check load every minute
    sender.add_periodic_task(
        crontab(minute='*'),
        monitor_load.s(),
    )

@app.task
def monitor_load():
    # Simulate getting current load (replace with actual metrics)
    current_load = random.randint(1, 100)
    historical_data.append(current_load)
    
    predicted_load = predict_load()
    print(f"Predicted load for next period: {predicted_load}")
    
    # In a real implementation, this would trigger scaling actions
    if predicted_load > 8 and len(historical_data) > 20:
        print("ALERT: Scaling up services needed!")
    elif predicted_load < 3 and len(historical_data) > 20:
        print("ALERT: Scaling down services possible.")