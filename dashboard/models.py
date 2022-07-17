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
    code=StringField()
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

class Discuss(EmbeddedDocument):
    user_name=StringField()
    discuss=StringField()
    title=StringField()

    def json(self):
        user_dict = {
            "user_name":self.user_name,
            "title":self.title,
            "discuss":self.discuss
        }
        return json.dumps(user_dict)



class Problem(Document):
    problem_id = StringField(unique=True,Required=True)
    problem_name=StringField(Required=True)
    description=StringField(Required=True)
    difficulty=StringField()
    tags=StringField()
    score=FloatField()
    solved_by=ListField(EmbeddedDocumentField(SubmittedProblem))
    # test_case=ListField(EmbeddedDocumentField(TestCase))
    discussion=ListField(EmbeddedDocumentField(Discuss))

    def json(self):
        problem_dict = {
            "problem_id":self.problem_id,
            "problem_name":self.problem_name,
            "description":self.description,
            "difficulty":self.difficulty,
            "tags":self.tags,
            "score":self.score,
            "solved_by":self.solved_by,
            "discussion":self.discussion,
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
    problem_id = "trailing_zeroes",
    problem_name="Trailing Zeros",
    description="""
Your task is to calculate the number of trailing zeros in the factorial n!.

For example, 20!=2432902008176640000 and it has 4 trailing zeros.

Input

The only input line has an integer n.

Output

Print the number of trailing zeros in n!.

Constraints
1≤n≤109
Example

Input:
20

Output:
4
    """,
    difficulty="Medium",
    tags="Math, Introductory Problems",
    score=40,
    solved_by=[],
    discussion=[]
)