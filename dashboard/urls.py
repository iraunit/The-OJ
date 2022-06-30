from django.urls import path,include
from .import views
urlpatterns = [
    path('home', views.home),
    path('problem/<str:problem_id>',views.ViewProblem)
]
