from django.db import models

class PostReaction(models.Model):

    post = models.ForeignKey("Post", on_delete=models.CASCADE)
    reaction = models.ForeignKey("Reaction", on_delete=models.CASCADE)
    user = models.ForeignKey("RareUser", on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['post','reaction','user'], name='unique_post_reaction')
        ]