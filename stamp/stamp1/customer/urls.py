from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='customer-index'),
    path('create', views.create, name='customer-create'),
    path('edit/<int:pk>', views.edit, name='customer-edit'),
    path('camera/<int:pk>', views.camera, name='customer-camera'),
]
