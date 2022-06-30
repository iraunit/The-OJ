from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
import json,_json
from rest_framework.parsers import JSONParser
from django.http.response import JsonResponse
from .models import Problem
from .serializers import UsersSerializers


config={
    "apiKey": "AIzaSyDSWmcUHY2esXYHa9k8ktMAfXQv0U5cICg",
    "authDomain": "the-oj-c4da7.firebaseapp.com",
    "projectId": "the-oj-c4da7",
    "storageBucket": "the-oj-c4da7.appspot.com",
    "messagingSenderId": "517725104591",
    "appId": "1:517725104591:web:ec30def359416eccf7caba",
    "measurementId": "G-CFW8PR20NE"
  }



# Create your views here.
@csrf_exempt
# @login_required(login_url='/login')
def home(request,idd=0):
     user_email="Anonymous"
     # if request.user:
     #      id=request.user.id
     #      user = User.objects.get(id=id)
     #      user_email = user.first_name + " "+user.last_name
     #      if user_email==" ":
     #           user_email=request.user

     #databse code
     
     if request.method=='GET':
          users=Problem.objects
          # json_data=users.to_json()
          # users_serializer=UsersSerializers(users)
          # response= JsonResponse(users_serializer.data,safe=False)
          # return users.to_json()
          return render(request,'home.html',{
          "user_email":user_email,
          "response":users  
           })
     # elif request.method=='POST':
          # user_data=JSONParser().parse(request)
          # users_serializer=UsersSerializers(data=user_data)
          # if users_serializer.is_valid():
          #      users_serializer.save()
          #      return JsonResponse("done",safe=False)
          # else:
          #       return JsonResponse("failed",safe=False)


     return render(request,'home.html',{
          "user_email":user_email,
     })



