import datetime

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

from config.models import BaseModel


class CalcTag(BaseModel):
    """Модель категорий расчётов"""
    title = models.CharField(max_length=20)

    class Meta:
        verbose_name = 'Тэг расчёта'
        verbose_name_plural = 'Тэги расчётов'

    def __str__(self):
        return self.title


class Calc(BaseModel):
    """Модель расчёта"""
    designer = models.ForeignKey(User, blank=True, null=True, default=None, on_delete=models.DO_NOTHING)
    tags = models.ForeignKey(CalcTag, blank=True, null=True, default=None, on_delete=models.DO_NOTHING)  # tag
    title = models.CharField('Название расчёта', max_length=128)
    create_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Расчёт'
        verbose_name_plural = 'Расчёты'

    def __str__(self):
        return self.title

    def was_calc_recently(self):  # Можно использоваться для быстрого поиска недавних расчётов
        return self.create_at >= (timezone.now() - datetime.timedelta(day=7))


class Detail(BaseModel):
    """Модель детали в расчёте"""
    calc = models.ForeignKey(Calc, on_delete=models.CASCADE)
    height = models.PositiveIntegerField('Высота')
    width = models.PositiveIntegerField('Ширина')
    nmb = models.PositiveIntegerField('Количество')
    price_material = models.PositiveIntegerField('Цена м2')
    total_price = models.DecimalField('Стоимость', decimal_places=2, max_digits=10, default=0)

    class Meta:
        verbose_name = 'Деталь'
        verbose_name_plural = 'Детали'

    def __str__(self):
        return '{} - {}x{}-{}'.format(self.calc, self.height, self.width, self.nmb)

    def save(self, *args, **kwargs):
        # Автоматический расчёт общей стоимости при сохранении
        self.total_price = int(self.nmb) \
                           * int(self.height) * int(self.width) \
                           * int(self.price_material) \
                           / 10000  # Т.к. в сантиметрах делим на 10000
        super(Detail, self).save(*args, **kwargs)


class CategoryFurniture(BaseModel):
    """Модель категории фурнитуры"""
    title = models.CharField(max_length=100, default=None)

    class Meta:
        verbose_name = 'Категория фурнитуры'
        verbose_name_plural = 'Категории фурнитуры'

    def __str__(self):
        return self.title


class Furniture(BaseModel):
    """Модель фурнитуры"""
    category = models.ForeignKey(CategoryFurniture, on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=100, default=None)
    article = models.CharField(max_length=50, default=None)
    price = models.DecimalField(decimal_places=2, max_digits=8, default=None)
    price_retail = models.DecimalField(decimal_places=2, max_digits=8, blank=True, null=True)
    availability = models.CharField('Наличие', max_length=20, null=True, default=None)

    class Meta:
        verbose_name = 'Фурнитура'
        verbose_name_plural = 'Фурнитура'

    def __str__(self) -> str:
        return '%s - %s - %s - %s' % (self.category, self.title[:50], self.price, self.price_retail)


class FurnitureInCalc(BaseModel):
    """Модель фурнитуры в заказе"""
    calc = models.ForeignKey(Calc, on_delete=models.CASCADE)
    furniture = models.ForeignKey(Furniture, null=True, on_delete=models.SET_NULL)
    title = models.CharField('Название', max_length=100)
    article = models.CharField('Артикул', max_length=50, unique=True)
    price = models.DecimalField('Оптовая цена', decimal_places=2, max_digits=8)
    price_retail = models.DecimalField('Розничная цена', decimal_places=2, max_digits=8, default=1)
    availability = models.CharField('Наличие', max_length=20, null=True)
    nmb = models.PositiveIntegerField('Количество')
    total_price = models.DecimalField('Итого', decimal_places=2, max_digits=8)

    class Meta:
        verbose_name = 'Фурнитура в расчёте'
        verbose_name_plural = 'Фурнитура в расчёте'

    def __str__(self) -> str:
        return '%s - %s - %s - %s' % (self.calc.title, self.title[:50], self.price, self.price_retail)

    def save(self, *args, **kwargs) -> None:
        # Автоматический расчёт общей стоимости и параметров при добавлении
        if self.furniture is not None:
            self.title = self.furniture.title
            self.article = self.furniture.article
            self.price = self.furniture.price
            self.price_retail = self.furniture.price_retail
            self.availability = self.furniture.availability
        self.total_price = self.nmb * float(self.price_retail)
        super(FurnitureInCalc, self).save(*args, **kwargs)


class Ldstp(BaseModel):
    """Модель ЛДСП для информации о наличии цветов"""
    title = models.CharField(max_length=128)
    price = models.DecimalField(decimal_places=2, max_digits=8)
    availability = models.CharField(max_length=32)

    class Meta:
        verbose_name = 'ЛДСП'
        verbose_name_plural = 'ЛДСП'

    def __str__(self):
        return '%s - %s - %s' % (self.title, self.price, self.availability)


class Comment(BaseModel):
    """Модель комментария к расчёту"""
    calc = models.ForeignKey(Calc, on_delete=models.CASCADE)
    title = models.CharField('Тема', max_length=50)
    text = models.TextField('Текст комментария', max_length=1000)

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return '%s - %s' % (self.calc.title, self.title)


class Box(BaseModel):
    pass
