from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from .models import Problem,Users,SubmittedProblem
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
     user_name="Anonymous"
     problem_name=""
     if request.method=='POST':
          id=request.user.id
          current_user = User.objects.get(id=id)
          user=Users.objects(email_id=current_user.email).get()
          current_problem=Problem.objects(problem_id=problem_id).get()
          code=request.POST['code_by_user']
          user_name=current_user.first_name + " "+current_user.last_name
          if user_name==" ":
               user_name=request.user.username
          language="C++"
          user.update(push__solved_problem=problem_id)
          problem_name=current_problem.problem_name
          test_cases=list(current_problem.test_case)
          verdict= handle_submission(code,user.email_id,test_cases)
          current_submission_by_user=SubmittedProblem(problem_id=problem_id,verdict=verdict,code=code,user_name=user_name,language=language)
          current_problem.update(push__solved_by=current_submission_by_user)
     # current_problem=Problem.objects.fields(problem_id=problem_id,slice__solved_by=[0,10]).all()
     return showLeaderBoard(request,problem_id,problem_name)


def showLeaderBoard(request,problem_id,problem_name):
     current_problem=(new_problem.find( { 'problem_id':problem_id } ))
     array_curr=list(current_problem)
     all_submission=array_curr[0]["solved_by"]
     submissions=[]
     for i in reversed(all_submission):
          submissions.append(i)
     # return HttpResponse(template/vertdict.html)
     print(len(submissions))
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
          "problem_name" : problem_name
     })


def AllLeaderBoard(request):
     user_name="Anonymous"
     if request.user:
          id=request.user.id
          user = User.objects.get(id=id)
          user_name = user.first_name + " "+user.last_name
          if user_name==" ":
               user_name=request.user
     all_users=Users.objects().all().order_by('-total_score')
     return render(request,'leaderboard.html',{
          "user_email":user_name,
          "leaders":all_users
     })


def handle_submission(submission,user_name, testcases):
    code_file_name='user_codes/'+user_name.split('@')[0]+'.cpp'
    exec_file_name='user_codes/'+user_name.split('@')[0]+'.exe'
    with open(code_file_name, 'w') as destination:
        destination.write(submission)

    subprocess.run(["g++", code_file_name, "-o", exec_file_name])
#     subprocess.run(["g++", code_file_name, "-o", "output.exe"])
#     subprocess.run(["g++", "input.cpp", "-o", "output.exe"])

    for testcase in testcases:

        input = testcase.input
        input = bytes(input, 'utf-8')

        output = subprocess.run([exec_file_name], capture_output=True, input = input, timeout=10)
        output = output.stdout.decode("utf-8")

        if output != testcase.output:
            return "Wrong Answer"

    return "Accepted"