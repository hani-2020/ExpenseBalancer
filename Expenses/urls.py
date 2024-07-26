from django.urls import path
from . import views

urlpatterns = [
    path('create_expense/<int:id>', views.create_expense, name='create_expense'),
]
