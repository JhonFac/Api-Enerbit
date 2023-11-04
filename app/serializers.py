from rest_framework import serializers

from .models import Customer, WorkOrder


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        exclude = ['created_at']

class WorkOrderSerializer(serializers.ModelSerializer):
    customer = CustomerSerializer(read_only=True)
    
    class Meta:
        model = WorkOrder
        exclude = ['created_at']
        depth = 1


    def create(self, validated_data):
        return WorkOrder.objects.create(**validated_data)
    
    def validate_status(self, value):
        if value not in ['New', 'Done', 'Cancelled']:
            raise serializers.ValidationError("El estado debe ser 'New', 'Done', o 'Cancelled'.")
        return value


class CustomerWithWorkOrdersSerializer(serializers.ModelSerializer):
    work_orders = WorkOrderSerializer(many=True, read_only=True)

    class Meta:
        model = Customer
        fields = ('id', 'first_name', 'last_name', 'address', 'start_date', 'end_date', 'is_active', 'created_at', 'work_orders')