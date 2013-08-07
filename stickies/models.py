from django.db import models
from django.contrib.auth.models import User

class Sticky(models.Model):
    """ 
    Stores information about the sticky 
    notes on the ask page of the community 
    section 
    """
    writer = models.ForeignKey(User)
    message = models.CharField(max_length=75)
    date = models.DateTimeField(auto_now_add=True, blank=True)
