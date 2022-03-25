from django.urls import reverse
from django.shortcuts import render
from django.http import Http404, HttpResponseRedirect, JsonResponse
from django.contrib.auth.decorators import login_required

from .models import *
from .forms import *
from .tasks import update_data_furniture
from .services import crud_furniture_in_calc,\
                        crud_details_in_calc,\
                        current_furniture_in_calc_and_main_calc_info,\
                        current_details_in_calc_and_main_calc_info


def calc_list(request):
    """Показывает список текущих расчётов."""
    if request.user.is_authenticated:
        if request.user.is_staff:
            calc_list = Calc.objects.order_by('-create_at')[:15]
        else:
            calc_list = Calc.objects.filter(designer=request.user).order_by('-create_at')
    return render(request, 'calc/calc_list.html', locals())


def adding_calc(request):
    """Добавляет новый расчёт."""
    if request.POST:
        form = CalcForm(request.POST)
        if form.is_valid():
            obj = Calc.objects.create(designer=request.user, title=form.cleaned_data["title"],
                tags=form.cleaned_data["tags"])
            obj.save()
            return HttpResponseRedirect(reverse('calc_details_form', args = (obj.id,)))
        return render(request, 'calc/adding_calc.html', locals())  
    else:
        form = CalcForm()
        return render(request, 'calc/adding_calc.html', locals())


@login_required()
def calc_details_form(request, calc_id):
    """Форма для расчёта с взаимодействием через Ajax."""
    calc = Calc.objects.get(pk=calc_id)
    # form = DetailForm
    furniture_list = Furniture.objects.filter(category_id = 1)
    latest_comment = Comment.objects.filter(calc=calc_id).order_by('-id')[:10]
    return render(request, 'calc/calc_details_form.html', locals())


def adding_detail(request):
    """Контроллер изменение деталей из расчета"""
    calc_id = request.POST.get("calc_id")
    crud_details_in_calc(request)
    return JsonResponse(current_details_in_calc_and_main_calc_info(calc_id=calc_id))


def adding_furniture(request):
    """Контроллер изменение деталей из расчета"""
    calc_id = request.POST.get("calc_id")
    crud_furniture_in_calc(request)
    return JsonResponse(current_furniture_in_calc_and_main_calc_info(calc_id=calc_id))


def update_data(request):
    """Обновление базы данных фурнитуры"""
    update_data_furniture.delay()
    return HttpResponseRedirect(reverse('calc_list'))


def comment(request, calc_id):
    try:
        a = Calc.objects.get( id = calc_id )
    except:
        raise Http404("Not found")

    a.comment_set.create(author_name = request.POST['name'], comment_text = request.POST['text'])
    return HttpResponseRedirect(reverse('calc_details_form', args = (a.id,)))

