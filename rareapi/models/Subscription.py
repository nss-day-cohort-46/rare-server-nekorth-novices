from django.db import models
from django.utils import timezone

class Subscription(models.Model):

    follower = models.ForeignKey("RareUser", related_name="follower", on_delete=models.CASCADE)
    author = models.ForeignKey("RareUser", related_name="author", on_delete=models.CASCADE)
    created_on = models.DateTimeField(default=timezone.now())
    ended_on = models.DateTimeField(null=True)
