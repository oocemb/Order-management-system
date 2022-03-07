from django import forms
from .models import *
from django.core.exceptions import ValidationError



class DetailForm(forms.ModelForm):

    class Meta:
        model = Detail
        exclude = [""]