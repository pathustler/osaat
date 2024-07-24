from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('',views.workstation_dashboard, name="workstation_dashboard"),
    
    path('order/<str:po_number>/box-cut/',views.box_cut, name="box_cut"),
    path('order/<str:po_number>/box-cut/complete',views.confirm_box_cut, name="box_cut_complete"),
    
    #search
    path('<str:job_type>/search/', views.job_search, name="job_search"),
    
    path('tube-cut/',views.tube_cut, name="tube_cut"),
    path('trap-prep/',views.track_prep, name="track_prep"),
    path('hardware/',views.hardware, name="hardware"),
    path('powder-coat/',views.powder_coat, name="powder_coat"),
    path('fabric/',views.fabric, name="fabric"),
    path('assembly/',views.assembly, name="assembly"),
    path('shipping/',views.shipping, name="shipping"),
]