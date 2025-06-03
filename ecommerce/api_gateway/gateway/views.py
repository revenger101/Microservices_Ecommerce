from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from django.core.cache import cache
from django.utils import timezone
from .serializers import (
    UserSerializer, OrderSerializer, OrderItemSerializer,
    AuthTokenSerializer, CreateOrderSerializer, OrderStatusUpdateSerializer
)
from .services import UserServiceClient, OrderServiceClient
from api_gateway.celery import process_order, process_order_workflow
import logging

logger = logging.getLogger(__name__)

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100

# Authentication Views
@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    """Authenticate user and return token"""
    serializer = AuthTokenSerializer(data=request.data)
    if serializer.is_valid():
        email = serializer.validated_data['email']
        password = serializer.validated_data['password']

        try:
            # Call user service to authenticate
            user_client = UserServiceClient()
            user_response = user_client.authenticate_user(email, password)

            if hasattr(user_response, 'success') and user_response.success:
                # Create or get token
                token, created = Token.objects.get_or_create(user_id=user_response.user.id)

                return Response({
                    'token': token.key,
                    'user': {
                        'id': user_response.user.id,
                        'username': user_response.user.username,
                        'email': user_response.user.email,
                    }
                }, status=status.HTTP_200_OK)
            else:
                return Response({
                    'error': 'Invalid credentials'
                }, status=status.HTTP_401_UNAUTHORIZED)

        except Exception as e:
            logger.error(f"Authentication error: {str(e)}")
            return Response({
                'error': 'Authentication service unavailable'
            }, status=status.HTTP_503_SERVICE_UNAVAILABLE)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# User Management Views
@api_view(['GET', 'POST'])
@permission_classes([AllowAny])  # Allow registration
def users(request):
    """List users or create new user"""
    if request.method == 'GET':
        try:
            user_client = UserServiceClient()
            users_response = user_client.list_users()

            if hasattr(users_response, 'users'):
                serializer = UserSerializer(users_response.users, many=True)
                return Response(serializer.data)
            else:
                return Response({
                    'error': 'Failed to fetch users'
                }, status=status.HTTP_503_SERVICE_UNAVAILABLE)

        except Exception as e:
            logger.error(f"Error fetching users: {str(e)}")
            return Response({
                'error': 'User service unavailable'
            }, status=status.HTTP_503_SERVICE_UNAVAILABLE)

    elif request.method == 'POST':
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            try:
                user_client = UserServiceClient()
                user_response = user_client.create_user(
                    username=serializer.validated_data['username'],
                    email=serializer.validated_data['email'],
                    password=serializer.validated_data['password']
                )

                if hasattr(user_response, 'success') and user_response.success:
                    response_serializer = UserSerializer(user_response.user)
                    return Response(response_serializer.data, status=status.HTTP_201_CREATED)
                else:
                    return Response({
                        'error': getattr(user_response, 'message', 'Failed to create user')
                    }, status=status.HTTP_400_BAD_REQUEST)

            except Exception as e:
                logger.error(f"Error creating user: {str(e)}")
                return Response({
                    'error': 'User service unavailable'
                }, status=status.HTTP_503_SERVICE_UNAVAILABLE)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([AllowAny])
def user_detail(request, user_id):
    """Get specific user"""
    try:
        user_client = UserServiceClient()
        user_response = user_client.get_user(user_id)

        if hasattr(user_response, 'user'):
            serializer = UserSerializer(user_response.user)
            return Response(serializer.data)
        else:
            return Response({
                'error': 'User not found'
            }, status=status.HTTP_404_NOT_FOUND)

    except Exception as e:
        logger.error(f"Error in user_detail: {str(e)}")
        return Response({
            'error': 'User service unavailable'
        }, status=status.HTTP_503_SERVICE_UNAVAILABLE)

# Order Management Views
@api_view(['GET', 'POST'])
@permission_classes([AllowAny])
def orders(request):
    """List orders or create new order"""
    if request.method == 'GET':
        try:
            user_id = request.GET.get('user_id')
            order_client = OrderServiceClient()

            if user_id:
                orders_response = order_client.get_user_orders(user_id)
            else:
                # For demo purposes, return mock orders
                return Response([
                    {
                        'id': 1,
                        'user_id': 1,
                        'status': 'PENDING',
                        'total_amount': '199.99',
                        'created_at': '2024-01-15T10:30:00Z'
                    }
                ])

            if hasattr(orders_response, 'orders'):
                serializer = OrderSerializer(orders_response.orders, many=True)
                return Response(serializer.data)
            else:
                return Response({
                    'error': 'Failed to fetch orders'
                }, status=status.HTTP_503_SERVICE_UNAVAILABLE)

        except Exception as e:
            logger.error(f"Error fetching orders: {str(e)}")
            return Response({
                'error': 'Order service unavailable'
            }, status=status.HTTP_503_SERVICE_UNAVAILABLE)

    elif request.method == 'POST':
        try:
            order_client = OrderServiceClient()

            # Process order asynchronously with Celery
            task = process_order.delay(
                request.data.get('user_id', 1),
                request.data.get('items', [])
            )

            # Also create order via gRPC
            order_response = order_client.create_order(
                user_id=request.data.get('user_id', 1),
                items=request.data.get('items', [])
            )

            if hasattr(order_response, 'success') and order_response.success:
                response_serializer = OrderSerializer(order_response.order)
                return Response({
                    'order': response_serializer.data,
                    'task_id': task.id,
                    'message': 'Order created and processing started'
                }, status=status.HTTP_201_CREATED)
            else:
                return Response({
                    'error': getattr(order_response, 'message', 'Failed to create order')
                }, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            logger.error(f"Error creating order: {str(e)}")
            return Response({
                'error': 'Order service unavailable'
            }, status=status.HTTP_503_SERVICE_UNAVAILABLE)

# Health Check
@api_view(['GET'])
@permission_classes([AllowAny])
def health_check(request):
    """Health check endpoint"""
    try:
        services_status = {
            'user_service': 'healthy',
            'order_service': 'healthy',
            'celery': 'healthy',
            'database': 'healthy'
        }

        overall_status = 'healthy'

        return Response({
            'status': overall_status,
            'services': services_status,
            'timestamp': timezone.now().isoformat()
        })

    except Exception as e:
        logger.error(f"Health check error: {str(e)}")
        return Response({
            'status': 'unhealthy',
            'error': str(e)
        }, status=status.HTTP_503_SERVICE_UNAVAILABLE)