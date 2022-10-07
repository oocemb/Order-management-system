from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse

from .forms import *


class ObjectDetailMixin:
    """Миксин информации об обьекте
    """
    model = None
    template = None

    def get(self, request, slug):
        obj = get_object_or_404(self.model, slug__iexact = slug)
        return render(request, self.template, {self.model.__name__.lower():obj
        , 'admin_obj':obj, 'detail':True})


class ObjectCreateMixin:
    """Миксин создания обьекта
    """
    form_model = None
    template = None

    def get(self, request):
        form = self.form_model()
        return render(request, self.template, {'form':form,'detail':form})

    def post(self,request):
        bound_form = self.form_model(request.POST)
        if bound_form.is_valid():
            new_obj = bound_form.save()
            return redirect(new_obj)
        return render(request, self.template, {'form':bound_form})


class ObjectUpdateMixin:
    """Миксин обновления обьекта
    """
    model = None
    model_form = None
    template = None

    def get(self, request, slug):
        obj = self.model.objects.get(slug__iexact=slug)
        bound_form = self.model_form(instance=obj)
        return render(request, self.template, {'form':bound_form, self.model.__name__.lower(): obj})

    def post(self, request, slug):
        obj = self.model.objects.get(slug__iexact=slug)
        bound_form = self.model_form(request.POST, instance=obj)
        if bound_form.is_valid():
            new_obj = bound_form.save()
            return redirect(new_obj)
        return render(request, self.template, {'form': bound_form, self.model.__name__.lower(): obj})


class ObjectDeleteMixin:
    """Миксин удаления обьекта
    """
    model = None
    template = None
    redirect_url = None

    def get(self, request, slug):
        obj = self.model.objects.get(slug__iexact=slug)
        return render(request, self.template, {self.model.__name__.lower():obj})
    
    def post(self, request, slug):
        obj = self.model.objects.get(slug__iexact=slug)
        obj.delete()
        return redirect(reverse(self.redirect_url))