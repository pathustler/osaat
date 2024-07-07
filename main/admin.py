from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

# Register your models here.
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import Customer, WasabiGallery, Timeline, CustomerFile, Order,Unit, Crew, TechnicianEvent, SalesEvent, GroupedJob, DeliveryEvent, Document,GalleryImage

class UserAdmin(BaseUserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'display_groups')
    
    def display_groups(self, obj):
        return ", ".join([group.name for group in obj.groups.all()])
    display_groups.short_description = 'Groups'

@admin.register(Crew)
class CrewAdmin(admin.ModelAdmin):
    list_display = ('name', 'crew_type')
    search_fields = ('name__username', 'crew_type')
    list_filter = ('crew_type',)

@admin.register(TechnicianEvent)
class TechnicianEventAdmin(admin.ModelAdmin):
    list_display = ('id','technician', 'order', 'visit_type', 'start_time', 'end_time')
    search_fields = ('technician__name__username', 'order__po_number', 'visit_type', 'status')
    list_filter = ('visit_type', 'start_time', 'end_time')

@admin.register(SalesEvent)
class SalesEventAdmin(admin.ModelAdmin):
    list_display = ('salesperson', 'order', 'title', 'main_phone', 'address', 'status', 'start_time', 'end_time')
    search_fields = ('salesperson__name__username', 'order__po_number', 'title', 'address', 'status')
    list_filter = ('status', 'start_time', 'end_time')

@admin.register(GroupedJob)
class GroupedJobAdmin(admin.ModelAdmin):
    list_display = ('order', 'title', 'done')
    search_fields = ('order__po_number', 'title')
    list_filter = ('done',)

@admin.register(DeliveryEvent)
class DeliveryEventAdmin(admin.ModelAdmin):
    list_display = ('title', 'address', 'start_time', 'end_time')
    search_fields = ('title', 'address')
    list_filter = ('start_time', 'end_time')
    filter_horizontal = ('jobs',)



admin.site.register(Customer)
admin.site.register(WasabiGallery)
admin.site.register(Timeline)
admin.site.register(CustomerFile)
admin.site.register(Order)
admin.site.register(Unit)
admin.site.register(Document)
admin.site.register(GalleryImage)




admin.site.unregister(User)
admin.site.register(User, UserAdmin)