from django.urls import path
from django.contrib.auth import views as authviews
from . import views

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('login/', views.userlogin, name='login'),
    path('logout/', authviews.LogoutView.as_view(), name='logout'),
    path('', views.home, name='homepage')
]
