from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(Account)
admin.site.register(Champions)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Customer)

