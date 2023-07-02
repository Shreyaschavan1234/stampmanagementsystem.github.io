from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='sell-index'),
    path('create', views.create, name='sell-create'),
    path('customer/<int:pk>', views.customer, name='sell-customer'),
    path('ajax/get_stamp_details', views.get_stamp_details, name='get-stamp-details'),
    path('info/<int:pk>', views.info, name='sell-info'),
]
