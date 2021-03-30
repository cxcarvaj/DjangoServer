from django.contrib import admin

# Register your models here.
from tiaApp.models import DepartmentsF, OrdersF, ProductsF, OrderProductsF
from django.contrib import admin
admin.site.register(DepartmentsF)
admin.site.register(OrdersF)
admin.site.register(ProductsF)
admin.site.register(OrderProductsF)