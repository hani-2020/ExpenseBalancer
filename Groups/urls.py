from django.urls import path
from . import views

urlpatterns = [
    path('create_groups', views.create_groups, name='create_groups'),
    path('view_groups', views.view_groups, name='view_groups'),
    path('edit_group/<int:id>/', views.edit_group, name='edit_group'),
    path('delete_group/<int:id>/', views.delete_group, name='delete_group'),
    path('leave_group/<int:id>/', views.leave_group, name='leave_group'),
    path('join_group/<int:group_id>/<int:user_id>', views.join_group, name='join_group')
]