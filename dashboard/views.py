from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

# Create your views here.

@login_required(login_url='/login')
def home(request):
     id=request.user.id
     user = User.objects.get(id=id)
     user_email = user.first_name + " "+user.last_name
     if user_email==" ":
          user_email=request.user
     return render(request,'home.html',{
          "user_email":user_email  
     })