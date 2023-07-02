from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='purchase-index'),
    path('create', views.create, name='purchase-create'),
]
