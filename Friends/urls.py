from django.urls import path
from . import views

urlpatterns = [
    path('', views.friends_page, name='friends_page'),
    path('send_request/<int:id>/', views.send_request, name='send_request'),
    path('pending_requests/', views.pending_requests, name='pending_requests'),
    path('accept_request/<int:id>/', views.accept_request, name='accept_request'),
    path('reject_request/<int:id>/', views.reject_request, name='reject_request'),
    path('see_friends', views.see_friends, name='see_friends')
]
