from django.db import models

# Create your models here.
class Users(models.Model):
    _id=models.CharField(max_length=250,default="")
    email=models.EmailField(primary_key=True)
    total_score=models.FloatField(default=0.0)
    problems_solved=models.TextField(default="")