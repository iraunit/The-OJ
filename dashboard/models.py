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
    test_case=ListField(EmbeddedDocumentField(TestCase))
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
    problem_id = "weird_algorithm",
    problem_name="Weird Algorithm",
    description="""
    Consider an algorithm that takes as input a positive integer n. If n is even, the algorithm divides it by two, and if n is odd, the algorithm multiplies it by three and adds one. The algorithm repeats this, until n is one. For example, the sequence for n=3 is as follows:
               
                        3→10→5→16→8→4→2→1

    Your task is to simulate the execution of the algorithm for a given value of n.
    
    Input

    The only input line contains an integer n.

    Output

    Print a line that contains all values of n during the algorithm.

    Constraints
    1≤n≤10^6
    Example

    Input:
    3

    Output:
    3 10 5 16 8 4 2 1   
    """,
    difficulty="Medium",
    tags="Math, Introductory Problems",
    score=50,
    test_case=[TestCase(input="7",output="7 22 11 34 17 52 26 13 40 20 10 5 16 8 4 2 1"),TestCase(input="15",output="5040"),TestCase(input="159487",output="159487 478462 239231 717694 358847 1076542 538271 1614814 807407 2422222 1211111 3633334 1816667 5450002 2725001 8175004 4087502 2043751 6131254 3065627 9196882 4598441 13795324 6897662 3448831 10346494 5173247 15519742 7759871 23279614 11639807 34919422 17459711 52379134 26189567 78568702 39284351 117853054 58926527 176779582 88389791 265169374 132584687 397754062 198877031 596631094 298315547 894946642 447473321 1342419964 671209982 335604991 1006814974 503407487 1510222462 755111231 2265333694 1132666847 3398000542 1699000271 5097000814 2548500407 7645501222 3822750611 11468251834 5734125917 17202377752 8601188876 4300594438 2150297219 6450891658 3225445829 9676337488 4838168744 2419084372 1209542186 604771093 1814313280 907156640 453578320 226789160 113394580 56697290 28348645 85045936 42522968 21261484 10630742 5315371 15946114 7973057 23919172 11959586 5979793 17939380 8969690 4484845 13454536 6727268 3363634 1681817 5045452 2522726 1261363 3784090 1892045 5676136 2838068 1419034 709517 2128552 1064276 532138 266069 798208 399104 199552 99776 49888 24944 12472 6236 3118 1559 4678 2339 7018 3509 10528 5264 2632 1316 658 329 988 494 247 742 371 1114 557 1672 836 418 209 628 314 157 472 236 118 59 178 89 268 134 67 202 101 304 152 76 38 19 58 29 88 44 22 11 34 17 52 26 13 40 20 10 5 16 8 4 2 1")]
)