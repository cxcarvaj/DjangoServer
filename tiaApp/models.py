from django.db import models

class DepartmentsF(models.Model):
    department_id = models.AutoField(primary_key=True)
    department = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'departments_f'


class OrdersF(models.Model):
    order_id = models.AutoField(primary_key=True)
    order_hour_of_day = models.PositiveIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'orders_f'


class ProductsF(models.Model):
    product_id = models.AutoField(primary_key=True)
    product_name = models.CharField(max_length=200)
    department = models.ForeignKey(DepartmentsF, models.DO_NOTHING)
    price = models.FloatField()
    margin = models.FloatField()

    class Meta:
        managed = False
        db_table = 'products_f'


class OrderProductsF(models.Model):
    order = models.ForeignKey('OrdersF', models.DO_NOTHING, blank=True, null=False, primary_key=True)
    product = models.ForeignKey('ProductsF', models.DO_NOTHING, blank=True, null=False)
    quantity = models.PositiveIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'order_products_f'