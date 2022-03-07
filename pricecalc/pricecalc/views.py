from django.shortcuts import render, get_list_or_404, get_object_or_404, redirect
from django.http import HttpResponse, Http404, HttpResponseRedirect



def redirect_main(request):
    """ Перенаправляет на основную страницу
    """
    return redirect('calc_list', permanent=True)  # постоянный редиркект , бывает временный 




