from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .services import UserServiceClient, OrderServiceClient
from .serializers import UserSerializer, OrderSerializer
from api_gateway.celery import process_order


class UserView(APIView):
    def get(self, request, user_id):
        client = UserServiceClient()
        response = client.get_user(user_id)
        if response.error:
            return Response({'error': response.error}, status=status.HTTP_404_NOT_FOUND)
        serializer = UserSerializer(response.user)
        return Response(serializer.data)

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        client = UserServiceClient()
        response = client.create_user(
            serializer.validated_data['username'],
            serializer.validated_data['email'],
            serializer.validated_data['password']
        )
        
        if response.error:
            return Response({'error': response.error}, status=status.HTTP_400_BAD_REQUEST)
        
        return Response(UserSerializer(response.user).data, status=status.HTTP_201_CREATED)

class OrderView(APIView):
    def get(self, request, user_id):
        client = OrderServiceClient()
        response = client.get_user_orders(user_id)
        if hasattr(response, 'error'):
            return Response({'error': response.error}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = OrderSerializer(response.orders, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = OrderSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        client = OrderServiceClient()
        response = client.create_order(
            serializer.validated_data['user_id'],
            serializer.validated_data['items']
        )

        def post(self, request):
            serializer = OrderSerializer(data=request.data)
            if not serializer.is_valid():
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        # Process order asynchronously
        task = process_order.delay(
            serializer.validated_data['user_id'],
            serializer.validated_data['items']
        )
        
        
        if response.error:
            return Response({'error': response.error}, status=status.HTTP_400_BAD_REQUEST)
        
        return Response(OrderSerializer(response.order).data, status=status.HTTP_201_CREATED)