from django.db import models
from django.utils import timezone

class Comment(models.Model):

    author = models.ForeignKey("RareUser", on_delete=models.CASCADE)
    post = models.ForeignKey("Post", on_delete=models.CASCADE)
    content = models.CharField(max_length=100)
    created_on = models.DateField(default=timezone.now())