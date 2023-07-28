from django.db import models


class BaseModel(models.Model):
    objects = models.Manager()  # we can create active and inactive managers

    class Meta:
        abstract = True
