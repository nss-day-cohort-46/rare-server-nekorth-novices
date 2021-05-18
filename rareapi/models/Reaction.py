from django.db import models

class Reaction(models.Model):

    label = models.CharField(max_length=50)
    image_url = models.ImageField(upload_to="reaction_images", height_field=None, width_field=None, max_length=100)
    posts = models.ManyToManyField("Post", through="PostReaction")
    users = models.ManyToManyField("RareUser", through="PostReaction")
