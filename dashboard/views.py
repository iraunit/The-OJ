from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
import json,_json
from rest_framework.parsers import JSONParser
from django.http.response import JsonResponse
from .models import Problem
from .serializers import UsersSerializers
import pymongo
from decouple import config

connect_string="mongodb+srv://"+config('MONGO_ID')+":"+config('MONGO_PASS')+"@database-the-oj.ocnht.mongodb.net/?retryWrites=true&w=majority"
my_client = pymongo.MongoClient(connect_string)
problem_database=my_client["problem_list"]
new_problem=problem_database['problem']

# Create your views here.
@csrf_exempt
@login_required(login_url='/login')
def home(request):
     user_email="Anonymous"
     if request.user:
          id=request.user.id
          user = User.objects.get(id=id)
          user_email = user.first_name + " "+user.last_name
          if user_email==" ":
               user_email=request.user

     #databse code
     
     if request.method=='GET':
          users=Problem.objects();
          return render(request,'home.html',{
          "user_email":user_email,
          "response":users  
           })
     return render(request,'home.html',{
          "user_email":user_email,
     })



