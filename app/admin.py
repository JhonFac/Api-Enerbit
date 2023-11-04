from django.contrib import admin

from .models import Customer, WorkOrder

admin.site.register(WorkOrder)
admin.site.register(Customer)
