from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('',views.workstation_dashboard, name="workstation_dashboard"),
    
    path('order/<str:po_number>/box_cut/',views.box_cut, name="box_cut"),
    path('order/<str:po_number>/box_cut/confirm',views.confirm_box_cut, name="box_cut_confirm"),
    
    #search
    path('<str:job_type>/search/', views.job_search, name="job_search"),
    
    path('order/<str:po_number>/tube_cut/',views.tube_cut, name="tube_cut"),
    path('order/<str:po_number>/tube_cut/complete',views.confirm_tube_cut, name="tube_cut_confirm"),
    
    path('order/<str:po_number>/pre_assembly/',views.pre_assembly, name="pre_assembly"),
    path('order/<str:po_number>/pre_assembly/complete',views.confirm_pre_assembly, name="pre_assembly_confirm"),
    
    path('trap-prep/',views.pre_assembly, name="pre_assembly"),
    path('hardware/',views.hardware, name="hardware"),
    path('powder-coat/',views.powder_coat, name="powder_coat"),
    path('fabric/',views.fabric, name="fabric"),
    path('assembly/',views.assembly, name="assembly"),
    path('shipping/',views.shipping, name="shipping"),
]