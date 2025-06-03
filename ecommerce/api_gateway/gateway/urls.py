from django.urls import path, include
from graphene_django.views import GraphQLView
from .schema import schema
from . import views

# REST API URLs
api_patterns = [
    # Authentication
    path('auth/login/', views.login, name='api-login'),

    # Users
    path('users/', views.users, name='api-users'),
    path('users/<int:user_id>/', views.user_detail, name='api-user-detail'),

    # Orders
    path('orders/', views.orders, name='api-orders'),

    # Health
    path('health/', views.health_check, name='api-health'),
]

urlpatterns = [
    # GraphQL endpoint
    path('graphql/', GraphQLView.as_view(graphiql=True, schema=schema)),

    # REST API endpoints
    path('api/v1/', include(api_patterns)),
]