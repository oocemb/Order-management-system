from django import forms

from calc.models import Calc, Comment, FurnitureInCalc


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        exclude = ["calc"]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'text': forms.Textarea(attrs={'class': 'form-control'}),
        }


class CalcForm(forms.ModelForm):
    class Meta:
        model = Calc
        fields = ["title", "tags"]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'tags': forms.Select(attrs={'class': 'form-control'}),
        }


class FurnitureInCalcForm(forms.ModelForm):
    """Форма для добавления фурнитуры не из БД"""
    class Meta:
        model = FurnitureInCalc
        exclude = ["calc", "furniture", "total_price"]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'article': forms.TextInput(attrs={'class': 'form-control'}),
            'price': forms.TextInput(attrs={'class': 'form-control'}),
            'price_retail': forms.TextInput(attrs={'class': 'form-control'}),
            'availability': forms.TextInput(attrs={'class': 'form-control'}),
            'nmb': forms.TextInput(attrs={'class': 'form-control'}),
        }
