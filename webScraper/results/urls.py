from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('ShowItems/<str:ch>/<int:id>/', views.show_items, name='ShowItems'),
]