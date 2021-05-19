from django.db import models

class DemotionQueue(models.Model):

    admin = models.ForeignKey("RareUser", on_delete=models.CASCADE, related_name="admin")
    approver = models.ForeignKey("RareUser", on_delete=models.SET_NULL, null=True, related_name="approver")
    action = models.CharField(max_length=50)