from django.urls import path
from . import views

urlpatterns = [
    path('create_expense/<int:id>', views.create_expense, name='create_expense'),
    path('save_split/<int:expense_id>/', views.save_split, name='save_split')
]
