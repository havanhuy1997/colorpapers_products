from dashboard.models import * 
from django import forms


class addTaskForm(forms.ModelForm):
    class Meta:
        model = processExecutions
        fields = ['process_title','node_id','node_type']