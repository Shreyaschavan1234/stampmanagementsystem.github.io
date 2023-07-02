from django.db import models
from location.models import Location
# from purchase.models import Purchase
from customer.models import Customer
from category.models import Category

# Create your models here.
class StampType(models.Model):
    name = models.CharField(max_length=100)
    number = models.IntegerField()
    base_price = models.FloatField()
    image = models.ImageField(upload_to = 'products/', blank = True, null = True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'stamp_types'

# class StampPurchase(models.Model):
#     purchase = models.ForeignKey(Purchase, on_delete=models.CASCADE)
#     stamp_type = models.ForeignKey(StampType, on_delete = models.CASCADE)
#     purchase_price = models.FloatField()
#     amount = models.FloatField(null=True, blank=True)
#     initial_code = models.CharField(max_length=10)
#     location = models.ForeignKey(Location, on_delete = models.CASCADE)
#     series_start = models.BigIntegerField()
#     series_end = models.BigIntegerField()
#     quantity = models.IntegerField()
#     date = models.DateField()
#     time = models.TimeField()

#     def __str__(self):
#         return self.name

#     class Meta:
#         db_table = 'stamp_purchases'

class Stamp(models.Model):
    # purchase = models.ForeignKey(Purchase, on_delete=models.CASCADE)
    stamp_type = models.ForeignKey(StampType, on_delete=models.CASCADE)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    code = models.CharField(max_length=10, null=True, blank=True)
    number = models.BigIntegerField(null=True, blank=True)
    code_number = models.CharField(max_length=20, unique=True, null=True, blank=True)
    sold = models.BooleanField(default=False)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True, blank=True)
    corresponding_person = models.CharField(max_length=200, null=True, blank=True)
    base_amount = models.FloatField(default=0)
    additional_amount = models.FloatField(default=0)
    total_amount = models.FloatField(default=0)
    title = models.TextField(null=True, blank=True)
    purpose = models.TextField(null=True, blank=True)
    file = models.FileField(upload_to='stamp_files/', null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True)
    date = models.DateField(null=True, blank=True)
    time = models.TimeField(null=True, blank=True)
    datetime = models.DateTimeField(null=True, blank=True)
    paid_with = models.CharField(max_length=10, null=True, blank=True)
    notes = models.CharField(max_length=200, null=True, blank=True)
    transaction_id = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'stamps'
