import grpc
import ssl
import sys
import os
from django.conf import settings

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
                success = True
                error = ""
                user = type('User', (), {
                    'id': 1, 'username': 'demo', 'email': 'demo@example.com'
                })()
            return DummyResponse()
        def CreateUser(self, request, metadata=None):
            class DummyResponse:
                success = True
                error = ""
                message = "User created successfully"
                user = type('User', (), {
                    'id': 1, 'username': 'demo', 'email': 'demo@example.com'
                })()
            return DummyResponse()
        def ListUsers(self, request, metadata=None):
            class DummyResponse:
                users = [
                    type('User', (), {'id': 1, 'username': 'john', 'email': 'john@example.com'})(),
                    type('User', (), {'id': 2, 'username': 'jane', 'email': 'jane@example.com'})(),
                ]
            return DummyResponse()
        def AuthenticateUser(self, request, metadata=None):
            class DummyResponse:
                success = True
                user = type('User', (), {
                    'id': 1, 'username': 'demo', 'email': 'demo@example.com'
                })()
            return DummyResponse()

    class user_service_pb2_grpc:
        UserServiceStub = DummyStub

    class order_service_pb2_grpc:
        OrderServiceStub = DummyStub

class BaseGRPCClient:
    """Base class for gRPC clients with SSL/TLS and authentication"""

    def __init__(self, service_host, service_port, token=None, use_ssl=True):
        self.service_host = service_host
        self.service_port = service_port
        self.token = token
        self.use_ssl = use_ssl

        # Set up metadata for authentication
        self.metadata = []
        if token:
            self.metadata.append(('authorization', f'Bearer {token}'))

        # Add request ID for tracing
        import uuid
        self.metadata.append(('request-id', str(uuid.uuid4())))

        # Create channel with SSL/TLS or insecure
        self.channel = self._create_channel()

    def _create_channel(self):
        """Create gRPC channel with SSL/TLS support"""
        target = f'{self.service_host}:{self.service_port}'

        if self.use_ssl:
            try:
                # Load SSL certificates
                ssl_cert_path = getattr(settings, 'GRPC_SSL_CERT_PATH', None)
                ssl_key_path = getattr(settings, 'GRPC_SSL_KEY_PATH', None)
                ssl_ca_path = getattr(settings, 'GRPC_SSL_CA_PATH', None)

                if ssl_cert_path and ssl_key_path and ssl_ca_path:
                    # Load certificates
                    with open(ssl_ca_path, 'rb') as f:
                        trusted_certs = f.read()
                    with open(ssl_cert_path, 'rb') as f:
                        cert_chain = f.read()
                    with open(ssl_key_path, 'rb') as f:
                        private_key = f.read()

                    # Create SSL credentials
                    credentials = grpc.ssl_channel_credentials(
                        root_certificates=trusted_certs,
                        private_key=private_key,
                        certificate_chain=cert_chain
                    )

                    # Create secure channel
                    return grpc.secure_channel(target, credentials)
                else:
                    # Use default SSL credentials
                    credentials = grpc.ssl_channel_credentials()
                    return grpc.secure_channel(target, credentials)

            except Exception as e:
                print(f"SSL setup failed, falling back to insecure: {e}")
                return grpc.insecure_channel(target)
        else:
            return grpc.insecure_channel(target)

    def close(self):
        """Close the gRPC channel"""
        if hasattr(self, 'channel'):
            self.channel.close()

class UserServiceClient(BaseGRPCClient):
    def __init__(self, token=None):
        super().__init__(
            service_host=getattr(settings, 'USER_SERVICE_HOST', 'user_service'),
            service_port=getattr(settings, 'USER_SERVICE_PORT', 50051),
            token=token,
            use_ssl=getattr(settings, 'GRPC_USE_SSL', False)
        )
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