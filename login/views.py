from django.shortcuts import render,redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User
# Create your views here.
from .form import Register
from dashboard.models import Users

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
        try:
            if form.is_valid():
                obj=form.save(commit=False)
                email_id = request.POST['email']
                obj.email=email_id
                obj.save()
                user_name=request.POST['username']
                total_score=0.0
                solved_problem=[]
                Users(email_id=email_id,user_name=user_name,total_score=total_score,solved_problem=solved_problem).save()
                messages.success(request,'Account was created for '+form.cleaned_data.get('username'))
                return redirect('/login')
        except:
            return redirect(home)
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
    try:
        id=request.user.id
        user = User.objects.get(id=id)
        user_email = user.email
        print("email: "+user_email)
        Users.objects(email_id=user_email).get()
    except:
        try:
            user_name=request.user.first_name + " "+request.user.last_name
            total_score=0.0
            solved_problem=[]
            Users(email_id=request.user.email,user_name=user_name,total_score=total_score,solved_problem=solved_problem).save()
        except:
            return login_page(request)
    return redirect('/home')



