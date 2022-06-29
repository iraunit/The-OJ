from urllib import response
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Users
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from django.http.response import JsonResponse
from .serializers import UsersSerializers

# Create your views here.
@csrf_exempt
@login_required(login_url='/login')
def home(request,idd=0):
     user_email="Anonymous"
     if request.user:
          id=request.user.id
          user = User.objects.get(id=id)
          user_email = user.first_name + " "+user.last_name
          if user_email==" ":
               user_email=request.user

     #databse code
     
     if request.method=='GET':
          users=Users.objects.all()
          users_serializer=UsersSerializers(users,many=True)
          response= JsonResponse(users_serializer.data,safe=False)
          return render(request,'home.html',{
          "user_email":user_email,
          "response":response  
           })
     elif request.method=='POST':
          user_data=JSONParser().parse(request)
          users_serializer=UsersSerializers(data=user_data)
          if users_serializer.is_valid():
               users_serializer.save()
               return JsonResponse("done",safe=False)
          else:
                return JsonResponse("failed",safe=False)


     return render(request,'home.html',{
          "user_email":user_email,
     })

