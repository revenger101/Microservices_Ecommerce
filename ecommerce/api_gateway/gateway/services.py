import grpc
from protos import user_service_pb2, user_service_pb2_grpc
from protos import order_service_pb2, order_service_pb2_grpc

class UserServiceClient:
    def __init__(self , token=None):
        with open('ca.crt', 'rb') as f:
            trusted_certs = f.read()

        if token:
            self.metadata = [('authorization', f'Bearer {token}')]
        else:
            self.metadata = None
        
        credentials = grpc.ssl_channel_credentials(
            root_certificates=trusted_certs
        )
        self.channel = grpc.secure_channel('user_service:50051', credentials)
        self.stub = user_service_pb2_grpc.UserServiceStub(self.channel)

    def get_user(self, user_id):
        request = user_service_pb2.UserRequest(id=user_id)
        return self.stub.GetUser(request, metadata=self.metadata)

    def create_user(self, username, email, password):
        user = user_service_pb2.User(
            username=username,
            email=email,
            password=password
        )
        return self.stub.CreateUser(user)

class OrderServiceClient:
    def __init__(self):
        self.channel = grpc.insecure_channel('order_service:50052')
        self.stub = order_service_pb2_grpc.OrderServiceStub(self.channel)

    def create_order(self, user_id, items):
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

    def get_user_orders(self, user_id):
        request = order_service_pb2.UserOrdersRequest(user_id=user_id)
        return self.stub.ListOrders(request)