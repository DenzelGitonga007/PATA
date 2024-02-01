from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('register/', views.user_creation_view, name='register'), # register url
    path('login/', views.authentication_view, name='login'), # login url
    path('logout/', views.logout, name='logout'), # logout user
    path('', views.home, name='home') # the home page

]