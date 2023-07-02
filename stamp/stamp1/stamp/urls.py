from django.urls import path
from . import views

urlpatterns = [
    # path('stamps-ajax-data-1/', views.myModel_asJson, name="ajax-stamp-data-1"), 
    path('stamps-ajax-data/', views.ItemListView.as_view(), name="ajax-stamp-data"), 
    path('stamps-data', views.index, name='stamp-index'),
    path('types', views.stamp_types, name='stamp-types'),
    path('types/edit/<int:pk>', views.stamp_types_edit, name='stamp-types-edit'),
]
