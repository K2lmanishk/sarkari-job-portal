from django.urls import path
from . import views

app_name = 'syllabus'

urlpatterns = [
    path('', views.syllabus_list, name='syllabus_list'),
    path('<slug:slug>/', views.syllabus_detail, name='syllabus_detail'),
]