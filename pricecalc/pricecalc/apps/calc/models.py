import datetime
from turtle import title
from django.db import models
from django.utils import timezone
from social_django.models import UserSocialAuth
from django.contrib.auth.models import User



class CalcTag(models.Model):
    title = models.CharField(max_length=20)

    def __str__(self):
        return self.title

class Calc(models.Model):
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
    calc = models.ForeignKey(Calc, on_delete= models.CASCADE)
    heigth = models.PositiveIntegerField('Высота')
    width = models.PositiveIntegerField('Ширина')
    nmb = models.PositiveIntegerField('Количество')
    price_material = models.PositiveIntegerField('Цена м2')
    total_price = models.DecimalField('Стоимость', decimal_places=2, max_digits=10, default=0)
        
    def __str__(self):
        return '{} - {}x{}-{}'.format(self.calc, self.heigth, self.width, self.nmb)

    def save(self, *args,**kwargs): # т.к. в сантиметрах делим на 10000
        self.total_price = int(self.nmb) * int(self.heigth) * int(self.width) * int(self.price_material) / 10000
        super(Detail, self).save(*args,**kwargs)


        


class Comment(models.Model): # в единственном числе названия классов
    calc = models.ForeignKey(Calc, on_delete= models.CASCADE)
    name = models.CharField('name avtor', max_length = 50)
    text = models.CharField('текст комм', max_length = 50)

    def __str__(self):
        return self.author_name

    class Meta:
        verbose_name = 'Коментарий'
        verbose_name_plural = 'Коментарии'



class Furniture(models.Model):
    title = models.CharField(max_length=100, default=None)
    article = models.CharField(max_length=50, default=None)
    price = models.DecimalField(decimal_places=2, max_digits=8, default=None)
    availability = models.CharField(max_length=20, default=None)

    def __str__(self) -> str:
        return self.title[:30]

class FurnitureInCalc(models.Model):
    calc = models.ForeignKey(Calc, on_delete=models.CASCADE)
    furniture = models.ForeignKey(Furniture, null=True, on_delete=models.SET_NULL)
    title = models.CharField(max_length=100)
    article = models.CharField(max_length=50)
    price = models.DecimalField(decimal_places=2,max_digits=8)
    availability = models.CharField(max_length=20)
    nmb = models.PositiveIntegerField()
    total_price = models.DecimalField(decimal_places=2,max_digits=8)

    def save(self, *args, **kwargs) -> None:
        title = self.furniture.title
        self.title = title
        art = self.furniture.article
        self.article = art
        prc = self.furniture.price
        self.price = prc
        ava = self.furniture.availability
        self.availability = ava
        self.total_price = self.nmb * float(self.price)
        super(FurnitureInCalc, self).save(*args, **kwargs)


class Box(models.Model):
    pass



class Calculation(models.Model):
    title = models.CharField('price_title', max_length = 50)
    date = models.DateTimeField('price_date')



class SpecificationDetail(models.Model):
    calculation = models.ForeignKey(Calculation, on_delete= models.CASCADE)





#class Team(models.Model):
#    name = models.CharField(max_length=20)
#    TEAM_LVL = ( '10', '9', '8')
#    #TEAM_LVL = ( ('U9', 'Under 09s'), ('U10', 'Under 10s'))
#    team_level = models.CharField(max_length=10, choices=TEAM_LVL, default='10')


#a = Calc.object.get(id = 1)
        #a.comment.set_all() # вернёт все коменты
        #a.comment.set_create(name = 'Diz1', comment_text = 'wtf kuhen')
        #a.comment.set_create(name = 'Diz21', comment_text = 'wtf ku11hen')
        #a.comment.set_create(name = 'Diz13', comment_text = 'wtf kuhe33n')
        #a.comment.set.count() # ---> 3
        #a.comment.set.filter(....) 
        #cs = a.comment.set.filter(....) 
        #cs.delete()  # после присваивания удаляет эти коменты по фильтру уже из исходной таблицы

        #calc.object.filter(title__startswith = 'Кухня') вернёт все статьи с началом тайтла кухня
        #calc.object.filter(create_at__year = (current_year = timezone.now().year)) вернёт все статьи текущего года
