from django import forms

from .models import Activity

class ActivityModelForm(forms.ModelForm):
    class Meta:
        model = Activity
        fields = ['care_group', 'activity_type', 'activity_date',]
