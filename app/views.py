
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView

from .controller import Controllers as C
from .models import Customer, WorkOrder
from .serializers import CustomerSerializer, WorkOrderSerializer


class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

    def create(self, request, *args, **kwargs):
        print(request.data)
        serializer = self.get_serializer(data=request.data)
        print(serializer)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

class WorkOrderViewSet(viewsets.ModelViewSet):
    queryset = WorkOrder.objects.all()
    serializer_class = WorkOrderSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        if C.changue_is_active_customer(C, serializer, request.data['customer_id']):
            return Response("The customer does not exist.", status=status.HTTP_404_NOT_FOUND)
        self.perform_update(serializer)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
    
class OrdersByCustomerViewSet(APIView):
    def get(self, request, customer_id):
        return C.customer_by_id(customer_id)

class ActiveCustomersView(APIView):
    def get(self, request):
        return Response(C.filter_active_customer())        

class OrdersWithinDateRangeOrStatus(APIView):

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('since', openapi.IN_QUERY, type=openapi.TYPE_STRING, description="Fecha de inicio en formato 'YYYY-MM-DD'"),
            openapi.Parameter('until', openapi.IN_QUERY, type=openapi.TYPE_STRING, description="Fecha final en formato 'YYYY-MM-DD'"),
            openapi.Parameter('status', openapi.IN_QUERY, type=openapi.TYPE_STRING, description="Estado de la orden de trabajo"),
        ],
        operation_description="Get orders within a date range and status"
    )

    def get(self, request):
        since = request.query_params.get('since')
        until = request.query_params.get('until')
        status = request.query_params.get('status')
    
        return C.get_order_between_date(since, until, status)