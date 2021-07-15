from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()

class Website(models.Model):
    Link = models.CharField(max_length=200, blank=True)
    

    def __str__(self):
        return "{}".format(self.pk)

class Message(models.Model):
    website = models.ForeignKey(Website, null=True, blank=True, on_delete=models.CASCADE)
    content = models.TextField()
    username =  models.CharField(max_length=200, blank=True)
    user = models.ForeignKey(
        User, related_name='messages', on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username





