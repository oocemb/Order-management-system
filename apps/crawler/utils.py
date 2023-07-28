# Not used now
import requests


def calculate_furniture_price(price: int | float) -> float:
    """Рассчитывает цену фурнитуры по заданной формуле"""
    MULTIPLIER = 1.5
    MULTIPLIER_MAX = 1.4
    COEFFICIENT_MIN = 100
    COEFFICIENT = 500
    MAX_PRICE = 10000
    MIN_PRICE = 1500
    if price < MIN_PRICE:
        return round(price * MULTIPLIER + COEFFICIENT_MIN, 2)
    elif price > MAX_PRICE:
        return round(price * MULTIPLIER_MAX, 2)
    else:
        return round(price * MULTIPLIER + COEFFICIENT, 2)


def get_http(url: str):
    """Получает http response от получаемого URL."""
    response = requests.get(url)
    return response


def get_html(url: str, params: str = ""):
    """Получает Html код страницы по URL и заданным параметрам"""
    try:
        response = requests.get(url, params=params, timeout=20)
    except requests.exceptions.ConnectTimeout:  # TODO: backoff
        return False
    return response.text
