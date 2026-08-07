from django.urls import path
from . import views

app_name = 'results'

urlpatterns = [
    path('', views.result_list, name='result_list'),
    path('<slug:slug>/', views.result_detail, name='result_detail'),
]