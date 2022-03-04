from pyexpat import model
import re
from statistics import mode
from tabnanny import verbose
from time import time
from django.db import models
import datetime
from django.utils import timezone
from django.urls import reverse
from django.utils.text import slugify

class Calc(models.Model):
    calc_title = models.CharField('название калькулятора', max_length = 30) # ~200
    calc_text = models.TextField('текст кальк') # 20-30k ~
    calc_date = models.DateTimeField('дата рассчёта')

    class Meta:
        verbose_name = 'Калькуль'
        verbose_name_plural = 'Калькули'

    def __str__(self):
        return self.calc_title

    def was_calc_recently(self):
        return self.calc_date >= (timezone.now() - datetime.timedelta(day=7))

        #a = Calc.object.get(id = 1)
        #a.comment.set_all() # вернёт все коменты
        #a.comment.set_create(author_name = 'Diz1', comment_text = 'wtf kuhen')
        #a.comment.set_create(author_name = 'Diz21', comment_text = 'wtf ku11hen')
        #a.comment.set_create(author_name = 'Diz13', comment_text = 'wtf kuhe33n')
        #a.comment.set.count() # ---> 3
        #a.comment.set.filter(....) 
        #cs = a.comment.set.filter(....) 
        #cs.delete()  # после присваивания удаляет эти коменты по фильтру уже из исходной таблицы

        #calc.object.filter(calc_title__startswith = 'Кухня') вернёт все статьи с началом тайтла кухня
        #calc.object.filter(calc_date__year = (current_year = timezone.now().year)) вернёт все статьи текущего года

class Comment(models.Model): # в единственном числе названия классов
    calc = models.ForeignKey(Calc, on_delete= models.CASCADE)
    author_name = models.CharField('name avtor', max_length = 50)
    comment_text = models.CharField('текст комм', max_length = 50)

    def __str__(self):
        return self.author_name

    class Meta:
        verbose_name = 'комент'
        verbose_name_plural = 'коменты'

class User(models.Model):
    user_name = models.CharField('user_name', max_length = 50)

    def get_absolute_url(self):
        return reverse('calc:calculation', kwargs = {'user_id': self.id})


class Furniture(models.Model):
    pass


class Box(models.Model):
    pass


class Calculation(models.Model):
    user = models.ForeignKey(User, on_delete= models.CASCADE)
    price_title = models.CharField('price_title', max_length = 50)
    price_date = models.DateTimeField('price_date')


class SpecificationDetail(models.Model):
    calculation = models.ForeignKey(Calculation, on_delete= models.CASCADE)


class Detail(models.Model):
    specdetail = models.ForeignKey(SpecificationDetail, on_delete= models.CASCADE)
    det_heigth = models.IntegerField('det_higth')
    det_widht = models.IntegerField('det_widht')
    det_material = models.TextField('det_material')
        


#class Team(models.Model):
#    name = models.CharField(max_length=20)
#    TEAM_LVL = ( '10', '9', '8')
#    #TEAM_LVL = ( ('U9', 'Under 09s'), ('U10', 'Under 10s'))
#    team_level = models.CharField(max_length=10, choices=TEAM_LVL, default='10')