import uuid

from django.db import models
from django.forms import CharField, IntegerField


class StatusChoices(models.TextChoices):
    NEW = 'New', 'New'
    DONE = 'Done', 'Done'
    CANCELLED = 'Cancelled', 'Cancelled'


class Customer(models.Model):
    id = models.UUIDField(primary_key=True, editable=False)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    start_date = models.DateTimeField(null=True)
    end_date = models.DateTimeField(null=True)
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


    def save(self, *args, **kwargs):
        if not self.id:
            self.id = uuid.uuid4()
        super(Customer, self).save(*args, **kwargs)


class WorkOrder(models.Model):
    id = models.UUIDField(primary_key=True, editable=False)
    customer_id = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='work_orders')
    title = models.CharField(max_length=255)
    planned_date_begin = models.DateTimeField()
    planned_date_end = models.DateTimeField()
    status = models.CharField(max_length=20, choices=StatusChoices.choices, default=StatusChoices.NEW)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Work Order {self.id} for {self.customer_id.first_name} {self.customer_id.last_name}"

    def save(self, *args, **kwargs):
        if not self.id:
            self.id = uuid.uuid4()
        super(WorkOrder, self).save(*args, **kwargs)
