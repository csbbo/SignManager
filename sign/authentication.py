import functools
from django.shortcuts import render,redirect,reverse



def login_require(func):
    @functools.wraps(func)
    def wrapper(self,request,*args,**kw):
        print(request.session.get('name'))
        if not request.session.get('name'):
            return redirect(reverse('login'))
        return func(self,request,*args,**kw)
    return wrapper

