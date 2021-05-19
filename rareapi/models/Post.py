from django.db import models
from django.utils import timezone

class Post(models.Model):

    user = models.ForeignKey("RareUser", on_delete=models.CASCADE)
    category = models.ForeignKey("Category", on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=50)
    publication_date = models.DateTimeField(default=timezone.now())
    image_url = models.ImageField(upload_to=None, height_field=None, width_field=None, max_length=100)
    content = models.CharField(max_length=200)
    approved = models.BooleanField(default=False)