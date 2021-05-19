from django.db import models
from django.db.models.constraints import UniqueConstraint

class Category(models.Model):

    label = models.CharField(max_length=50, unique=True)