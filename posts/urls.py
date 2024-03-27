from django.urls import path
from . import views

app_name = 'posts'


urlpatterns = [
    path('create_missing_person/', views.create_missing_person, name='create_missing_person'), # create_missing_person
    path('', views.posts_index, name='posts_index'), # display all posts
    path('<int:post_id>/', views.view_post_details, name='view_post_details'), # view particular post details
]