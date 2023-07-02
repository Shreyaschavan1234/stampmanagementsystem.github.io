from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='su-face-index'),
    path('dataset/<int:pk>', views.create_dataset, name='su-create-dataset'),
    path('faces', views.face_train, name='su-train-faces'),
    path('test', views.test, name='su-train-test'),
]