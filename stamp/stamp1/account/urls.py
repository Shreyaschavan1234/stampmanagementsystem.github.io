from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login, name='login'),
    path('face-login/', views.face_login, name='face-login'),
    path('logout/', views.logout, name='logout'),
]
