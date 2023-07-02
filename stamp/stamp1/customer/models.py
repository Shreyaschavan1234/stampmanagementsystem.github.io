from django.db import models

# Create your models here.
class Customer(models.Model):
    name = models.CharField(max_length=100)
    aadhaar = models.CharField(max_length=12, unique=True)
    mobile = models.CharField(max_length=10)
    state = models.CharField(max_length=100)
    district = models.CharField(max_length=100)
    tehsil = models.CharField(max_length=100)
    town = models.CharField(max_length=100)
    pincode = models.IntegerField()
    image = models.ImageField(upload_to="customers/", null = True, blank = True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'customers'