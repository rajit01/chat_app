from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from .models import Message, UserStatus

from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse
from .models import Message, UserStatus

def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            UserStatus.objects.create(user=user) 
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'chat/signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'chat/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def home(request):
    users = User.objects.exclude(id=request.user.id)
    return render(request, 'chat/home.html', {'users': users})


# @login_required
# def chat_room(request, username):
#     other_user = User.objects.get(username=username)
#     messages = Message.objects.filter(
#         sender__in=[request.user, other_user],
#         receiver__in=[request.user, other_user]
#     ).order_by('timestamp')
#     user_status = UserStatus.objects.filter(user=other_user).first()
#     return render(request, 'chat/chat_room.html', {
#         'other_user': other_user,
#         'messages': messages,
#         'user_status': user_status,
#     })

from django.shortcuts import get_object_or_404

@login_required
def chat_room(request, username):
    receiver = get_object_or_404(User, username=username)
    return render(request, 'chat/chat_room.html', {
        'receiver': receiver
    })

from channels.db import database_sync_to_async


@database_sync_to_async
def save_message(self, sender_username, receiver_username, message):
    try:
        sender = User.objects.get(username=sender_username)
        receiver = User.objects.get(username=receiver_username)
        Message.objects.create(sender=sender, receiver=receiver, content=message)
        print(f"✅ Message saved: {message}")
    except Exception as e:
        print("❌ Error saving message:", e)
