from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('NewlistItem/<int:id>/', views.NewlistItem, name='NewlistItem'),
    path('ToplistItem/<int:id>/', views.ToplistItem, name='ToplistItem'),
]