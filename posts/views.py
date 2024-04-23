from django.shortcuts import get_object_or_404, render, redirect
from .models import MissingPerson, Comment
from .forms import CommentReplyForm, MissingPersonForm, CommentForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMessage, send_mail
from django.conf import settings
from django.http import JsonResponse, HttpResponseBadRequest
import threading
from django.template.loader import render_to_string
from django.utils.html import strip_tags



"""
CRUD FOR THE POSTS:

Create - Create/post missing person's details
Read 1 - Read/view details of the missing person, both for the user who posted, and everyone else in the world
Read 2 - Read/view details of the missing person, both for the user who posted, and everyone else in the world: only viewing
Update - User who posted, is able to update the details of the missing person
Delete - User who posted is able to delete the missing person

"""

# Create post
@login_required(login_url='accounts:login')
def create_missing_person(request):
    """Upload missing person's details"""
    if request.method == 'POST':
        form = MissingPersonForm(request.POST, request.FILES)
        if form.is_valid():
            missing_person = form.save(commit=False)
            missing_person.user = request.user
            missing_person.save()
            user_email = request.user.email  # Get the email of the logged-in user who posted
            
            # Send email upon successful posting
            try:
                # Prepare email content
                site_url = request.build_absolute_uri('/')  # Get the site URL dynamically
                context = {
                    'user': request.user,
                    'missing_person': missing_person,
                    'site_url': site_url,  # Pass the site URL to the template context
                }
                html_message = render_to_string('email/create_post_notification.html', context)
                plain_message = strip_tags(html_message)

                email_message = EmailMessage(
                    subject="Post submitted successfully",  # Subject
                    body = plain_message,
                    # body=email_content,  # Email content
                    from_email=settings.EMAIL_HOST_USER,  # Sender's email
                    to=[user_email],  # Recipient email
                )
                email_message.send()
            except Exception as e:
                # Handle email sending failure
                raise Exception("Email sending failed: {}".format(str(e)))
            
            # End of email send
            messages.success(request, 'Your post is now live! We hope you find the person soon')
            return redirect('posts:posts_index')
        else:
            messages.error(request, "Oops! Failed to upload missing person's details")
    else:
        form = MissingPersonForm()
    context = {'form': form}
    return render(request, 'posts/create_missing_person.html', context)





# Read 1-- Display all posts
@login_required(login_url='accounts:login')
def posts_index(request):
    """
    Fetch and display all posts
    """
    posts = MissingPerson.objects.all().order_by('-created_at')
    # If the user has just posted, their post should appear first
    if request.user.is_authenticated:
        user_posts = posts.filter(user=request.user)
        if user_posts.exists():
            user_post = user_posts.first()
            other_posts = posts.exclude(pk=user_post.pk)
            posts = [user_post] + list(other_posts)
    
    # Fetch comments and reactions for each post
    post_data = []
    for post in posts:
        comments = post.comment_set.all()  # Retrieve comments for each post
        # reactions = post.reaction_set.all()  # Retrieve reactions for each post
        post_data.append({
            'post': post,
            'comments': comments,
            # 'reactions': reactions,
        })
    
    context = {'post_data': post_data}
    return render(request, 'posts/posts_index.html', context)



# Read 2 -- viewing the details: only viewing
@login_required(login_url='accounts:login')
def view_post_details(request, post_id):
    """
    View the particular post details
    """
    post = get_object_or_404(MissingPerson, pk=post_id)
    comments = post.comment_set.all().order_by('-timestamp')  # Retrieve comments for the post, ordered by timestamp descending

    context = {
        'post': post,
        'comments': comments,
    }
    return render(request, 'posts/view_post_details.html', context)



# Update
@login_required(login_url='accounts:login')
def update_post(request, post_id):
    """
    Update the details of the post

    """
    post = get_object_or_404(MissingPerson, pk=post_id)
    # Check if the current user is the owner of the post
    if post.user != request.user:
        messages.error(request, "You don't have permission to update this post.")
        return redirect('posts:posts_index')
    
    if request.method == 'POST':
        form = MissingPersonForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your post has been updated successfully!')
            return redirect('posts:posts_index')
        else:
            messages.error(request, 'Failed to update the post')
    else:
        form = MissingPersonForm(instance=post)
    context = {'form': form}
    return render(request, 'posts/update_post.html', context)


# Delete
@login_required(login_url='accounts:login')
def delete_post(request, post_id):
    """
    Delete the post

    """
    post = get_object_or_404(MissingPerson, pk=post_id)
    # Check if the user deleting is the one who posted
    if post.user != request.user:
        messages.error(request, "You don't have permission to delete this post")
        return redirect('posts:posts_index')
    
    if request.method == 'POST':
        post.delete()
        messages.success(request, 'Your post has been deleted successfully!')
        return redirect('posts:posts_index')



# Comment
@login_required(login_url='accounts/login')
def comment_on_post(request, post_id):
    post = get_object_or_404(MissingPerson, id=post_id)
    
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.post = post
            comment.save()
            
            # Notify the post owner
            messages.info(request, f'New comment on your post by {request.user.username}')
            
            # Send email asynchronously
            threading.Thread(target=send_email_async, args=(post, comment, request)).start()
            
            # Return a JSON response indicating success
            return JsonResponse({'success': True})
        else:
            # Return a JSON response with form errors if the form is not valid
            return JsonResponse({'success': False, 'errors': form.errors}, status=400)
    else:
        # Return a JSON response with an error if the request method is not POST
        return JsonResponse({'error': 'Invalid request method'}, status=405)



def send_email_async(post, comment, request):
    try:
        # Prepare email content
        subject = f'New comment on your post by {request.user.username}'
        context = {
            'user': post.user.username,
            'comment_user': request.user.username,
            'comment_text': comment.text,
            'post_url': request.build_absolute_uri(post.get_absolute_url())
        }
        html_message = render_to_string('email/comment_notification.html', context)
        plain_message = strip_tags(html_message)
        
        # Send email
        send_mail(
            subject,
            plain_message,
            settings.EMAIL_HOST_USER,
            [post.user.email],
            html_message=html_message,
        )
    except Exception as e:
        print(f"Email sending failed: {str(e)}")


# Reply to comment
@login_required(login_url='accounts/login')
def reply_to_comment(request, comment_id):
    if request.method == 'POST':
        comment_id = request.POST.get('comment_id')
        comment = get_object_or_404(Comment, id=comment_id)
        form = CommentReplyForm(request.POST)
        if form.is_valid():
            reply = form.save(commit=False)
            reply.user = request.user
            reply.comment = comment  # Assign the parent comment
            reply.save()
            messages.info(request, f'New reply to your comment by {request.user.username}')
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'errors': form.errors}, status=400)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)



# Liking
@login_required(login_url='accounts:login')
def react_to_post(request, post_id):
    if request.method == 'POST' and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        post = get_object_or_404(MissingPerson, pk=post_id)
        
        # Toggle like for the current user
        post.toggle_like(request.user)
        
        # Save the post instance to persist changes to the database
        post.save()
        
        # Get the updated like count for the post
        like_count = post.liked_by.count()
        
        # Return JSON response with the updated like count
        return JsonResponse({'likeCount': like_count})
    else:
        # Handle invalid request method or non-ajax request
        return HttpResponseBadRequest('Invalid request: AJAX request expected')

