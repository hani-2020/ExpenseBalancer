from django.urls import path
from . import views

urlpatterns = [
    path('create_groups', views.create_groups, name='create_groups')
]