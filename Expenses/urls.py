from django.urls import path
from . import views

urlpatterns = [
    path('', views.create_expense, name='create_expense'),
]
