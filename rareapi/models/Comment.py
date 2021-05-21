from django.db import models
from django.utils import timezone

class Comment(models.Model):

    author = models.ForeignKey("RareUser", on_delete=models.CASCADE)
    post = models.ForeignKey("Post", on_delete=models.CASCADE)
    content = models.CharField(max_length=100)
    created_on = models.DateTimeField(default=timezone.now())

    @property
    def owner(self):
        return self.__owner

    @owner.setter
    def owner(self, value):
        print("ownership comment")
        if value == self.author :
            print("true")
            self.__owner = True
        else :
            self.__owner = False