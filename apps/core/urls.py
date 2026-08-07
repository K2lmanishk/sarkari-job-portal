from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('privacy-policy/', views.privacy, name='privacy'),
    path('disclaimer/', views.disclaimer, name='disclaimer'),
    path('terms-and-conditions/', views.terms, name='terms'),
    path('newsletter/subscribe/', views.newsletter_subscribe, name='newsletter_subscribe'),
]