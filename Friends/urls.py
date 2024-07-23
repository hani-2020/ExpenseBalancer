from django.urls import path
from . import views

urlpatterns = [
    path('', views.friends_page, name='friends_page')
]
