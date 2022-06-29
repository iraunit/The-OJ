from django.db import models

# Create your models here.
class Users(models.Model):
    email=models.EmailField(primary_key=True)
    total_score=models.FloatField(default=0.0)
    problems_solved=models.TextField(default="")