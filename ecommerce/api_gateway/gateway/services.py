import grpc
import sys
import os

# Add the protos directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'protos'))

try:
    import user_service_pb2
    import user_service_pb2_grpc
    import order_service_pb2
    import order_service_pb2_grpc
except ImportError as e:
    print(f"Import error: {e}")
    # Create dummy classes for development
    class DummyStub:
        def __init__(self, channel): pass
        def GetUser(self, request, metadata=None):
            class DummyResponse:
                error = "Service not available"
            return DummyResponse()
        def CreateUser(self, user):
            class DummyResponse:
                error = "Service not available"
            return DummyResponse()

    class user_service_pb2_grpc:
        UserServiceStub = DummyStub

    class order_service_pb2_grpc:
        OrderServiceStub = DummyStub

class UserServiceClient:
    def __init__(self, token=None):
        if token:
            self.metadata = [('authorization', f'Bearer {token}')]
        else:
            self.metadata = None

        # Use insecure channel for now (we can add SSL later)
        self.channel = grpc.insecure_channel('user_service:50051')
        self.stub = user_service_pb2_grpc.UserServiceStub(self.channel)

    def get_user(self, user_id):
        try:
            request = user_service_pb2.UserRequest(id=user_id)
            return self.stub.GetUser(request, metadata=self.metadata)
        except Exception as e:
            class ErrorResponse:
                error = f"Error getting user: {str(e)}"
            return ErrorResponse()

    def create_user(self, username, email, password):
        try:
            user = user_service_pb2.User(
                username=username,
                email=email,
                password=password
            )
            return self.stub.CreateUser(user)
        except Exception as e:
            class ErrorResponse:
                error = f"Error creating user: {str(e)}"
            return ErrorResponse()

class OrderServiceClient:
    def __init__(self):
        self.channel = grpc.insecure_channel('order_service:50052')
        self.stub = order_service_pb2_grpc.OrderServiceStub(self.channel)

    def create_order(self, user_id, items):
        try:
            order_items = [order_service_pb2.OrderItem(
                product_id=item['product_id'],
                quantity=item['quantity'],
                price=item['price']
            ) for item in items]

            order = order_service_pb2.Order(
                user_id=user_id,
                items=order_items,
                status='PENDING'
            )
            return self.stub.CreateOrder(order)
        except Exception as e:
            class ErrorResponse:
                error = f"Error creating order: {str(e)}"
            return ErrorResponse()

    def get_user_orders(self, user_id):
        try:
            request = order_service_pb2.UserOrdersRequest(user_id=user_id)
            return self.stub.ListOrders(request)
        except Exception as e:
            class ErrorResponse:
                error = f"Error getting orders: {str(e)}"
            return ErrorResponse()