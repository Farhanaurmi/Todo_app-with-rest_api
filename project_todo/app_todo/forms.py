from django.forms import ModelForm
from .models import TodoClass

class TodoForm(ModelForm):
    class Meta:
        model = TodoClass
        fields = ['title','memo','im']