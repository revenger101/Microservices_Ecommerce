from concurrent import futures
import grpc
from django.core.exceptions import ObjectDoesNotExist
from ..protos import user_service_pb2, user_service_pb2_grpc
from .models import User
from ..gateway.authentication import AuthInterceptor


class UserService(user_service_pb2_grpc.UserServiceServicer):
    def CreateUser(self, request, context):
        try:
            user = User.objects.create(
                username=request.username,
                email=request.email,
                password=request.password
            )
            return user_service_pb2.UserResponse(user=self._user_to_proto(user))
        except Exception as e:
            context.set_code(grpc.StatusCode.ALREADY_EXISTS)
            return user_service_pb2.UserResponse(error=str(e))

    def GetUser(self, request, context):
        try:
            user = User.objects.get(id=request.id)
            return user_service_pb2.UserResponse(user=self._user_to_proto(user))
        except ObjectDoesNotExist:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            return user_service_pb2.UserResponse(error="User not found")

    def ListUsers(self, request, context):
        users = User.objects.all()
        return user_service_pb2.UserList(users=[self._user_to_proto(user) for user in users])

    def _user_to_proto(self, user):
        return user_service_pb2.User(
            id=user.id,
            username=user.username,
            email=user.email,
            password=user.password
        )

def serve():
    with open('user_service.key', 'rb') as f:
        private_key = f.read()
    with open('user_service.crt', 'rb') as f:
        certificate = f.read()

    server = grpc.server(
        futures.ThreadPoolExecutor(max_workers=10),
        interceptors=(AuthInterceptor(),)
    )
    
    server_credentials = grpc.ssl_server_credentials(
        [(private_key, certificate)]
    )
    
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    user_service_pb2_grpc.add_UserServiceServicer_to_server(UserService(), server)
    server.add_secure_port('[::]:50051', server_credentials)
    server.start()
    server.wait_for_termination()