import os
import logging
import time
import random
from datetime import datetime, timedelta
from celery import Celery, group, chain, chord
from celery.exceptions import Retry
from django.core.cache import cache
import numpy as np

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'api_gateway.settings')

app = Celery('api_gateway')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django apps.
app.autodiscover_tasks()

logger = logging.getLogger(__name__)

# AI-based Load Prediction Model
class LoadPredictor:
    def __init__(self):
        self.historical_data = []
        self.is_trained = False

    def add_data_point(self, timestamp, load_metric, concurrent_users=0, orders_per_hour=0):
        """Add a data point for training"""
        self.historical_data.append({
            'timestamp': timestamp.isoformat(),
            'load_metric': load_metric,
            'concurrent_users': concurrent_users,
            'orders_per_hour': orders_per_hour
        })

        # Keep only last 1000 data points
        if len(self.historical_data) > 1000:
            self.historical_data = self.historical_data[-1000:]

    def predict_load(self, timestamp=None):
        """Predict load for given timestamp using simple heuristics"""
        if timestamp is None:
            timestamp = datetime.now()

        # Simple heuristic-based prediction
        hour = timestamp.hour
        day_of_week = timestamp.weekday()

        # Base load based on time of day
        if 9 <= hour <= 17:  # Business hours
            base_load = 0.7
        elif 18 <= hour <= 22:  # Evening
            base_load = 0.5
        else:  # Night/early morning
            base_load = 0.2

        # Adjust for day of week
        if day_of_week in [5, 6]:  # Weekend
            base_load *= 0.6

        # Add some randomness
        load = base_load + random.uniform(-0.1, 0.1)
        return max(0.1, min(1.0, load))  # Clamp between 0.1 and 1.0

load_predictor = LoadPredictor()

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')

# Cross-service workflow orchestration
@app.task(bind=True, autoretry_for=(Exception,), retry_kwargs={'max_retries': 3, 'countdown': 60})
def validate_user(self, user_id):
    """Validate user exists and is active"""
    try:
        from gateway.services import UserServiceClient

        logger.info(f"Validating user {user_id}")

        client = UserServiceClient()
        response = client.get_user(user_id)

        if hasattr(response, 'user') and response.user:
            return {
                'user_id': user_id,
                'valid': True,
                'user_data': {
                    'id': response.user.id,
                    'username': getattr(response.user, 'username', 'demo'),
                    'email': getattr(response.user, 'email', 'demo@example.com')
                }
            }
        else:
            return {'user_id': user_id, 'valid': False, 'error': 'User not found'}

    except Exception as e:
        logger.error(f"Error validating user {user_id}: {str(e)}")
        raise self.retry(countdown=60, exc=e)

@app.task(bind=True, autoretry_for=(Exception,), retry_kwargs={'max_retries': 3, 'countdown': 60})
def validate_inventory(self, items):
    """Validate product inventory"""
    try:
        logger.info(f"Validating inventory for items: {items}")

        # Simulate inventory check
        validated_items = []
        for item in items:
            # Mock inventory validation
            available_quantity = random.randint(0, 100)
            if available_quantity >= item.get('quantity', 1):
                validated_items.append({
                    **item,
                    'available': True,
                    'available_quantity': available_quantity
                })
            else:
                validated_items.append({
                    **item,
                    'available': False,
                    'available_quantity': available_quantity
                })

        return {
            'items': validated_items,
            'all_available': all(item['available'] for item in validated_items)
        }

    except Exception as e:
        logger.error(f"Error validating inventory: {str(e)}")
        raise self.retry(countdown=60, exc=e)

@app.task(bind=True, autoretry_for=(Exception,), retry_kwargs={'max_retries': 3, 'countdown': 60})
def calculate_pricing(self, items, user_data):
    """Calculate order pricing with discounts"""
    try:
        logger.info(f"Calculating pricing for user {user_data.get('user_id')}")

        subtotal = sum(item.get('price', 29.99) * item.get('quantity', 1) for item in items)

        # Apply user-specific discounts
        discount_rate = 0.1 if user_data.get('user_data', {}).get('username') == 'premium' else 0.05
        discount_amount = subtotal * discount_rate

        tax_rate = 0.08
        tax_amount = (subtotal - discount_amount) * tax_rate

        shipping_amount = 10.0 if subtotal < 50 else 0.0

        total = subtotal - discount_amount + tax_amount + shipping_amount

        return {
            'subtotal': round(subtotal, 2),
            'discount_amount': round(discount_amount, 2),
            'tax_amount': round(tax_amount, 2),
            'shipping_amount': round(shipping_amount, 2),
            'total': round(total, 2)
        }

    except Exception as e:
        logger.error(f"Error calculating pricing: {str(e)}")
        raise self.retry(countdown=60, exc=e)

@app.task(bind=True, autoretry_for=(Exception,), retry_kwargs={'max_retries': 3, 'countdown': 60})
def create_order_record(self, user_data, items, pricing):
    """Create order record in order service"""
    try:
        from gateway.services import OrderServiceClient

        logger.info(f"Creating order for user {user_data.get('user_id')}")

        client = OrderServiceClient()
        response = client.create_order(
            user_id=user_data['user_id'],
            items=items
        )

        if hasattr(response, 'success') and response.success:
            return {
                'order_id': getattr(response.order, 'id', random.randint(1000, 9999)),
                'order_number': getattr(response.order, 'order_number', f'ORD-{random.randint(10000, 99999)}'),
                'status': 'CREATED'
            }
        else:
            raise Exception(f"Failed to create order: {getattr(response, 'message', 'Unknown error')}")

    except Exception as e:
        logger.error(f"Error creating order: {str(e)}")
        raise self.retry(countdown=60, exc=e)

@app.task(bind=True)
def send_order_confirmation(self, user_data, order_data, pricing):
    """Send order confirmation email"""
    try:
        logger.info(f"Sending confirmation for order {order_data.get('order_number')}")

        # Simulate email sending
        time.sleep(1)

        return {
            'email_sent': True,
            'recipient': user_data.get('user_data', {}).get('email'),
            'order_number': order_data.get('order_number')
        }

    except Exception as e:
        logger.error(f"Error sending confirmation: {str(e)}")
        return {'email_sent': False, 'error': str(e)}

@app.task(bind=True)
def update_inventory(self, items):
    """Update inventory after order creation"""
    try:
        logger.info(f"Updating inventory for {len(items)} items")

        # Simulate inventory update
        time.sleep(0.5)

        updated_items = []
        for item in items:
            updated_items.append({
                'product_id': item.get('product_id'),
                'quantity_reserved': item.get('quantity'),
                'updated': True
            })

        return {'items_updated': updated_items}

    except Exception as e:
        logger.error(f"Error updating inventory: {str(e)}")
        return {'items_updated': [], 'error': str(e)}

# Complex workflow orchestration
@app.task(bind=True)
def process_order_workflow(self, user_id, items):
    """Orchestrate complete order processing workflow"""
    try:
        logger.info(f"Starting order workflow for user {user_id}")

        # Step 1: Validate user and inventory in parallel
        validation_group = group(
            validate_user.s(user_id),
            validate_inventory.s(items)
        )

        # Step 2: Calculate pricing after validation
        # Step 3: Create order and send confirmation in parallel
        # Step 4: Update inventory

        workflow = chain(
            validation_group,
            calculate_pricing.s(items),
            group(
                create_order_record.s(items),
                send_order_confirmation.s()
            ),
            update_inventory.s(items)
        )

        result = workflow.apply_async()

        return {
            'workflow_id': result.id,
            'status': 'started',
            'user_id': user_id,
            'items_count': len(items)
        }

    except Exception as e:
        logger.error(f"Error starting workflow: {str(e)}")
        return {'error': str(e), 'status': 'failed'}

# AI-based load prediction and auto-scaling
@app.task(bind=True)
def collect_load_metrics(self):
    """Collect current load metrics"""
    try:
        current_time = datetime.now()

        # Simulate collecting metrics
        concurrent_users = random.randint(10, 100)
        orders_per_hour = random.randint(5, 50)
        cpu_usage = random.uniform(0.2, 0.9)
        memory_usage = random.uniform(0.3, 0.8)

        # Calculate load metric (composite score)
        load_metric = (cpu_usage * 0.4 + memory_usage * 0.3 +
                      min(concurrent_users / 100, 1.0) * 0.3)

        # Store in cache for real-time access
        cache.set('concurrent_users', concurrent_users, 300)
        cache.set('orders_per_hour', orders_per_hour, 300)
        cache.set('current_load', load_metric, 300)

        # Add to predictor
        load_predictor.add_data_point(
            current_time, load_metric, concurrent_users, orders_per_hour
        )

        return {
            'timestamp': current_time.isoformat(),
            'load_metric': load_metric,
            'concurrent_users': concurrent_users,
            'orders_per_hour': orders_per_hour,
            'cpu_usage': cpu_usage,
            'memory_usage': memory_usage
        }

    except Exception as e:
        logger.error(f"Error collecting metrics: {str(e)}")
        return {'error': str(e)}

@app.task(bind=True)
def predict_and_scale(self):
    """Predict future load and trigger auto-scaling"""
    try:
        current_time = datetime.now()
        future_time = current_time + timedelta(minutes=30)

        # Predict load for next 30 minutes
        predicted_load = load_predictor.predict_load(future_time)
        current_load = cache.get('current_load', 0.5)

        logger.info(f"Current load: {current_load:.2f}, Predicted load: {predicted_load:.2f}")

        # Auto-scaling logic
        scaling_action = None
        if predicted_load > 0.8 and current_load > 0.7:
            scaling_action = 'scale_up'
            # Trigger scaling up (would integrate with Kubernetes/Docker Swarm)
            logger.info("🔥 High load predicted - triggering scale up")

        elif predicted_load < 0.3 and current_load < 0.4:
            scaling_action = 'scale_down'
            # Trigger scaling down
            logger.info("📉 Low load predicted - triggering scale down")

        # Store prediction results
        cache.set('load_prediction', {
            'predicted_load': predicted_load,
            'prediction_time': future_time.isoformat(),
            'scaling_action': scaling_action
        }, 1800)  # 30 minutes

        return {
            'current_load': current_load,
            'predicted_load': predicted_load,
            'prediction_for': future_time.isoformat(),
            'scaling_action': scaling_action,
            'timestamp': current_time.isoformat()
        }

    except Exception as e:
        logger.error(f"Error in prediction/scaling: {str(e)}")
        return {'error': str(e)}

# Periodic tasks for monitoring and scaling
@app.task(bind=True)
def monitor_system_health(self):
    """Monitor overall system health"""
    try:
        # Collect metrics
        metrics_result = collect_load_metrics.delay()

        # Predict and scale
        scaling_result = predict_and_scale.delay()

        return {
            'metrics_task': metrics_result.id,
            'scaling_task': scaling_result.id,
            'status': 'monitoring_active'
        }

    except Exception as e:
        logger.error(f"Error in system monitoring: {str(e)}")
        return {'error': str(e)}

# Simple order processing (backward compatibility)
@app.task(bind=True, max_retries=3)
def process_order(self, user_id, items):
    """Simple order processing (backward compatibility)"""
    try:
        # Use the complex workflow for better reliability
        workflow_result = process_order_workflow.delay(user_id, items)

        return {
            'status': 'success',
            'workflow_id': workflow_result.id,
            'message': 'Order processing started with advanced workflow'
        }

    except Exception as exc:
        logger.error(f"Error in simple order processing: {str(exc)}")
        raise self.retry(exc=exc, countdown=2 ** self.request.retries)