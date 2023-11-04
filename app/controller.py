from datetime import datetime

import redis
from django.utils import timezone
from rest_framework.response import Response

from .models import Customer, WorkOrder
from .serializers import (
    CustomerSerializer,
    CustomerWithWorkOrdersSerializer,
    WorkOrderSerializer,
)


class Controllers():
    
    @staticmethod
    def filter_active_customer():
        active_customers = Customer.objects.filter(is_active=True)
        serializer = CustomerSerializer(active_customers, many=True)
        return serializer.data

    @staticmethod
    def customer_by_id(customer_id):
        try:
            customer = Customer.objects.get(id=customer_id)
            serializer = CustomerWithWorkOrdersSerializer(customer)
            return Response(serializer.data)
        except Customer.DoesNotExist:
            return Response({"message": "Customer not found"}, status=404)
        
    @staticmethod
    def changue_is_active_customer(self, serializer, customer_id):

        get_status= serializer.validated_data.get('status') 

        try:
            customer = Customer.objects.get(id=customer_id)
            order_by_customer=self.customer_by_id(customer_id)
            num_orders =len(order_by_customer.data['work_orders'])

            print(customer.is_active)
            print(num_orders)
            print(get_status)

            # si ya hay una orden y esta en False,
            # no se hace ningun cambio al estado, segun el requerimiento.
            if num_orders>= 1 and customer.is_active == False:
                print('no hace nada')
                return False

            ## 1. cambia estado a true al finalizar la primera orden,
            ## 4. si es la primera orden, cambia is_active a True
            if get_status == 'Done' or num_orders== 0:
                print('cambio 1')
                status = True
                customer.start_date = timezone.now()

            ## 4. se crea otra orden de servicio y el is_active queda en False
            if get_status == 'New' and num_orders>= 1:
                print('cambio 2')
                status = False
                customer.end_date = timezone.now()

            self.publish_redis_event(customer_id, status)

            customer.is_active = status
            customer.save()
            return False
        except Customer.DoesNotExist:
            return True

    @staticmethod
    def get_order_between_date(since, until, status):
        
        since_date = datetime.strptime(since, "%Y-%m-%d")
        since_date = since_date.replace(hour=0, minute=0, second=0, microsecond=0)

        until_date = datetime.strptime(until, "%Y-%m-%d")
        until_date = until_date.replace(hour=23, minute=59, second=59, microsecond=999999)

        orders = WorkOrder.objects.filter(
            created_at__range=(since_date, until_date),
            status=status
        )
        serializer = WorkOrderSerializer(orders, many=True)
        return Response(serializer.data)
    
    @staticmethod
    def publish_redis_event(order_id, status):

        r = redis.StrictRedis(host='localhost', port=6379, db=0)

        stream_name = 'ordenes_de_servicio'
        evento = {
            'order_id': order_id,
            'status': status,
        }
        r.xadd(stream_name, evento)
