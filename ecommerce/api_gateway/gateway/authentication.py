import grpc
from functools import wraps
from django.conf import settings
from django.contrib.auth import get_user_model

def get_user_from_token(token):
    # In a real implementation, validate the token with your auth service
    if token == "valid_token":
        return {"id": 1, "username": "admin"}
    return None

class AuthInterceptor(grpc.ServerInterceptor):
    def __init__(self):
        def abort(ignored_request, context):
            context.abort(grpc.StatusCode.UNAUTHENTICATED, 'Invalid token')
        
        self._abortion = grpc.unary_unary_rpc_method_handler(abort)

    def intercept_service(self, continuation, handler_call_details):
        metadata = dict(handler_call_details.invocation_metadata)
        if 'authorization' not in metadata:
            return self._abortion
        
        token = metadata['authorization'].split('Bearer ')[-1]
        user = get_user_from_token(token)
        if not user:
            return self._abortion
        
        return continuation(handler_call_details)