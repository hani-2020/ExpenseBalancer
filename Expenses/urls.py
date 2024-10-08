from django.urls import path
from . import views

urlpatterns = [
    path('create_expense/<int:id>', views.create_expense, name='create_expense'),
    path('save_split/<int:expense_id>/', views.save_split, name='save_split'),
    path('view_expenses', views.view_expenses, name='view_expenses'),
    path('view_group_expenses/<int:group_id>/', views.view_group_expenses, name='view_group_expenses'),
    path('view_expense_breakup/<int:expense_id>', views.view_expense_breakup, name='view_expense_breakup'),
    path('edit_expense/<int:expense_id>', views.edit_expense, name='edit_expense'),
    path('delete_expense/<int:expense_id>/', views.delete_expense, name='delete_expense'),
    path('pay_expense/<int:split_id>/', views.pay_expense, name='pay_expense'),
    path('debtors_creditors/', views.debtors_creditors, name="debtors_creditors")
]
