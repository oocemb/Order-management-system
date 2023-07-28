from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.http.request import HttpRequest
from django.db.models import SlugField


class ObjectDetailMixin:
    model = None
    template = None

    def get(self, request: HttpRequest, slug: SlugField):
        obj = get_object_or_404(self.model, slug__iexact=slug)
        return render(
            request,
            self.template,
            {self.model.__name__.lower(): obj, 'admin_obj': obj, 'detail': True}
        )


class ObjectCreateMixin:
    model_form = None
    template = None

    def get(self, request: HttpRequest):
        form = self.model_form()
        return render(request, self.template, {'form': form, 'detail': True})

    def post(self, request: HttpRequest):
        bound_form = self.model_form(request.POST)
        if bound_form.is_valid():
            new_obj = bound_form.save()
            return redirect(new_obj)
        return render(request, self.template, {'form': bound_form})


class ObjectUpdateMixin:
    model = None
    model_form = None
    template = None

    def get(self, request: HttpRequest, slug: SlugField):
        obj = self.model.objects.get(slug__iexact=slug)
        bound_form = self.model_form(instance=obj)
        return render(request, self.template, {'form': bound_form, self.model.__name__.lower(): obj})

    def post(self, request: HttpRequest, slug: SlugField):
        obj = self.model.objects.get(slug__iexact=slug)
        bound_form = self.model_form(request.POST, instance=obj)
        if bound_form.is_valid():
            new_obj = bound_form.save()
            return redirect(new_obj)
        return render(request, self.template, {'form': bound_form, self.model.__name__.lower(): obj})


class ObjectDeleteMixin:
    model = None
    template = None
    redirect_url = None

    def get(self, request: HttpRequest, slug: SlugField):
        obj = self.model.objects.get(slug__iexact=slug)
        return render(request, self.template, {self.model.__name__.lower(): obj})
    
    def post(self, request: HttpRequest, slug: SlugField):
        obj = self.model.objects.get(slug__iexact=slug)
        obj.delete()
        return redirect(reverse(self.redirect_url))
