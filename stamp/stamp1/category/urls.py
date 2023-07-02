from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='stamp-cats'),
    path('edit/<int:pk>', views.edit, name='stamp-cats-edit'),
]
