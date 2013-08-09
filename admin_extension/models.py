from django.db import models
from django.contrib.auth.models import User

class Info(models.Model):
    name = models.CharField(max_length=50)
    text = models.TextField(max_length=2000)
    def __unicode__(self):
        return self.name

# model to extend the default User model with a few other optional fields
class Profile(models.Model):
    user = models.OneToOneField(User)
    picture = models.FileField(upload_to='media/profile_pictures', blank=True, null=True)
    telephone = models.CharField(max_length=20, blank=True, null=True)
    address = models.CharField(max_length=500, blank=True, null=True)
    def __unicode__(self):
        return self.user.username
