import graphene
from .types import UserType, OrderType

class Query(graphene.ObjectType):
    user = graphene.Field(UserType, id=graphene.Int())
    orders = graphene.List(OrderType, user_id=graphene.Int())
    
    def resolve_user(self, info, id):
        from .services import UserServiceClient
        client = UserServiceClient()
        response = client.get_user(id)
        if response.error:
            raise Exception(response.error)
        return response.user
    
    def resolve_orders(self, info, user_id):
        from .services import OrderServiceClient
        client = OrderServiceClient()
        response = client.get_user_orders(user_id)
        if hasattr(response, 'error'):
            raise Exception(response.error)
        return response.orders

class CreateUser(graphene.Mutation):
    class Arguments:
        username = graphene.String(required=True)
        email = graphene.String(required=True)
        password = graphene.String(required=True)
    
    user = graphene.Field(UserType)
    
    def mutate(self, info, username, email, password):
        from .services import UserServiceClient
        client = UserServiceClient()
        response = client.create_user(username, email, password)
        if response.error:
            raise Exception(response.error)
        return CreateUser(user=response.user)

class CreateOrder(graphene.Mutation):
    class Arguments:
        user_id = graphene.Int(required=True)
        items = graphene.List(graphene.JSONString)
    
    order = graphene.Field(OrderType)
    
    def mutate(self, info, user_id, items):
        from .services import OrderServiceClient
        client = OrderServiceClient()
        response = client.create_order(user_id, items)
        if response.error:
            raise Exception(response.error)
        return CreateOrder(order=response.order)

class Mutation(graphene.ObjectType):
    create_user = CreateUser.Field()
    create_order = CreateOrder.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)