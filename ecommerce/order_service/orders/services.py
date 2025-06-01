from concurrent import futures
import grpc
from django.core.exceptions import ObjectDoesNotExist
from datetime import datetime
from ..protos import order_service_pb2, order_service_pb2_grpc
from .models import Order, OrderItem

class OrderService(order_service_pb2_grpc.OrderServiceServicer):
    def CreateOrder(self, request, context):
        try:
            order = Order.objects.create(
                user_id=request.user_id,
                status=request.status
            )
            
            for item in request.items:
                OrderItem.objects.create(
                    order=order,
                    product_id=item.product_id,
                    quantity=item.quantity,
                    price=item.price
                )
            
            return order_service_pb2.OrderResponse(order=self._order_to_proto(order))
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            return order_service_pb2.OrderResponse(error=str(e))

    def GetOrder(self, request, context):
        try:
            order = Order.objects.get(id=request.id)
            return order_service_pb2.OrderResponse(order=self._order_to_proto(order))
        except ObjectDoesNotExist:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            return order_service_pb2.OrderResponse(error="Order not found")

    def ListOrders(self, request, context):
        orders = Order.objects.filter(user_id=request.user_id)
        return order_service_pb2.OrderList(orders=[self._order_to_proto(order) for order in orders])

    def _order_to_proto(self, order):
        items = [order_service_pb2.OrderItem(
            product_id=item.product_id,
            quantity=item.quantity,
            price=float(item.price)
        ) for item in order.items.all()]
        
        return order_service_pb2.Order(
            id=order.id,
            user_id=order.user_id,
            items=items,
            status=order.status,
            created_at=order.created_at.strftime('%Y-%m-%d %H:%M:%S')
        )

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    order_service_pb2_grpc.add_OrderServiceServicer_to_server(OrderService(), server)
    server.add_insecure_port('[::]:50052')
    server.start()
    server.wait_for_termination()