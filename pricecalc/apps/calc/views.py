from django.urls import reverse
from django.shortcuts import render
from django.http import Http404, HttpResponseRedirect, JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_page

from .models import *
from .forms import *
from .tasks import update_data_furniture, update_ldstp_task
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


# @cache_page(60 * 15)
@login_required()
def calc_details_form(request, calc_id):
    """Форма для расчёта с взаимодействием через Ajax."""
    calc = Calc.objects.get(pk=calc_id)
    furniture = Furniture.objects.all()
    standart_furniture = furniture.filter(category_id = 1)
    kitchen_furniture = furniture.filter(category_id = 2)
    countertops_furniture = furniture.filter(category_id = 3)
    silk_and_drying_furniture = furniture.filter(category_id = 4)
    lift_and_box_furniture = furniture.filter(category_id = 5)
    mensolo_hangers_legs_furniture = furniture.filter(category_id = 6)
    wardrobe_furniture = furniture.filter(category_id = 7)
    handle_furniture = furniture.filter(category_id = 8)
    ldsp_list = Ldstp.objects.all()
    latest_comment = Comment.objects.filter(calc_id=calc_id).order_by('-id')
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


def update_ldsp(request):
    """Обновление базы данных ЛДСП"""
    update_ldstp_task.delay()
    return HttpResponseRedirect(reverse('calc_list'))


def leave_comment(request, calc_id):
    """Форма для добавления нового комментария."""
    if request.POST:
        form = CommentForm(request.POST)
        if form.is_valid():
            obj = Comment.objects.create(calc_id=calc_id,
                name=form.cleaned_data["name"],
                text=form.cleaned_data["text"])
            obj.save()
            return HttpResponseRedirect(reverse('calc_details_form', args = (calc_id,)))
        print('no valid')
        return render(request, 'calc/leave_comment.html', locals())
    else:
        form = CommentForm()
        return render(request, 'calc/leave_comment.html', locals())


def adding_new_furniture(request, calc_id):
    """Форма для добавления новой фурнитуры не из Базы данных."""
    if request.POST:
        form = FurnitureInCalcForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data)
            obj = FurnitureInCalc.objects.create(calc_id=calc_id,
                title=form.cleaned_data["title"],
                article=form.cleaned_data["article"],
                price=form.cleaned_data["price"],
                price_retail=form.cleaned_data["price_retail"],
                availability=form.cleaned_data["availability"],
                nmb=form.cleaned_data["nmb"])
            obj.save()
            return HttpResponseRedirect(reverse('calc_details_form', args = (calc_id,)))
        print('no valid')
        return render(request, 'calc/adding_new_furniture.html', locals())
    else:
        form = FurnitureInCalcForm()
        return render(request, 'calc/adding_new_furniture.html', locals())