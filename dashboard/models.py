import datetime
import json
from django.forms import DateTimeField, EmailField, FloatField
from mongoengine import *
from mongoengine import Document,connect
from mongoengine.document import Document
from pygments import lexers,styles
from mongoengine.fields import StringField, ListField,EmbeddedDocument,EmbeddedDocumentField
from decouple import config
connect_string="mongodb+srv://"+config('MONGO_ID')+":"+config('MONGO_PASS')+"@database-the-oj.ocnht.mongodb.net/?retryWrites=true&w=majority&connectTimeoutMS=60000"
# my_client = pymongo.MongoClient(connect_string)
connect(db="my_database", host=connect_string)


LEXERS = [item for item in lexers.get_all_lexers() if item[1]]
LANGUAGE_CHOICES = sorted([(item[1][0], item[0]) for item in LEXERS])
STYLE_CHOICES = sorted([(item, item) for item in styles.get_all_styles()])

class SubmittedProblem(EmbeddedDocument):
    problem_id=StringField(Required=True)
    verdict=StringField(Required=True)
    submitted_date=DateTimeField(default=datetime.datetime.now)
    code=StringField(unique=True)
    user_email=EmailField()
    user_name=StringField(required=True)
    language=StringField()

    def json(self):
        submitted_problem_dict = {
            "problem_id":self.problem_id,
            "verdict":self.verdict,
            "submitted_date":self.submitted_date,
            "code":self.code,
            "user_email":self.user_email,
            "user_name":self.email_id,
            "language":self.language,
        }
        return json.dumps(submitted_problem_dict)
    
    meta = {
        "indexes":["problem_id"],
        "indexes":["user_name"],
        "ordering":["date_created"]
    }

class TestCase(EmbeddedDocument):
    input=StringField()
    output=StringField()

    def json(self):
        test_case_dict = {
            "input":self.input,
            "output":self.output
        }
        return json.dumps(test_case_dict)




class Problem(Document):
    problem_id = StringField(unique=True,Required=True)
    problem_name=StringField(Required=True)
    description=StringField(Required=True)
    difficulty=StringField()
    tags=StringField()
    score=FloatField()
    solved_by=ListField(EmbeddedDocumentField(SubmittedProblem))
    test_case=ListField(EmbeddedDocumentField(TestCase))

    def json(self):
        problem_dict = {
            "problem_id":self.problem_id,
            "problem_name":self.problem_name,
            "description":self.description,
            "difficulty":self.difficulty,
            "tags":self.tags,
            "score":self.score,
            "solved_by":self.solved_by,
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

# sub=SubmittedProblem(problem_id="problem submit ho gya",verdict="pass ho gya code",user_name="Raunit Verma")

problem=Problem(
    problem_id = "find_factorial_of_a_number",
    problem_name="Crazy Factorial",
    description="Given an integer n find the factorial of the integer n.",
    difficulty="Easy",
    tags="Math",
    score=10,
    test_case=[TestCase(input="5",output="120"),TestCase(input="7",output="5040"),TestCase(input="10",output="3628800"),TestCase(input="4",output="24")]
)