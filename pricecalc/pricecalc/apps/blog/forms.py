from django import forms
from django.core.exceptions import ValidationError

from .models import Tag, Post


def clean_slug_method(self):
    """Форма проверки чтоб слаг не был равен невозможному 
    в нашем контексте значению."""
    new_slug = self.cleaned_data['slug'].lower()
    if new_slug == 'create':
        raise ValidationError('Slug may not be "create"')
    if Tag.objects.filter(slug__iexact=new_slug).count():
        raise ValidationError('Slug not uniq go re')
    return new_slug


class TagForm(forms.ModelForm):
    """Форма для тэга поста."""
    class Meta:
        model = Tag
        fields = ['title', 'slug']
        widgets = {
            'title': forms.TextInput(attrs={'class':'form-control'}),
            'slug': forms.TextInput(attrs={'class':'form-control'}),
        }

    def clean_slug(self):
        return clean_slug_method(self)


class PostForm(forms.ModelForm):
    """Форма для поста."""
    class Meta:
        model = Post
        fields = ['title','body','tags']
        widgets = {
            'title': forms.TextInput(attrs={'class':'form-control'}),
            'body': forms.Textarea(attrs={'class':'form-control'}),
            'tags': forms.SelectMultiple(attrs={'class':'form-control'}),
        }

    def clean_slug(self):
        return clean_slug_method(self)