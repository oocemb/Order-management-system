from django import forms
from .models import Detail, Calc


class DetailForm(forms.ModelForm):
    """Форма для работы с деталями."""
    class Meta:
        model = Detail
        exclude = [""]


class CalcForm(forms.ModelForm):
    """Форма для работы с расчётами."""
    class Meta:
        model = Calc
        fields = ["title","tags"]
        widgets = {
            'title': forms.TextInput(attrs={'class':'form-control'}),
            'tags': forms.Select(attrs={'class':'form-control'}),
        }