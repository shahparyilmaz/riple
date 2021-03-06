from django.shortcuts import render,redirect
from django.http import HttpResponse
import random
from django.http import JsonResponse
from django.forms.models import model_to_dict
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from .forms import *
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import *
from datetime import datetime,date
from django.core.signals import request_finished
from django.dispatch import receiver
from .decorators import *


def test(request):
    return render(request,'app/test.html')

def css(request):
    return render(request,'app/css.html')

@login_required(login_url='login')
def home(request):
    user = request.user
    notifications=Notification.objects.filter(user=user).order_by('-time')
    feed_list=FeedPost.objects.filter(users=user).order_by('-time')
    all_notifications=Notification.objects.filter(user=user).order_by('-time')
    follow_req_notifications=Notification.objects.filter(user=user,notification_type=4).order_by('time')
    context={
        'user':user,
        'all_notifications':all_notifications,
        'follow_req_notifications':follow_req_notifications,
        'feed_list':feed_list,
        'notifications':notifications,
    }
    return render(request,'app/home.html',context)

@login_required(login_url='login')
def home_search(request):
    if request.method == 'POST':
        username=request.POST.get('search')
        try:
            user=User.objects.get(username=username).username
            return redirect(f'/user/{user}')
        except:
            messages.info(request,f'There is no user with username: {username}')
            return redirect('home')
    else:
        return redirect('home')

@login_required(login_url='login')
def notifications(request):
    user=request.user
    notifications=Notification.objects.filter(user=user).order_by('-time')
    context={
        'user':user,
        'notifications':notifications,
    }
    return render(request,'app/notifications.html',context)

def user(request,username):
    user=User.objects.get(username=username)
    allowed_users=user.profile.followers()
    requested=False
    try:
        if Notification.objects.get(user=user,notifier=request.user,notification_type=4) is not None:
            requested=True
    except:
        requested=False
    context={
        'user':user,
        'allowed_users':allowed_users,
        'all_posts':user.post_set.all().order_by('-time'),
        'requested':requested
    }
    if request.user in allowed_users:
        return render(request,'app/userprofileunlocked.html',context)
    else:
        return render(request,'app/userprofilelocked.html',context)

def userpost(request,username,id):
    poster=User.objects.get(username=username)
    post=Post.objects.get(id=id)
    user=request.user
    no_likes=Like.objects.filter(post=post).count()
    no_comments=Comment.objects.filter(post=post).count()
    liked=False
    comments=None
    if Comment.objects.filter(post=post) is not None:
        comments=post.comment_set.all().order_by('-time')
    try:
        like = Like.objects.get(user=user,post=post)
        liked=True
    except:
        liked=False
    context={
        'post':post,
        'poster':poster,
        'user':user,
        'comments':comments,
        'liked':liked,
        'no_likes':no_likes,
        'no_comments':no_comments,
    }
    return render(request,'app/openpost.html',context)


def add_comment(request,username,id):
    if request.method == 'POST':
        poster=User.objects.get(username=username)
        post=Post.objects.get(id=id)
        user=request.user
        content = request.POST['comment']
        user = request.user
        commenter_profile_url = user.profile.profile_pic.url
        commenter = user.username
        if len(content)!=0:
            comment=Comment(user=user,post=post,content=content)
            comment.save()
            date = comment.display_date
            time = comment.display_time
        context={
            'username':username,
            'id':id,
            'comment':content,
            'commenter':request.user,
            'time':comment.time
        }
        return JsonResponse({'commenter':commenter,'comment':content,'commenter_pic':commenter_profile_url,'date':date,'time':time},status=200)
    else:
        print('not post')
        return JsonResponse({'error':'only post method'})

def like_unlike(request,username,id):
    poster=User.objects.get(username=username)
    post=Post.objects.get(id=id)
    user=request.user
    try:
        Like.objects.get(post=post,user=user).delete()
    except:
        like=Like(post=post,user=user)
        like.save()
    return redirect(f'/user/{username}/{id}')

def like_unlike_from_home(request,username,id):
    post=Post.objects.get(id=id)
    user=request.user
    try:
        Like.objects.get(post=post,user=user).delete()
    except:
        like=Like(post=post,user=user)
        like.save()
    return redirect('home')

def likeunlike(request,username,id):
    message = 'done'
    if request.method == 'GET':
        post = Post.objects.get(id=id)
        likes = post.no_likes
        user = request.user
        try:
            Like.objects.get(post=post,user=user).delete()
            likes -= 1
        except:
            like=Like(post=post,user=user)
            like.save()
            likes += 1
        return JsonResponse({'success':'done','likes':likes},status=200)
    else:
        return JsonResponse({'error':'only post method'})


def signup(request):
    form = SignUpForm()
    if request.method=="POST":
        form = SignUpForm(request.POST)
        profile_form = ProfileForm(request.POST or None,request.FILES or None)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request,'Account was created for '+username)
            login(request,user)
        return redirect('home')

    return render(request,'registration/signup.html',{'form':form})


def loginpage(request):
    if request.user.is_authenticated:
        return HttpResponse('You are already logged in')
    else:
        if request.method == 'POST':
            username= request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request,username=username,password=password)
            if user is not None:
                login(request,user)
                return redirect('home')
            else:
                messages.info(request,'Username or Password is incorrect')
        return render(request,'registration/login.html')

def logoutpage(request):
    if request.user.is_authenticated:
        logout(request)
        return redirect('login')
    else:
        return HttpResponse('You are not logged in')

@login_required(login_url='login')
def profile(request):
    user=request.user
    if request.method=='POST':
        form = ProfileForm(request.POST or None,request.FILES or None,instance=user.profile)
        if form.is_valid():
            profile=form.save(commit=False)
            user.profile=profile
            user.profile.save()
            return redirect('home')
    form = ProfileForm(instance=user.profile)
    context={
        'form':form
    }
    return render(request,'app/profile.html',context)

@login_required(login_url='login')
def post(request):
    form = PostForm()
    context={
        'form':form,
    }
    if request.method=='POST':
        form=PostForm(request.POST or None,request.FILES or None)
        try:
            post=form.save(commit=False)
            post.user=request.user
            post.save()
            messages.success(request,'Posted!')
            return redirect('home')
        except:
            messages.info(request,'Select a valid file')
            return render(request,'app/post.html',context)
    return render(request,'app/post.html',context)

@login_required(login_url='login')
def edit(request,id):
    user=request.user
    post=Post.objects.get(id=id)
    if request.method=='POST':
        form = PostForm(request.POST or None,request.FILES or None,instance=post)
        if form.is_valid():
            post=form.save()
            return redirect('home')
    form=PostForm(instance=post)
    context={
        'form':form,
    }
    return render(request,'app/post.html',context)

@login_required(login_url='login')
def following(request):
    user = request.user
    try:
        following_list=user.profile.following()
    except:
        following_list=None
    context={
        'user':user,
        'following_list':following_list,
    }
    return render(request,'app/following.html',context)

@login_required(login_url='login')
def followers(request):
    user = request.user
    try:
        followers_list=user.profile.followers()
    except:
        followers_list=None
    context={
        'user':user,
        'followers_list':followers_list,
    }
    return render(request,'app/followers.html',context)

@login_required(login_url='login')
def delete(request):
    request.user.profile.profile_pic.delete()
    return redirect('profile')



@login_required(login_url='login')
def follow_req(request,id):
    sender=request.user
    receiver=User.objects.get(id=id)
    notif=Notification(user=receiver,notifier=sender,notification_type=4)
    notif.save()
    path=request.GET.get('path')
    if path=='/':
        return redirect('home')
    else:
        return redirect(f'{path}')
        
@login_required(login_url='login')
def cancel_req(request,id):
    sender=request.user
    receiver=User.objects.get(id=id)
    Notification.objects.filter(user=receiver,notifier=sender,notification_type=4).delete()
    path=request.GET.get('path')
    if path=='/':
        return redirect('home')
    else:
        return redirect(f'{path}')

@login_required(login_url='login')
def req_accept(request,id):
    receiver=request.user
    sender=User.objects.get(id=id)
    receiver.friends.followers.add(sender)
    posts=Post.objects.filter(user=receiver)
    for p in posts:
        FeedPost.objects.get(post=p).users.add(sender)
    Notification.objects.filter(user=receiver,notifier=sender,notification_type=4).delete()
    notif=Notification(user=receiver,notifier=sender,notification_type=3)
    notif.save()
    notif2=Notification(user=sender,notifier=receiver,notification_type=5)
    notif2.save()
    path=request.GET.get('path')
    if path=='/':
        return redirect('home')
    else:
        return redirect(f'{path}')
@login_required(login_url='login')
def req_delete(request,id):
    receiver=request.user
    sender=User.objects.get(id=id)
    Notification.objects.filter(user=receiver,notifier=sender,notification_type=4).delete()
    path=request.GET.get('path')
    if path=='/':
        return redirect('home')
    else:
        return redirect(f'{path}')  

@login_required(login_url='login')
def follow(request,id):
    user=User.objects.get(id=id)
    follower=request.user
    user.friends.followers.add(follower)
    user.friends.save()
    notif=Notification(user=user,notifier=follower,notification_type=3)
    notif.save()
    posts=Post.objects.filter(user=user)
    for p in posts:
        FeedPost.objects.get(post=p).users.add(request.user)
    path=request.GET.get('path')
    if path=='/':
        return redirect('home')
    else:
        return redirect(f"{path}")

@login_required(login_url='login')
def unfollow(request,id):
    user=User.objects.get(id=id)
    unfollower=request.user
    user.friends.followers.remove(unfollower)
    user.friends.save()
    Notification.objects.filter(user=user,notifier=unfollower,notification_type=3).delete()
    posts=Post.objects.filter(user=user)
    for p in posts:
        FeedPost.objects.get(post=p).users.remove(request.user)
    path=request.GET.get('path')
    if path=='/':
        return redirect('home')
    else:
        return redirect(f"{path}")

