from django.shortcuts import render,redirect
from django.contrib.auth import authenticate
from django.http import HttpResponse

def unauthenticated_user(view_func):
    def wrapper_func(request,*args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home')
        else:
            return view_func(request,*args, **kwargs)
    return wrapper_func

def allowed_users(allowed_roles=[]):
    def decorator(view_func):
        def wrapper_func(request,*args,**kwargs):
            if request.user in allowed_roles:
                return view_func(request,*args, **kwargs)
            else:
                return HttpResponse("This account is private")
        return wrapper_func
    return decorator