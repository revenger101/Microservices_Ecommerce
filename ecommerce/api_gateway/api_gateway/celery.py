import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'api_gateway.settings')

app = Celery('api_gateway')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

@app.task(bind=True, max_retries=3)
def process_order(self, user_id, items):
    try:
        # Import here to avoid circular imports
        from gateway.services import UserServiceClient, OrderServiceClient

        # Validate user exists
        user_client = UserServiceClient()
        user_response = user_client.get_user(user_id)
        if user_response.error:
            raise ValueError(f"User not found: {user_response.error}")

        # Create order
        order_client = OrderServiceClient()
        order_response = order_client.create_order(user_id, items)

        if order_response.error:
            raise ValueError(f"Order creation failed: {order_response.error}")

        return {
            'status': 'success',
            'order_id': order_response.order.id
        }
    except Exception as exc:
        raise self.retry(exc=exc, countdown=2 ** self.request.retries)