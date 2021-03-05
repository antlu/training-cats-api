from django.urls import path

from api import views

urlpatterns = [
    path('ping/', views.ping),
    path('cats/', views.cats_list, name='cats_list'),
]
