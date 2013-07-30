from django.db import models
import os
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.db.models.signals import post_save

class Item(models.Model):
    class Meta:
            ordering = ['offered_date']
    name = models.CharField(max_length=200)
    offered_date = models.DateTimeField(auto_now_add=True, blank=True)
    description = models.CharField(max_length=500)  
    offered_by = models.ForeignKey(User)
    image = models.FileField(upload_to='media/images/%Y')
    def __unicode__(self):
        return self.name

# indicates a notification from one user to another, requesting an item
class Notification(models.Model):
	sent_to = models.ForeignKey(User, related_name='notification_from')
	sent_from = models.ForeignKey(User, related_name='notification_to')
	item = models.ForeignKey(Item)
	date = models.DateTimeField(auto_now_add=True, blank=True)
	visible = models.BooleanField()
	accepted = models.NullBooleanField()
	def __unicode(self):
		return "Sent to " + self.sent_to.username + "from" + self.sent_from.username
	
# model to extend the default User model with a few other optional fields
class Profile(models.Model):
	user = models.OneToOneField(User)
	picture = models.FileField(upload_to='media/profile_pictures', blank=True, null=True)
	telephone = models.CharField(max_length=12, blank=True, null=True)
	address = models.CharField(max_length=500, blank=True, null=True)

@receiver(models.signals.post_delete, sender=Item)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    """Deletes file from filesystem
    when corresponding 'Item' object is deleted.
    """
    if instance.image:
        if os.path.isfile(instance.image.path):
            os.remove(instance.image.path)
