import graphene
from graphene_django import DjangoObjectType
from .services import UserServiceClient, OrderServiceClient

class UserType(graphene.ObjectType):
    id = graphene.Int()
    username = graphene.String()
    email = graphene.String()
    
    def resolve_id(self, info):
        return self.id
    
    def resolve_username(self, info):
        return self.username
    
    def resolve_email(self, info):
        return self.email

class OrderItemType(graphene.ObjectType):
    product_id = graphene.Int()
    quantity = graphene.Int()
    price = graphene.Float()

class OrderType(graphene.ObjectType):
    id = graphene.Int()
    user_id = graphene.Int()
    items = graphene.List(OrderItemType)
    status = graphene.String()
    created_at = graphene.String()
    
    def resolve_user(self, info):
        user_client = UserServiceClient()
        user_response = user_client.get_user(self.user_id)
        return UserType(
            id=user_response.user.id,
            username=user_response.user.username,
            email=user_response.user.email
        )