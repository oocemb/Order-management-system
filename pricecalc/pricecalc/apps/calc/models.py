import datetime
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class CalcTag(models.Model):
    """Модель тэгов(категорий) расчётов."""
    title = models.CharField(max_length=20)

    class Meta:
        verbose_name = 'Тэг расчёта'
        verbose_name_plural = 'Тэги расчётов'

    def __str__(self):
        return self.title


class Calc(models.Model):
    """Модель расчёта."""
    designer = models.ForeignKey(User, blank=True, null=True, default=None, on_delete=models.DO_NOTHING)
    tags = models.ForeignKey(CalcTag, blank=True, null=True, default=None, on_delete=models.DO_NOTHING)
    title = models.CharField('Название расчёта', max_length = 64) # ~200
    create_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Расчёт'
        verbose_name_plural = 'Расчёты'

    def __str__(self):
        return self.title

    def was_calc_recently(self):
        return self.create_at >= (timezone.now() - datetime.timedelta(day=7))


class Detail(models.Model):
    """Модель детали в расчёте."""
    calc = models.ForeignKey(Calc, on_delete= models.CASCADE)
    heigth = models.PositiveIntegerField('Высота')
    width = models.PositiveIntegerField('Ширина')
    nmb = models.PositiveIntegerField('Количество')
    price_material = models.PositiveIntegerField('Цена м2')
    total_price = models.DecimalField('Стоимость', decimal_places=2, max_digits=10, default=0)

    class Meta:
        verbose_name = 'Деталь'
        verbose_name_plural = 'Детали'

    def __str__(self):
        return '{} - {}x{}-{}'.format(self.calc, self.heigth, self.width, self.nmb)

    def save(self, *args,**kwargs):
        # Автоматический расчёт общей стоимости при сохранении
        self.total_price = int(self.nmb) \
            * int(self.heigth) * int(self.width) \
            * int(self.price_material) \
            / 10000 # т.к. в сантиметрах делим на 10000
        super(Detail, self).save(*args,**kwargs)


class CategoryFurniture(models.Model):
    """Модель категории фурнитуры."""
    title = models.CharField(max_length=100, default=None)

    class Meta:
        verbose_name = 'Категория фурнитуры'
        verbose_name_plural = 'Категории фурнитуры'

    def __str__(self) -> str:
        return self.title


class Furniture(models.Model):
    """Модель фурнитуры."""
    category = models.ForeignKey(CategoryFurniture, on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=100, default=None)
    article = models.CharField(max_length=50, default=None)
    price = models.DecimalField(decimal_places=2, max_digits=8, default=None)
    price_retail = models.DecimalField(decimal_places=2, max_digits=8, blank=True, null=True)
    availability = models.CharField('Наличие', max_length=20, default=None)

    class Meta:
        verbose_name = 'Фурнитура'
        verbose_name_plural = 'Фурнитура'

    def __str__(self) -> str:
        return '%s - %s - %s - %s' %(self.category, self.title[:50], self.price, self.price_retail)


class FurnitureInCalc(models.Model):
    """Модель фурнитуры в заказе."""
    calc = models.ForeignKey(Calc, on_delete=models.CASCADE)
    furniture = models.ForeignKey(Furniture, null=True, on_delete=models.SET_NULL)
    title = models.CharField(max_length=100)
    article = models.CharField(max_length=50)
    price = models.DecimalField(decimal_places=2,max_digits=8)
    price_retail = models.DecimalField(decimal_places=2,max_digits=8, default=1)
    availability = models.CharField(max_length=20)
    nmb = models.PositiveIntegerField()
    total_price = models.DecimalField(decimal_places=2,max_digits=8)

    class Meta:
        verbose_name = 'Фурнитура в расчёте'
        verbose_name_plural = 'Фурнитура в расчёте'

    def __str__(self) -> str:
        return '%s - %s - %s - %s' %(self.calc.title, self.title[:50], self.price, self.price_retail)

    def save(self, *args, **kwargs) -> None:
        # Автоматический расчёт общей стоимости и параметров при добавлении
        self.title = self.furniture.title 
        self.article = self.furniture.article
        self.price = self.furniture.price
        self.price_retail = self.furniture.price_retail
        self.availability = self.furniture.availability
        self.total_price = self.nmb * float(self.price_retail)
        super(FurnitureInCalc, self).save(*args, **kwargs)


class Ldstp(models.Model):
    """Модель ЛДСП для информации о начичии цветов."""
    title = models.CharField(max_length=128)
    price = models.DecimalField(decimal_places=2, max_digits=8)
    availability = models.CharField(max_length=32)

    class Meta:
        verbose_name = 'ЛДСП'
        verbose_name_plural = 'ЛДСП'

    def __str__(self):
        return self.author_name

class Comment(models.Model):
    """Модель коментария к расчёту."""
    calc = models.ForeignKey(Calc, on_delete= models.CASCADE)
    name = models.CharField('Тема', max_length = 50)
    text = models.TextField('Текст коментария', max_length = 1000)

    class Meta:
        verbose_name = 'Коментарий'
        verbose_name_plural = 'Коментарии'

    def __str__(self):
        return '%s - %s' % (self.calc.title, self.name)


class Box(models.Model):
    pass