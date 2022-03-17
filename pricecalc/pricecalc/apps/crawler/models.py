from django.db import models



class Ldstp(models.Model):
    title = models.CharField(max_length=128)
    price = models.DecimalField(decimal_places=2, max_digits=8)
    availability = models.CharField(max_length=32)
