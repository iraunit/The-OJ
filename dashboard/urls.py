from django.urls import path,include
from .import views
urlpatterns = [
    path('home', views.home),
    path('problem/<str:problem_id>',views.ViewProblem),
    path('problem/submit/<str:problem_id>',views.submitProblem),
    path('leaderboard',views.AllLeaderBoard),
    path('submissions/<str:problem_id>',views.showLeaderBoard),
    path('mysubmissions/<str:problem_id>',views.mySubmissions),
    path('discussion/<str:problem_id>',views.Discussion),
    path('post-discussion/<str:problem_id>',views.writeDiscuss),
]
