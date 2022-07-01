import datetime
import json
from django.forms import DateTimeField, EmailField, FloatField
from mongoengine import *
from mongoengine import Document,connect
from mongoengine.document import Document
from mongoengine.fields import StringField, ListField,EmbeddedDocument,EmbeddedDocumentField
from decouple import config
connect_string="mongodb+srv://"+config('MONGO_ID')+":"+config('MONGO_PASS')+"@database-the-oj.ocnht.mongodb.net/?retryWrites=true&w=majority"
# my_client = pymongo.MongoClient(connect_string)
connect(db="my_database", host=connect_string, username=config('MONGO_ID'), password=config('MONGO_PASS'))

class SubmittedProblem(EmbeddedDocument):
    problem_id=StringField(Required=True)
    verdict=StringField(Required=True)
    submitted_date=DateTimeField(default=datetime.datetime.now)
    code=StringField()
    email_id=EmailField(required=True)
    language=StringField()

    def json(self):
        submitted_problem_dict = {
            "problem_id":self.problem_id,
            "verdict":self.verdict,
            "submitted_date":self.submitted_date,
            "code":self.code,
            "email_id":self.email_id,
            "language":self.language,
        }
        return json.dumps(submitted_problem_dict)
    
    meta = {
        "indexes":["problem_id"],
        "indexes":["email_id"],
        "ordering":["-date_created"]
    }



class Problem(Document):
    problem_id = StringField(unique=True,Required=True)
    problem_name=StringField(Required=True)
    description=StringField(Required=True)
    difficulty=StringField()
    tags=StringField()
    score=FloatField()
    solved_by=ListField(EmbeddedDocumentField(SubmittedProblem))
    example_testcase=ListField()
    test_case=ListField()

    def json(self):
        problem_dict = {
            "problem_id":self.problem_id,
            "problem_name":self.problem_name,
            "description":self.description,
            "difficulty":self.difficulty,
            "tags":self.tags,
            "score":self.score,
            "solved_by":self.solved_by,
            "example_testcase":self.example_testcase,
            "test_case":self.test_case,
        }
        return json.dumps(problem_dict)
    
    meta = {
        "indexes":["problem_id"],
        "ordering":["-date_created"]
    }


class Users(Document):
    email_id = StringField(unique=True,Required=True)
    user_name=StringField(Required=True)
    total_score=FloatField()
    solved_problem=ListField()

    def json(self):
        user_dict = {
            "email_id":self.email_id,
            "user_name":self.user_name,
            "total_score":self.total_score,
            "solved_problem":self.solved_problem,
        }
        return json.dumps(user_dict)
    
    meta = {
        "indexes":["total_score"],
        "ordering":["-total_score"]
    }

sub=SubmittedProblem(problem_id="problem submit ho gya",verdict="pass ho gya code",email_id="meraemail@gmail.com")

problem=Problem(
    problem_id = "ye mera id hai",
    problem_name="ye mera naam hai",
    description="ye mera des hai",
    difficulty="mai difficult hu",
    tags="mera tags ye hai",
    score=78.94,
    solved_by=[sub],
    example_testcase=["13","343"],
    test_case=["34","332","23423"]
)