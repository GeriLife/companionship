from django import forms
from django.contrib.admin.widgets import AdminDateWidget

from .models import Activity

class ActivitModelForm(forms.ModelForm):
    class Meta:
        model = Activity
        fields = ['activity_type', 'activity_date',]
        widgets = {
            'activity_date': AdminDateWidget(),
        }
