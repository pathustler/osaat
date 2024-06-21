from django.contrib import admin

# Register your models here.
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import Customer, WasabiGallery, Timeline, WasabiFile

class UserAdmin(BaseUserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'display_groups')
    
    def display_groups(self, obj):
        return ", ".join([group.name for group in obj.groups.all()])
    display_groups.short_description = 'Groups'


admin.site.register(Customer)
admin.site.register(WasabiGallery)
admin.site.register(Timeline)
admin.site.register(WasabiFile)

admin.site.unregister(User)
admin.site.register(User, UserAdmin)