from django import forms
from .models import *
from django.core.exceptions import ValidationError



class DetailForm(forms.ModelForm):

    class Meta:
        model = Detail
        exclude = [""]


class CalcForm(forms.ModelForm):

    class Meta:
        model = Calc
        fields = ["title","tags"]

        widgets = {
            'title': forms.TextInput(attrs={'class':'form-control'}),
            'tags': forms.Select(attrs={'class':'form-control'}),
        }