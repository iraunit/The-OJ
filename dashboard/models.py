
from sqlite3 import connect
from django.forms import FloatField, IntegerField
from mongoengine import *
from mongoengine import Document
from mongoengine.document import Document
from mongoengine.fields import StringField, ListField
from decouple import config
connect_string="mongodb+srv://"+config('MONGO_ID')+":"+config('MONGO_PASS')+"@database-the-oj.ocnht.mongodb.net/?retryWrites=true&w=majority"
# my_client = pymongo.MongoClient(connect_string)
connect(db="problem_list", host=connect_string, username=config('MONGO_ID'), password=config('MONGO_PASS'))

# Create your models here.
# class Users(models.Model):
#     _id=models.CharField(max_length=250,default="")
#     email=models.EmailField(primary_key=True)
#     total_score=models.FloatField(default=0.0)
#     problems_solved=models.TextField(default="")


class Problem(Document):
    problem_id = StringField(unique=True,Required=True)
    problem_name=StringField(Required=True)
    description=StringField(Required=True)
    difficulty=StringField()
    tags=StringField()
    score=FloatField()
    solved_by=ListField()

    def json(self):
        problem_dict = {
            "problem_id":self.problem_id,
            "problem_name":self.problem_name,
            "description":self.description,
            "difficulty":self.difficulty,
            "tags":self.tags,
            "score":self.score,
            "solved_by":self.solved_by,
        }
    
    meta = {
        "indexes":["problem_id"],
        "ordering":["-date_created"]
    }


# prob= Problem(
#     problem_id="hello lol",
#     problem_name="koi naam nhi hai",
#     description="lol ho tum"
# ).save()