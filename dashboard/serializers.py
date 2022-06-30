from rest_framework_mongoengine.serializers import DocumentSerializer
from .models import Problem


class UsersSerializers(DocumentSerializer):
    class Meta:
        model=Problem
        fields=("problem_name","description","difficulty","tags","score","solved_by")
