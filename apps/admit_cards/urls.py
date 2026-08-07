from django.urls import path
from . import views

app_name = 'admit_cards'

urlpatterns = [
    path('', views.admit_card_list, name='admit_card_list'),
    path('<slug:slug>/', views.admit_card_detail, name='admit_card_detail'),
]