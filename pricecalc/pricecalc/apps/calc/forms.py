from django import forms

from .models import Detail, Calc, Comment, FurnitureInCalc


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


class FurnitureInCalcForm(forms.ModelForm):
    """Форма для добавления фурнитуры не из БД."""
    class Meta:
        model = FurnitureInCalc
        exclude = ["calc", "furniture", "total_price"]
        widgets = {
            'title': forms.TextInput(attrs={'class':'form-control'}),
            'article': forms.TextInput(attrs={'class':'form-control'}),
            'price': forms.TextInput(attrs={'class':'form-control'}),
            'price_retail': forms.TextInput(attrs={'class':'form-control'}),
            'availability': forms.TextInput(attrs={'class':'form-control'}),
            'nmb': forms.TextInput(attrs={'class':'form-control'}),
        }