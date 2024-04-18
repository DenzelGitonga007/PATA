from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from .models import Conversation
from .forms import MessageForm
from django.contrib.auth import get_user_model
import json
from django.http import JsonResponse

User = get_user_model()

# Display the conversations list
@login_required(login_url='accounts/login')
def conversation_list(request):
    """Display the conversation"""
    # Fetch all conversations involving the current user
    conversations = Conversation.objects.filter(participants=request.user)
    context = {
        'conversations': conversations
        }
    return render(request, 'chat/conversation_list.html', context)


# See the messages in the conversation
# views.py
@login_required(login_url='accounts/login')
def conversation_detail(request, conversation_id):
    """See the messages in the conversation"""
    conversation = get_object_or_404(Conversation, id=conversation_id)
    messages = conversation.messages.all()

    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.conversation = conversation
            message.sender = request.user
            message.save()
            return JsonResponse({'status': 'success'})
        else:
            return JsonResponse({'status': 'error', 'errors': form.errors}, status=400)
    else:
        form = MessageForm()

    context = {
        'conversation': conversation,
        'messages': messages,
        'form': form  # Pass the message form to the template
    }
    return render(request, 'chat/conversation_detail.html', context)


# Launch chat session
@login_required(login_url='accounts/login')
def start_conversation(request, username):
    """Launch chat session"""
    # Retrieve the user object corresponding to the username
    recipient = get_object_or_404(User, username=username)

    # Check if a conversation already exists between the users
    existing_conversation = Conversation.objects.filter(participants=request.user).filter(participants=recipient)

    if existing_conversation.exists():
        # Redirect to the existing conversation
        return redirect('chat:conversation_detail', conversation_id=existing_conversation.first().id)
    else:
        # Create a new conversation
        new_conversation = Conversation.objects.create()
        new_conversation.participants.add(request.user, recipient)
        new_conversation.save()

        # Redirect to the newly created conversation
        return redirect('chat:conversation_detail', conversation_id=new_conversation.id)
