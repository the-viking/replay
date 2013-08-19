from django.db import models
import os
import datetime
from django.dispatch import receiver
from django.contrib.auth.models import User

class Item(models.Model):
    name = models.CharField(max_length=40)
    offered_date = models.DateTimeField(auto_now_add=True, blank=True)
    description = models.CharField(max_length=500)  
    offered_by = models.ForeignKey(User)
    image = models.FileField(upload_to='media/images/%Y')
    deleted = models.BooleanField(default=False)

    # by default, sort by reverse date added (most recently added first)
    class Meta:
            ordering = ['-offered_date']

    def __unicode__(self):
        return self.name

# indicates a notification from one user to another, requesting an item
class Notification(models.Model):
    # foreign keys for involved users, additional names to avoid clash
    sent_to = models.ForeignKey(User, related_name='notification_from')
    sent_from = models.ForeignKey(User, related_name='notification_to')
    item = models.ForeignKey(Item)
    date = models.DateTimeField(auto_now_add=True, blank=True)
    # indicates whether the notification is still visible. use visible() method instead
    visible = models.BooleanField()
    # optional field to indicate whether notification was accepted (not currently being used)
    accepted = models.NullBooleanField()

    def appears(self):
        """
        Returns a boolean for whether the notification should still be
        visible, based on the set expiration time
        """
        # set expiration time to be 5 days
        exp_time = datetime.timedelta(5)
        now = datetime.datetime.now(self.date.tzinfo)
        return now - self.date < exp_time 

    def __unicode(self):
        return "Sent to " + self.sent_to.username + "from" + self.sent_from.username
	

@receiver(models.signals.post_delete, sender=Item)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    """
    Deletes file from filesystem
    when corresponding 'Item' object is deleted.
    """
    if instance.image:
        if os.path.isfile(instance.image.path):
            os.remove(instance.image.path)
