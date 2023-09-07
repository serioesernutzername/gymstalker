from django import forms
from .models import data_entry


class DataForm(forms.ModelForm):
    class Meta:
        model = data_entry
        fields = '__all__'
