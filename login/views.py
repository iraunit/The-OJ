from django.shortcuts import render,redirect
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
# Create your views here.
from .form import Register

def login_page(request):
    if request.user.is_authenticated:
        return redirect(home)
    if request.method=='POST':
        username= request.POST.get('username')
        password= request.POST.get('password')
        user=authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            return redirect(home)
        else:
            messages.info(request,'Username Or Password is incorrrect')
            return render(request, "login.html")
    return render(request, "login.html")


def register(request):
    if request.user.is_authenticated:
        return redirect(home)
    form=Register()
    if request.method=='POST':
        form=UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,'Account was created for '+form.cleaned_data.get('username'))
            return redirect('/login')
    return render(request, "register.html",{
        'form':form
    })

def logoutUser(request):
    logout(request)
    storage = messages.get_messages(request)
    storage.used = True
    messages.success(request,'Successfully Signed Out')
    return redirect(login_page)

def home(request):
    return redirect('/home')



