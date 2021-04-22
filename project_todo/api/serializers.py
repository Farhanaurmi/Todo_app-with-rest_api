from rest_framework import serializers
from app_todo.models import TodoClass

class TodoClassSerializer(serializers.ModelSerializer):
    Ctime=serializers.ReadOnlyField()
    dtime=serializers.ReadOnlyField()

    class Meta:
        model=TodoClass
        fields=['id','title','memo','Ctime','dtime','im','user']

