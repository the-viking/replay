from django.contrib import admin
from admin_extension.models import Info, Profile
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

class InfoAdmin(admin.ModelAdmin):
    readonly_fields = ('name',)


admin.site.register(Info, InfoAdmin)

# Define an inline admin descriptor for Employee model
# which acts a bit like a singleton
class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'profile'

# Define a new User admin
class UserAdmin(UserAdmin):
    inlines = (ProfileInline, )

# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)

admin.site.register(Profile)
