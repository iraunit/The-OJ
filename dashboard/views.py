from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from .models import Problem,Users,SubmittedProblem
import pymongo
from mongoengine import *
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


@login_required(login_url='/login')
def ViewProblem(request,problem_id):
     user_email="Anonymous"
     if request.user:
          id=request.user.id
          user = User.objects.get(id=id)
          user_email = user.first_name + " "+user.last_name
          if user_email==" ":
               user_email=request.user
     problem_to_show=Problem.objects(problem_id=problem_id)
     return render(request,'problem.html',{
          "user_email":user_email,
          "response":problem_to_show
     })

@login_required(login_url='/login')
def submitProblem(request,problem_id):
     if request.method=='POST':
          id=request.user.id
          current_user = User.objects.get(id=id)
          user=Users.objects(email_id=current_user.email).get()
          current_problem=Problem.objects(problem_id=problem_id).get()
          verdict="Passed"
          code=request.POST['code_by_user']
          email_id=current_user.email
          language="C++"
          submission=SubmittedProblem(problem_id=problem_id,verdict=verdict,code=code,email_id=email_id,language=language)
          user.update(push__solved_problem=problem_id)
          current_problem.update(push__solved_by=submission)
     return render(request,'verdict.html')