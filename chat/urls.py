from django.urls import path
from . import views
app_name = 'chat'


urlpatterns = [
    path('conversations/', views.conversation_list, name='conversation_list'), # conversation list
    path('conversation/<int:conversation_id>/', views.conversation_detail, name='conversation_detail'), # messages in the conversation
    path('start-conversation/<str:username>/', views.start_conversation, name='start_conversation'), # start the conversation
]