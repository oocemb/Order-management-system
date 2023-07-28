from django.urls import reverse
from django.shortcuts import render
from django.http import HttpResponseRedirect, JsonResponse
from django.http.request import HttpRequest
from django.contrib.auth.decorators import login_required

from calc.models import Calc, Furniture, FurnitureInCalc, Ldstp, Comment, Detail
from calc.forms import CalcForm, CommentForm, FurnitureInCalcForm
from calc.utils import current_furniture_in_calc_and_main_calc_info, current_details_in_calc_and_main_calc_info


def calcs_list(request):
    """Показывает список текущих расчётов"""
    if request.user.is_authenticated:
        if request.user.is_staff:
            calc_list = Calc.objects.order_by('-create_at')[:15]
        else:
            calc_list = Calc.objects.filter(designer=request.user).order_by('-create_at')
    return render(request, 'calc/calc_list.html', locals())


def adding_calc(request):
    """Добавляет новый расчёт"""
    if request.POST:
        form = CalcForm(request.POST)
        if form.is_valid():
            obj = Calc.objects.create(designer=request.user, title=form.cleaned_data["title"],
                                      tags=form.cleaned_data["tags"])
            obj.save()
            return HttpResponseRedirect(reverse('calc_details', args=(obj.id,)))
        return render(request, 'calc/adding_calc.html', locals())
    else:
        form = CalcForm()
        return render(request, 'calc/adding_calc.html', locals())


@login_required
def calc_details(request: HttpRequest, calc_id: int):
    """Подробная информация по расчёту
    Инфо по текущим деталям и текущей фурнитуре получаем через Ajax"""
    calc = Calc.objects.get(pk=calc_id)
    if calc.designer != request.user and not request.user.is_staff:
        return HttpResponseRedirect(reverse('calc_list'))
    furniture = Furniture.objects.all()
    standard_furniture = furniture.filter(category_id=1)
    kitchen_furniture = furniture.filter(category_id=2)
    countertops_furniture = furniture.filter(category_id=3)
    silk_and_drying_furniture = furniture.filter(category_id=4)
    lift_and_box_furniture = furniture.filter(category_id=5)
    mensolo_hangers_legs_furniture = furniture.filter(category_id=6)
    wardrobe_furniture = furniture.filter(category_id=7)
    handle_furniture = furniture.filter(category_id=8)
    ldsp_list = Ldstp.objects.all()
    latest_comment = Comment.objects.filter(calc_id=calc_id).order_by('-id')
    return render(request, 'calc/calc_details.html', locals())


def crud_detail(request):
    """Создание или удаление в случае флага is_delete деталей в расчёте"""
    data = request.POST
    detail_id = data.get("detail_id")
    calc_id = data.get("calc_id")
    is_delete = data.get("is_delete")
    height = data.get("height")
    width = data.get("width")
    nmb = int(data.get("nmb"))
    price_material = data.get("price_material")
    if is_delete == "true":
        obj = Detail.objects.get(id=detail_id)
        obj.delete()
    elif nmb > 0:
        if int(detail_id) == 0:
            new_detail = Detail.objects.create(calc_id=calc_id, height=height,
                                               width=width, nmb=nmb, price_material=price_material)
            new_detail.save(force_update=True)
        else:
            new_obj = Detail.objects.get(id=detail_id)
            new_obj.nmb = int(nmb)
            new_obj.save(force_update=True)
    return JsonResponse(current_details_in_calc_and_main_calc_info(calc_id=calc_id))


def crud_furniture(request):
    """Создание или удаление в случае флага is_delete деталей в расчёте"""
    data = request.POST
    furniture_id = data.get("furniture_id")
    calc_id = data.get("calc_id")
    is_delete = data.get("is_delete")
    nmb = int(data.get("nmb"))
    if is_delete == "true":
        obj = FurnitureInCalc.objects.get(calc_id=calc_id, id=furniture_id)
        obj.delete()
    elif nmb > 0:
        new_obj, created = FurnitureInCalc.objects.get_or_create(calc_id=calc_id,
                                                                 furniture_id=furniture_id, defaults={"nmb": nmb})
        if not created:
            new_obj.nmb = int(nmb)
            new_obj.save(force_update=True)
    return JsonResponse(current_furniture_in_calc_and_main_calc_info(calc_id=calc_id))


def leave_comment(request, calc_id):
    """Форма для добавления нового комментария"""
    if request.POST:
        form = CommentForm(request.POST)
        if form.is_valid():
            obj = Comment.objects.create(calc_id=calc_id,
                                         title=form.cleaned_data["title"],
                                         text=form.cleaned_data["text"])
            obj.save()
            return HttpResponseRedirect(reverse('calc_details', args=(calc_id,)))
        return render(request, 'calc/leave_comment.html', locals())
    else:
        form = CommentForm()
        return render(request, 'calc/leave_comment.html', locals())


def adding_new_furniture(request, calc_id):
    """Форма для добавления новой фурнитуры не из Базы данных"""
    if request.POST:
        form = FurnitureInCalcForm(request.POST)
        if form.is_valid():
            obj = FurnitureInCalc.objects.create(
                calc_id=calc_id,
                title=form.cleaned_data["title"],
                article=form.cleaned_data["article"],
                price=form.cleaned_data["price"],
                price_retail=form.cleaned_data["price_retail"],
                availability=form.cleaned_data["availability"],
                nmb=form.cleaned_data["nmb"])
            obj.save()
            return HttpResponseRedirect(reverse('calc_details', args=(calc_id,)))
        return render(request, 'calc/adding_new_furniture.html', locals())
    else:
        form = FurnitureInCalcForm()
        return render(request, 'calc/adding_new_furniture.html', locals())
