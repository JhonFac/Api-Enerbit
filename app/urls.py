from django.urls import include, path
from rest_framework.routers import DefaultRouter

from app import views

router = DefaultRouter()

router.register(r'customers', views.CustomerViewSet,  basename="CustomerViewSet")
router.register(r'work-orders', views.WorkOrderViewSet,  basename="WorkOrderViewSet")

urlpatterns = [
    path('', include(router.urls)),
    path('orders_by_customers/<uuid:customer_id>/', views.OrdersByCustomerViewSet.as_view(), name='orders by customer'),
    path('active/customers/', views.ActiveCustomersView.as_view(), name='orders by customer'),
    path('orders_between_dates/', views.OrdersWithinDateRangeOrStatus.as_view(), name='orders between dates'),
]