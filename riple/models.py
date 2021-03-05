from django.db import models
import datetime
from django.contrib.auth.models import User
from django.db.models.signals import post_save,post_delete
# Create your models here.
    
class Friends(models.Model):
    followers = models.ManyToManyField(User,related_name='followers',blank=True)
    user = models.OneToOneField(User,on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username}'s friends list"

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_pic=models.ImageField(null=False,blank=True,default="default_user.png")
    age=models.IntegerField(null=True,blank=True,default=18)
    is_private=models.BooleanField(default=True,null=True,blank=True)
    def following(self):
        return Friends.objects.filter(followers=self.user)
    def followers(self):
        return self.user.friends.followers.all()
    @property
    def following_count(self):
        return self.following().count()
    @property
    def followers_count(self):
        return self.followers().count()

    def __str__(self):
        return self.user.username
    

def create_profile(sender,instance,created,**kwargs):
    if created:
        profile=Profile.objects.create(user=instance)

post_save.connect(create_profile,sender=User)

def create_friends(sender,instance,created,**kwargs):
    if created:
        friends=Friends.objects.create(user=instance)

post_save.connect(create_friends,sender=User)

class Post(models.Model):
    caption = models.CharField(max_length=500,null=True,blank=True)
    pic = models.ImageField(null=False,blank=False,upload_to="images/",default="default_user.png")
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    time = models.DateTimeField(null=True,blank=True,auto_now_add=True)
    @property
    def display_date(self):
        return self.time.strftime("%b %d")
    @property
    def display_time(self):
        return self.time.strftime("%I:%M %p")
    @property
    def no_likes(self):
        return Like.objects.filter(post=self).count()
    def no_comments(self):
        return Comment.objects.filter(post=self).count()
    @property
    def likes(self):
        #all_users_who_liked
        user_list=[]
        for l in Like.objects.filter(post=self):
            user_list.append(l.user)
        return user_list
    @property
    def comments(self):
        #all_users_who_commented
        user_list=[]
        for c in Comment.objects.filter(post=self):
            user_list.append(c.user)
        return user_list

class Notification(models.Model):
    NOTIFICATION_TYPES=((1,'Like'),(2,'Comment'),(3,'Follow'),(4,'Request'),(5,'Aceepted'))
    post = models.ForeignKey(Post,null=True,blank=True,on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name="noti_from_user")
    notifier = models.ForeignKey(User,on_delete=models.CASCADE,related_name="noti_to_user")
    pic = models.ImageField(null=True,blank=True)
    is_seen = models.BooleanField(default=False)
    time = models.DateTimeField(null=True,blank=True,auto_now_add=True)
    notification_type = models.IntegerField(choices=NOTIFICATION_TYPES)

    @property
    def notification_message(self):
        if self.notification_type==1:
            return "liked your photo"
        elif self.notification_type==2:
            return "commented on your photo"
        elif self.notification_type==3:
            return "followed you"
        elif self.notification_type==4:
            return "requested to follow you"
        else:
            return "accepted your request"
    
    @property
    def display_date(self):
        return self.time.strftime("%b %d")
    @property
    def display_time(self):
        return self.time.strftime("%I:%M %p")

class Like(models.Model):
    post=models.ForeignKey(Post,on_delete=models.CASCADE)
    user=models.ForeignKey(User,on_delete=models.CASCADE) #liker
    time=models.DateTimeField(null=True,blank=True,auto_now_add=True)
    def user_liked_post(sender,instance,*args, **kwargs):
        like=instance
        post=like.post
        liker=like.user
        user=post.user
        time=like.time
        pic=post.pic
        notify=Notification(post=post,user=user,notifier=liker,pic=pic,time=time,notification_type=1)
        notify.save() #this is not the save dictating the post_save signal

    def user_unliked_post(sender,instance,*args, **kwargs):
        unlike=instance
        post=unlike.post
        unliker=unlike.user
        user=post.user
        Notification.objects.filter(post=post,user=user,notifier=unliker,notification_type=1).delete()

post_save.connect(Like.user_liked_post,sender=Like)
post_delete.connect(Like.user_unliked_post,sender=Like)

class Comment(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE) #commenter
    post = models.ForeignKey(Post,on_delete=models.CASCADE)
    time = models.DateTimeField(auto_now_add=True)
    content = models.CharField(max_length=1000,blank=False,null=False)


    @property
    def display_date(self):
        return self.time.strftime("%b %d")
    @property
    def display_time(self):
        return self.time.strftime("%I:%M %p")
    

    def comment_added(sender,instance,created,*args, **kwargs):
        if created:
            comment=instance
            post=comment.post
            commenter=comment.user
            user=post.user
            time=comment.time
            pic=post.pic
            notify=Notification(post=post,user=user,notifier=commenter,pic=pic,time=time,notification_type=2)
            notify.save()

    def comment_deleted(sender,instance,*args, **kwargs):
        comment=instance
        post=comment.post
        commenter=comment.user
        user=post.user
        Notification.objects.filter(post=post,user=user,notifier=commenter,notification_type=2).delete()

post_save.connect(Comment.comment_added,sender=Comment)
post_delete.connect(Comment.comment_deleted,sender=Comment)

class FeedPost(models.Model):
    post=models.ForeignKey(Post,on_delete=models.CASCADE)
    user=models.ForeignKey(User,null=True,blank=True,related_name='post_followers',on_delete=models.CASCADE)
    users=models.ManyToManyField(User) #followers of the poster
    time=models.DateTimeField(null=False,blank=False)

    def is_user(self):
        is_user=False
        if self.user==user:
            is_user=True
        return is_user

def add_to_feed(sender,instance,created,*args, **kwargs):
    if created:
        users=Friends.objects.get(user=instance.user).followers.all()
        feed=FeedPost.objects.create(post=instance,time=instance.time)
        feed.save()
        for user in users:
            feed.users.add(user)
        feed.save()

post_save.connect(add_to_feed,sender=Post)
