from django.db import models
from location.models import Location
from stamp.models import StampType
from django.utils import timezone

# Create your models here.
class Purchase(models.Model):
    location = models.ForeignKey(Location, on_delete=models.CASCADE, null=True, blank=True)
    stamp_type = models.ForeignKey(StampType, on_delete = models.CASCADE, null=True, blank=True)
    code = models.CharField(max_length=10, null=True, blank=True)
    series_start = models.BigIntegerField(default=0)
    series_end = models.BigIntegerField(default=0)
    quantity = models.IntegerField(default=0)
    amount = models.FloatField(default=0)
    total = models.FloatField(default=0)
    date = models.DateField(default = timezone.now)

    # def __str__(self):
    #     return self.name

    class Meta:
        db_table = 'purchases'