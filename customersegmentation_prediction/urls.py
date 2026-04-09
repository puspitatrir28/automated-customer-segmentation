from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('analytics/', views.analytics_view, name='analytics'),
    path('form/', views.prediction_form_view, name='prediction_form'),
    path('customers/', views.customer_data_view, name='customer_data'),
    path('export-customers/', views.export_customer_csv, name='export_customers'),
]