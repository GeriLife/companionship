from django import forms

from .models import Activity

class ActivityModelForm(forms.ModelForm):
    class Meta:
        model = Activity
        fields = ['person', 'activity_type', 'activity_date', 'note',]
