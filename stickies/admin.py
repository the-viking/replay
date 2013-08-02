from django.contrib import admin
from stickies.models import Sticky

class StickyAdmin(admin.ModelAdmin):
    date_hierarchy = 'date'
    list_display = ('writer', 'date')

admin.site.register(Sticky, StickyAdmin)
