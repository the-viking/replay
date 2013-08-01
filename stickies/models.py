from django.db import models
from django.contrib.auth.models import User

class Sticky(models.Model):
    
    writer = models.ForeignKey(User)
    message = models.CharField(max_length=75)
    date = models.DateTimeField(auto_now_add=True, blank=True)
