from django import forms

from .models import Detail, Calc, Comment


class DetailForm(forms.ModelForm):
    """Форма для работы с деталями."""
    class Meta:
        model = Detail
        exclude = [""]


class CommentForm(forms.ModelForm):
    """Форма для работы с коментариями."""
    class Meta:
        model = Comment
        exclude = ["calc"]
        widgets = {
            'name': forms.TextInput(attrs={'class':'form-control'}),
            'text': forms.Textarea(attrs={'class':'form-control'}),
        }


class CalcForm(forms.ModelForm):
    """Форма для работы с расчётами."""
    class Meta:
        model = Calc
        fields = ["title","tags"]
        widgets = {
            'title': forms.TextInput(attrs={'class':'form-control'}),
            'tags': forms.Select(attrs={'class':'form-control'}),
        }