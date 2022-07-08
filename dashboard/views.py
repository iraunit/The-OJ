from ftplib import all_errors
from django import template
register = template.Library()
from genericpath import exists
from os import remove
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from .models import Problem,Users,SubmittedProblem,Discuss
import pymongo
from mongoengine import *
from decouple import config
import subprocess

connect_string="mongodb+srv://"+config('MONGO_ID')+":"+config('MONGO_PASS')+"@database-the-oj.ocnht.mongodb.net/?retryWrites=true&w=majority"
my_client = pymongo.MongoClient(connect_string)
problem_database=my_client["my_database"]
new_problem=problem_database['problem']

# Create your views here.
@csrf_exempt
@login_required(login_url='/login')
def home(request):
     user_email="Anonymous"
     try:
          if request.user:
               id=request.user.id
               user = User.objects.get(id=id)
               user_email = user.first_name + " "+user.last_name
               if user_email==" ":
                    user_email=request.user
     except:
          print('no user Found')
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
          "response":problem_to_show,
          "problem_id":problem_id
     })

@login_required(login_url='/login')
def submitProblem(request,problem_id):
     user_name="Anonymous"
     current_problem=Problem.objects(problem_id=problem_id).get()
     problem_name=current_problem.problem_name
     if request.method=='POST':
          id=request.user.id
          current_user = User.objects.get(id=id)
          user=Users.objects(email_id=current_user.email).get()
          code=request.POST['code_by_user']
          user_name=current_user.first_name + " "+current_user.last_name
          if user_name==" ":
               user_name=request.user.username
          language="C++"
          submitted_problem_by_users=list(user.solved_problem)
          test_cases=list(current_problem.test_case)
          verdict= handle_submission(code,user.email_id,test_cases)
          user_email=user.email_id
          if verdict=="Accepted":
               if current_problem.problem_id not in submitted_problem_by_users:
                    user.update(push__solved_problem=problem_id)
                    user.update(set__total_score=current_problem.score+user.total_score)
          current_submission_by_user=SubmittedProblem(problem_id=problem_id,verdict=verdict,code=code,user_email=user_email,user_name=user_name,language=language)
          current_problem.update(push__solved_by=current_submission_by_user)
     # current_problem=Problem.objects.fields(problem_id=problem_id,slice__solved_by=[0,10]).all()
     return showLeaderBoard(request,problem_id)

@login_required(login_url='/login')
def showLeaderBoard(request,problem_id):
     current_problem=(new_problem.find( { 'problem_id':problem_id } ))
     problem_name=current_problem[0]["problem_name"]
     array_curr=list(current_problem)
     all_submission=array_curr[0]["solved_by"]
     submissions=[]
     for i in reversed(all_submission):
          submissions.append(i)
     # return HttpResponse(template/vertdict.html)
     user_name="Anonymous"
     if request.user:
          id=request.user.id
          user = User.objects.get(id=id)
          user_name = user.first_name + " "+user.last_name
          if user_name==" ":
               user_name=request.user
     return render(request,'verdict.html',{
          "user_email":user_name,
          "submissions":submissions,
          "problem_name" : problem_name,
          "problem_id":problem_id
     })

@login_required(login_url='/login')
def mySubmissions(request,problem_id):
     current_problem=(new_problem.find( { 'problem_id':problem_id } ))
     problem_name=current_problem[0]["problem_name"]
     array_curr=list(current_problem)
     all_submission=array_curr[0]["solved_by"]
     submissions=[]
     id=request.user.id
     current_user = User.objects.get(id=id)
     for i in reversed(all_submission):
          email=i['user_email']
          if email==current_user.email:
               submissions.append(i)
     # return HttpResponse(template/vertdict.html)
     user_name="Anonymous"
     if request.user:
          id=request.user.id
          user = User.objects.get(id=id)
          user_name = user.first_name + " "+user.last_name
          if user_name==" ":
               user_name=request.user
     return render(request,'verdict.html',{
          "user_email":user_name,
          "submissions":submissions,
          "problem_name" : problem_name,
          "problem_id":problem_id
     })



@login_required(login_url='/login')
def AllLeaderBoard(request):
     user_name="Anonymous"
     if request.user:
          id=request.user.id
          user = User.objects.get(id=id)
          user_name = user.first_name + " "+user.last_name
          if user_name==" ":
               user_name=request.user
     all_users=Users.objects().all().order_by('-total_score')
     rank=[]
     for i in range(len(all_users)):
          rank.append(i+1)
     myList=zip(all_users,rank)
     return render(request,'leaderboard.html',{
          "user_email":user_name,
          "leaders":myList
     })


def handle_submission(submission,user_name, testcases):
    code_file_name='user_codes/'+user_name.split('@')[0]+'.cpp'
    exec_file_name='user_codes/'+user_name.split('@')[0]+'.exe'
    with open(code_file_name, 'w') as destination:
        destination.write(submission)

    subprocess.run(["g++", code_file_name, "-o", exec_file_name])
    file_exists=exists(exec_file_name)
    if not file_exists:
         return "RunTime Error"

    for testcase in testcases:

        input = testcase.input
        input = bytes(input, 'utf-8')
        try:
               output = subprocess.run([exec_file_name], capture_output=True, input = input,timeout=20)
               output = output.stdout.decode("utf-8")
        except:
             remove(exec_file_name)
             return "TLE"
        if output.strip() != testcase.output.strip():
            print(output.strip())
            print(testcase.output.strip())
            remove(exec_file_name)
            return "Wrong Answer"
    remove(exec_file_name)
    return "Accepted"


@login_required(login_url='/login')
def writeDiscuss(request,problem_id):
     user_email="Anonymous"
     if request.user:
          id=request.user.id
          user = User.objects.get(id=id)
          user_email = user.first_name + " "+user.last_name
          if user_email==" ":
               user_email=request.user
     problem_to_show=Problem.objects(problem_id=problem_id)
     return render(request,'post-discuss.html',{
          "user_email":user_email,
          "response":problem_to_show,
          "problem_id":problem_id
     })

@login_required(login_url='/login')
def PostDiscuss(request,problem_id):
     user_name="Anonymous"
     current_problem=Problem.objects(problem_id=problem_id).get()
     if request.method=='POST':
          id=request.user.id
          current_user = User.objects.get(id=id)
          discuss_by_user=request.POST['discuss_by_user']
          title=request.POST['title']
          user_name=current_user.first_name + " "+current_user.last_name
          if user_name==" ":
               user_name=request.user.username
          discuss=Discuss(user_name=user_name,discuss=discuss_by_user,title=title)
          current_problem.update(push__discussion=discuss)
     # current_problem=Problem.objects.fields(problem_id=problem_id,slice__solved_by=[0,10]).all()
     return Discussion(request,problem_id)


@login_required(login_url='/login')
def Discussion(request,problem_id):
     current_problem=Problem.objects(problem_id=problem_id).get()
     problem_name=None
     user_name="Anonymous"
     if request.method=='POST':
          id=request.user.id
          current_user = User.objects.get(id=id)
          discuss_by_user=request.POST['discuss_by_user']
          title=request.POST['title']
          user_name=current_user.first_name + " "+current_user.last_name
          if user_name==" ":
               user_name=request.user.username
          discuss=Discuss(user_name=user_name,discuss=discuss_by_user,title=title)
          current_problem.update(push__discussion=discuss)
     if request.user:
          id=request.user.id
          user = User.objects.get(id=id)
          user_name = user.first_name + " "+user.last_name
          if user_name==" ":
               user_name=request.user
     current_problem=(new_problem.find( { 'problem_id':problem_id } ))
     problem_name=current_problem[0]["problem_name"]
     array_curr=list(current_problem)
     all_discussion=array_curr[0]["discussion"]
     return render(request,'discuss.html',{
          "user_email":user_name,
          "discussions":all_discussion,
          "problem_name" : problem_name,
          "problem_id":problem_id
     })


@register.simple_tag
def update_variable(value):
    return value+1