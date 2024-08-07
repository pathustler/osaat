from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from .forms import CustomAuthenticationForm

urlpatterns = [
    path('', views.index, name='index'),
    path('accounts/login/', auth_views.LoginView.as_view(
        template_name='main/login.html',
        authentication_form=CustomAuthenticationForm
    ), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
    path("customer/<str:unique_code>/", views.customer, name="customer"),
    path("customer/<str:unique_code>/schedule", views.schedule, name="schedule"),
    path('customer/<str:unique_code>/timeline/create/', views.timeline_create, name='timeline_create'),
    path('customer/<str:unique_code>/order/create', views.order_wizard, name="order"),
    path('delete_event/<int:event_id>/', views.delete_event, name='delete_event'),
    path('customer/<str:unique_code>/order/<str:po_number>', views.order_info, name="orderinfo"),
    path('customer/<str:unique_code>/order/<str:po_number>/confirmation', views.confirmation, name="confirmation"),
    path('customer/<str:unique_code>/order/<str:po_number>/place_order', views.place_order, name="place_order"),
    path('orderplaced', views.order_already_placed_error, name="order_already_placed_error"),
    path('search/', views.search, name='search'),
    
    #CALENDARS
    path('calendar/technician_calendar', views.technician_calendar, name='technician_calendar'),
    path('api/technician_events/', views.get_technician_events, name='get_technician_events'),
    path('calendar/technician_calendar/delete_event/<int:event_id>/', views.delete_technician_event, name='delete_technician_event'),
    path('calendar/technician_calendar/update-event/<int:event_id>/', views.update_technician_event, name='update_technician_event'),
    
    path('calendar/sales_calendar', views.sales_calendar, name='sales_calendar'),
    path('api/sales_events/', views.get_sales_events, name='get_sales_events'),
    path('calendar/sales_calendar/delete_event/<int:event_id>/', views.delete_sales_event, name='delete_sales_event'),
    path('calendar/sales_calendar/update-event/<int:event_id>/', views.update_sales_event, name='update_sales_event'),
    
    path('calendar/delivery_calendar', views.delivery_calendar, name='delivery_calendar'),
    path('api/delivery_events/', views.get_delivery_events, name='get_delivery_events'),
    path('calendar/delivery_calendar/delete_event/<int:event_id>/', views.delete_delivery_event, name='delete_delivery_event'),
    path('calendar/delivery_calendar/update-event/<int:event_id>/', views.update_delivery_event, name='update_delivery_event'),
    path('calendar/delivery_calendar/schedule-event/<int:event_id>/', views.schedule_delivery_event, name='schedule_delivery_event'),
    
    #STORAGE
    path('storage/documents/', views.document_list, name='document_list'),
    path('storage/gallery/', views.gallery, name='gallery'),
    path('storage/browser/', views.file_browser, name='file_browser'),
    path('storage/browser/contents/', views.folder_contents, name='folder_contents'),
    
  
    
]