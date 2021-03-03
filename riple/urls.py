from django.contrib import admin
from django.urls import path
from riple import views

urlpatterns = [
    path('',views.home,name='home'),
    path('home_search',views.home_search,name='home_search'),
    path('register/',views.signup,name='register'),
    path('login/',views.loginpage,name='login'),
    path('logout/',views.logoutpage,name='logout'),
    path('profile/',views.profile,name='profile'),
    path('profile/delete/',views.delete,name='delete'),
    path('notifications/',views.notifications,name='notifications'),
    path('post/',views.post,name='post'),
    path('edit/<int:id>',views.edit,name='edit'),
    path('following',views.following,name='following'),
    path('followers',views.followers,name='followers'),
    path('follow/<int:id>',views.follow,name='follow'),
    path('unfollow/<int:id>',views.unfollow,name='unfollow'),
    path('follow_req/<int:id>',views.follow_req,name='follow_req'),
    path('cancel_req/<int:id>',views.cancel_req,name='cancel_req'),
    path('req_accept/<int:id>',views.req_accept,name='req_accept'),
    path('req_delete/<int:id>',views.req_delete,name='req_delete'),
    path('test',views.test,name='test'),
    path('user/<slug:username>',views.user,name='user'),
    path('user/<slug:username>/<int:id>',views.userpost,name='userpost'),
    path('add_comment/<slug:username>/<int:id>',views.add_comment,name='add_comment'),
    path('like_unlike/<slug:username>/<int:id>',views.like_unlike,name='like_unlike'),
    path('like_unlike_from_home/<slug:username>/<int:id>',views.like_unlike_from_home,name='like_unlike_from_home'),
    path('likeunlike/<slug:username>/<int:id>',views.likeunlike,name='likeunlike'),
    path('css',views.css,name="css")

    #path('login',views.login,name='login'),
]