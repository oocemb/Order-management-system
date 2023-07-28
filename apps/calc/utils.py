from calc.models import FurnitureInCalc, Detail


def current_furniture_in_calc_and_main_calc_info(calc_id: int) -> dict:
    """Составляет словарь из информации о текущей фурнитуре в расчёте
    её количестве и общей стоимости
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
        if item.furniture is not None:  # Костыль при удалении
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


def current_details_in_calc_and_main_calc_info(calc_id: int) -> dict:
    """Составляет словарь из информации о текущих деталях в расчёте
    их количестве и общей стоимости"""
    return_dict = dict()
    details_in_calc = Detail.objects.filter(calc=calc_id)
    return_dict["details_total_nmb"] = sum(details.nmb for details in details_in_calc)
    return_dict["total_calc_price"] = sum(details.total_price for details in details_in_calc)
    return_dict["details"] = list()

    for item in details_in_calc:
        details_dict = dict()
        details_dict["id"] = item.id
        details_dict["height"] = item.height
        details_dict["width"] = item.width
        details_dict["nmb"] = item.nmb
        details_dict["price_material"] = item.price_material
        details_dict["total_price"] = item.total_price
        return_dict["details"].append(details_dict)
    return return_dict
