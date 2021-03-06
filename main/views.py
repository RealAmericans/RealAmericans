from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render, get_object_or_404
from .models import *
from .forms import *
from django .contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

# view allows you to add profile pic
@login_required(login_url='/login')
def add_pfp(request):
    form = pfpForm()
    if request.method == 'POST':
        form = pfpForm(request.POST)
        if form.is_valid:
            profilePic.objects.filter(user=str(request.user)).delete()
            form2 = form.save(commit=False)
            form2.user = request.user
            form2.save()
            return redirect('profile')

    return render(request, 'add_pfp.html', {'form':form})

@login_required(login_url='/login')
def notifications(request):
    notificationsmMention.objects.all().delete()
    # find @user in post
    def findPost(user,all):
        for i in all:
            if f'@{user}' in str(i):
                notificationsmMention.objects.create(myuser=user, user=i.user, to_pk=i.pk, date=i.date)
                
    # find @user in comment
    def findComment(user,all):
        for i in all:
            if f'@{user}' in str(i):
                notificationsmMention.objects.create(myuser=user, user=i.user, to_pk=i.to_pk, date=i.date)
    
    findPost(request.user, post.objects.all())
    findComment(request.user, comment.objects.all())
    return render(request, 'notifications.html', {'mentions':notificationsmMention.objects.filter(myuser=str(request.user))})

@login_required(login_url='/login')
def get_post(request, pk):
    form = CommentForm()
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            form2 = form.save(commit=False)
            form2.user = request.user
            form2.to_pk = pk
            form2.save()
            
    get_post = post.objects.filter(pk=pk)
    comments = comment.objects.filter(to_pk=pk)
    all_ver = ver.objects.all()
    pic = profilePic.objects.all()
    c = 0
    for i in clicked.objects.filter(to_pk=pk):
        c = int(i.click)
    clicks = clicked.objects.create(to_pk = pk, click=c+1)
    return render(request, 'post.html', {'clicks':clicks,'post':get_post, 'form':form,'comments':comments, 'pic':pic,'all_ver':all_ver, 'User':str(request.user), })

def Logout(request):
    logout(request)
    return redirect('login') 

def signup(request):
    form = UserCreationForm()
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid:
            form.save()
            return redirect('login') 
    return render(request, 'signup.html', {'form':form})

def Login(request):
    pic = profilePic.objects.filter(user=str(request.user))
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'login.html', {'msg':['your username or password is incorrect'], 'pic':pic})
    return render(request, 'login.html', {'pic':pic})

@login_required(login_url='/login')
def get_topic(request, pk):
    return render(request, 'topic.html', {'topic':topic.objects.filter(pk=pk), 'all_post':post.objects.all(), 'pic':profilePic.objects.all()})

@login_required(login_url='/login')
def home(request):
    topics = topic.objects.all
    all_post = post.objects.all()
    pic = profilePic.objects.all()
    all_ver = ver.objects.all()
    form = PostForm()
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid:
            form2 = form.save(commit=False)
            form2.user = request.user
            form2.save()

    return render(request, 'home.html', {'topics':topics, 'post_form':form,'all_post':all_post, 'User':str(request.user), 'pic':pic,'all_ver':all_ver})

@login_required(login_url='/login')
def profile(request):
    get_post = post.objects.filter(user=str(request.user))
    all_ver = ver.objects.all()
    pic = profilePic.objects.filter(user=str(request.user))
    return render(request, 'profile.html', {'get_post':get_post,'User':str(request.user), 'pic':pic,'all_ver':all_ver})

