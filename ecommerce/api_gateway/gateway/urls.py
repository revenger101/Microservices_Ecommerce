from django.urls import path
from .views import UserView, OrderView
from graphene_django.views import GraphQLView
from .schema import schema

urlpatterns = [
    path('users/<int:user_id>/', UserView.as_view()),
    path('users/', UserView.as_view()),
    path('orders/<int:user_id>/', OrderView.as_view()),
    path('orders/', OrderView.as_view()),
    path('graphql/', GraphQLView.as_view(graphiql=True, schema=schema)),
]