from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='location-index'),
    path('edit/<int:pk>', views.edit, name='location-edit'),
]
