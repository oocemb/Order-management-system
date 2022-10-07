from .models import FurnitureInCalc, Detail


def crud_furniture_in_calc(request):
    """Создание или удаление в случае флага is_delete деталей в расчёте."""
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
    """Создание или удаление в случае флага is_delete деталей в расчёте."""
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
            new_detail = Detail.objects.create(calc_id=calc_id, heigth=heigth,
                width=width, nmb=nmb, price_material=price_material) 
            new_detail.save(force_update=True)
        else:
            new_obj = Detail.objects.get(id=detail_id)
            new_obj.nmb = int(nmb)
            new_obj.save(force_update=True)


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