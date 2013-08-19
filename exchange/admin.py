from django.contrib import admin
from exchange.models import Item, Notification, Pic

class ItemAdmin(admin.ModelAdmin):
    date_hierarchy = 'offered_date'
    list_display = ('name', 'offered_by', 'deleted', 'offered_date')


class NotificationAdmin(admin.ModelAdmin):
    date_hierarchy = 'date'
    list_display = ('sent_to', 'sent_from', 'item', 'date')


admin.site.register(Item, ItemAdmin)
admin.site.register(Notification, NotificationAdmin)
