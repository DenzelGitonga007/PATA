from django.urls import path
from . import views

app_name = 'posts'


urlpatterns = [
    path('create_missing_person/', views.create_missing_person, name='create_missing_person'), # create_missing_person
    path('', views.posts_index, name='posts_index'), # display all posts
    path('<int:post_id>/', views.view_post_details, name='view_post_details'), # view particular post details
    path('update/<int:post_id>/', views.update_post, name='update_post'), # update post details
    path('delete/<int:post_id>/', views.delete_post, name='delete_post'), # delete post

    # Reactions
    path('comment/<int:post_id>/', views.comment_on_post, name='comment_on_post'),
    path('react/<int:post_id>/', views.react_to_post, name='react_to_post'),
]