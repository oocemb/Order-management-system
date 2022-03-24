from django.urls import reverse
from django.shortcuts import render
from django.http import Http404, HttpResponseRedirect, JsonResponse
from django.contrib.auth.decorators import login_required
from .models import *
from .utils import *
from .forms import *
from .tasks import update_data_furniture

from .crawler import handle_parsing_data, multiprocessing_parsing


def adding_calc(request):
    
    if request.POST:
        form = CalcForm(request.POST)
        if form.is_valid():
            obj = Calc.objects.create(designer=request.user, title=form.cleaned_data["title"],
            tags=form.cleaned_data["tags"])
            obj.save()
            return HttpResponseRedirect(reverse('details_list', args = (obj.id,)))
        return render(request, 'calc/adding_calc.html', locals())  
    else:
        form = CalcForm()
        return render(request, 'calc/adding_calc.html', locals())



def calc_list(request):
    """ Показывает список текущих расчётов
    """
    if request.user.is_authenticated:
        if request.user.is_staff:
            calc_list = Calc.objects.order_by('-create_at')[:15]
        else:
            calc_list = Calc.objects.filter(designer=request.user).order_by('-create_at')

    return render(request, 'calc/calc_list.html', locals())


def update_data(request):
    update_data_furniture.delay()
    return HttpResponseRedirect(reverse('calc_list'))


def current_details_in_calc_and_main_calc_info(calc_id) -> dict:
    """Составляет словарь из информации о текущих делалях в расчёте 
    и информации о их количестве и общей стоимости
    """
    return_dict = dict()
    details_in_calc = Detail.objects.filter(calc=calc_id)     
    return_dict["details_total_nmb"] = sum(details.nmb for details in details_in_calc)
    return_dict["total_calc_price"] = sum(details.total_price for details in details_in_calc)
    return_dict["details"] = list()

    for item in details_in_calc:
        details_dict = dict()
        details_dict["id"] = item.id
        details_dict["heigth"] = item.heigth
        details_dict["width"] = item.width
        details_dict["nmb"] = item.nmb
        details_dict["price_material"] = item.price_material
        details_dict["total_price"] = item.total_price
        return_dict["details"].append(details_dict)
    
    return return_dict


def current_furniture_in_calc_and_main_calc_info(calc_id) -> dict:
    """Составляет словарь из информации о текущих делалях в расчёте 
    и информации о их количестве и общей стоимости
    TODO: Если удалять фурнитуру из базы данных, то они удаляются из рассчёта!!! 
    ForeingKey ставит (furniture_id = Null), ошибка и количество не меняется
    Может это и правильно если фурнитура удалена?
    """
    return_dict = dict()
    furniture_in_calc = FurnitureInCalc.objects.filter(calc=calc_id)     
    return_dict["furniture_total_nmb"] = sum(furniture.nmb for furniture in furniture_in_calc)
    return_dict["total_calc_price"] = sum(furniture.total_price for furniture in furniture_in_calc)
    return_dict["furniture"] = list()

    for item in furniture_in_calc:
        furniture_dict = dict()
        if item.furniture is not None:
            furniture_dict["furniture_id"] = item.furniture.id
        else:
            furniture_dict["furniture_id"] = 0
        furniture_dict["id"] = item.id
        furniture_dict["title"] = item.title
        furniture_dict["availability"] = item.availability
        furniture_dict["nmb"] = item.nmb
        furniture_dict["article"] = item.article
        furniture_dict["price"] = item.price_retail
        furniture_dict["total_price"] = item.total_price
        return_dict["furniture"].append(furniture_dict)
    
    return return_dict


def crud_details_in_calc(request):
    """Создание или удаление в случае флага is_delete деталей в расчёте
    """
    data = request.POST
    detail_id = data.get("detail_id")
    calc_id = data.get("calc_id")
    is_delete = data.get("is_delete")
    heigth = data.get("heigth")
    width = data.get("width")
    nmb = int(data.get("nmb"))
    price_material = data.get("price_material")
    if is_delete == "true":
        obj = Detail.objects.get(id=detail_id)
        obj.delete() 
    elif nmb > 0:
        if int(detail_id) == 0:
            new_detail = Detail.objects.create(calc_id=calc_id, heigth=heigth
            , width=width, nmb=nmb, price_material=price_material) 
            new_detail.save(force_update=True)
        else:
            new_obj = Detail.objects.get(id=detail_id)
            new_obj.nmb = int(nmb)
            new_obj.save(force_update=True)
        



def crud_furniture_in_calc(request):
    """Создание или удаление в случае флага is_delete деталей в расчёте
    """
    data = request.POST
    
    furniture_id = data.get("furniture_id")
    calc_id = data.get("calc_id")
    is_delete = data.get("is_delete")
    nmb = int(data.get("nmb"))
    if is_delete == "true":
        obj = FurnitureInCalc.objects.get(calc_id=calc_id, id=furniture_id)
        obj.delete() 
    elif nmb > 0:
        new_obj, created = FurnitureInCalc.objects.get_or_create(calc_id=calc_id
        , furniture_id=furniture_id, defaults={"nmb":nmb}) 
        if not created:
            new_obj.nmb = int(nmb)
            new_obj.save(force_update=True)



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


@login_required()
def details_list(request, calc_id):
    """ Показывает список деталей в конкретном расчёте (Ajax)
    """
    calc = Calc.objects.get(pk=calc_id)
    form = DetailForm

    furniture_list = Furniture.objects.all()
    handles_list = Handle.objects.all()
    latest_comment = Comment.objects.filter(calc=calc_id).order_by('-id')[:10]
    
    return render(request, 'calc/details_list.html', locals())



def comment(request, calc_id):
    try:
        a = Calc.objects.get( id = calc_id )
    except:
        raise Http404("Not found")

    a.comment_set.create(author_name = request.POST['name'], comment_text = request.POST['text'])
    return HttpResponseRedirect(reverse('details_list', args = (a.id,)))



def add_user(request):
    # a = User(user_name = request.POST['name'])
    # a.save()
    # можно сразу в базу без сейва a = User.objects.create(name = 123123)
    # регистронезависисый поиск xxx.objects.get(name__iexact = 'qweqwe')  - get возвр 1 обьект
    # лук ап контейнс  xxxx.objects.filter(name__contains = 'qweqwe') - фильрт возвр Кварисет
    # {{ post.body|truncatewords:15 }} - последние 15 слов из бади
    return HttpResponseRedirect(reverse('users'))  



def add_calculation(request, user_id):
    # calculation_set.create(price_title = request.POST['name'], price_date = timezone.now())
    return HttpResponseRedirect(reverse('calculation'))


