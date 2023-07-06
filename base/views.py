from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from .forms import TweetForm
from .models import Profile, Tweet


def login_page(request):
    if request.method == 'POST':
        username =request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'User does not exist')
        
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('base:dashboard')
        else:
            messages.error(request, 'Username or password is incorrect')

    return render(request, 'base/login.html', {})


def register_page(request):
    form = UserCreationForm()
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('base:dashboard')
        else:
            messages.error(request, 'An error occurred during registration')

    context = {'form': form}
    return render(request, 'base/register.html', context)


def logout_page(request):
    logout(request)
    return redirect('base:dashboard')


def dashboard(request):
    if request.user.is_authenticated:
        form = TweetForm(request.POST or None)
        if request.method == 'POST':
            form = TweetForm(request.POST)
            if form.is_valid():
                tweet = form.save(commit=False)
                tweet.user = request.user
                tweet.save()
                return redirect('base:dashboard')
        
        followed_tweets = Tweet.objects.filter(user__profile__in=request.user.profile.follows.all()).order_by('-created_at')

        context = {'form':form, 'tweets':followed_tweets}
        return render(request, 'base/dashboard.html', context)
    else: 
        tweets = Tweet.objects.all()
        context = {'tweets':tweets}
        return render(request, 'base/dashboard.html', context)


def profile_list(request):
    profiles = Profile.objects.exclude(user=request.user)
    
    context = {'profiles': profiles}
    return render(request, 'base/profile_list.html', context)


def profile(request, pk):
    if not hasattr(request.user, 'profile'):
        missing_profile = Profile(user=request.user)
        missing_profile.save()

    profile = Profile.objects.get(id=pk)

    if request.method == 'POST':
        current_user_profile = request.user.profile
        data = request.POST
        action = data.get('follow')
        if action == 'follow':
            current_user_profile.follows.add(profile)
        elif action == 'unfollow':
            current_user_profile.follows.remove(profile)
        current_user_profile.save()

    context = {'profile': profile}
    return render(request, 'base/profile.html', context)



def delete_tweet(request, id):
    tweet = Tweet.objects.get(id=id)

    if request.user != tweet.user:
        messages.error(request, "You don't have permission to delete this tweet!")

    else:
        tweet.delete()
        return redirect('base:dashboard')
    
    return render(request, 'base/delete.html', context={'tweet':tweet})





