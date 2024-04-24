from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('register/', views.user_creation_view, name='register'), # register url
    path('login/', views.authentication_view, name='login'), # login url
    path('logout/', views.logout_user, name='logout'), # logout user
    path('', views.home, name='home'), # the home page
    path('profile/<str:username>/', views.user_profile, name='user_profile'), # view users profile
    path('faq/', views.faqs, name='faqs'), # faqs
    path('user_profile_report/', views.user_profile_report, name='user_profile_report'),
]
