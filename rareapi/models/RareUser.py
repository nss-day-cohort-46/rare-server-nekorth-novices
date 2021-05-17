from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class RareUser(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.CharField(max_length=50)
    created_on = models.DateField(default=timezone.now())
    active = models.BooleanField()
    profile_image = models.ImageField(upload_to=None, height_field=None, width_field=None, max_length=100)