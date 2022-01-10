from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('NewlistItem/<int:id>/', views.new_list_item, name='NewlistItem'),
    path('ToplistItem/<int:id>/', views.top_list_item, name='ToplistItem'),
]