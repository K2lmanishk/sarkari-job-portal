from django.urls import path
from . import views

app_name = 'answer_keys'

urlpatterns = [
    path('', views.answer_key_list, name='answer_key_list'),
    path('<slug:slug>/', views.answer_key_detail, name='answer_key_detail'),
]