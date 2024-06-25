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
    path('customer/<str:unique_code>/timeline/create/', views.timeline_create, name='timeline_create'),
    path('customer/<str:unique_code>/order/create', views.order, name="order"),
    path('customer/<str:unique_code>/order/<str:po_number>/unit', views.unit, name="unit"),
    path('delete_event/<int:event_id>/', views.delete_event, name='delete_event'),
    path('customer/<str:unique_code>/order/<str:po_number>', views.order_info, name="orderinfo"),
]