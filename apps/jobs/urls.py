from django.urls import path
from . import views

app_name = 'jobs'

urlpatterns = [
    path('', views.job_list, name='job_list'),
    path('search/', views.job_search, name='job_search'),
    path('<slug:slug>/', views.job_detail, name='job_detail'),
    path('category/<slug:category_slug>/', views.job_by_category, name='job_by_category'),
    path('state/<slug:state_slug>/', views.job_by_state, name='job_by_state'),
    path('qualification/<str:qualification>/', views.job_by_qualification, name='job_by_qualification'),
]