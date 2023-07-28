from django.db import models
from django.urls import reverse

from base.utils import gen_slug
from config.models import BaseModel


class Tag(BaseModel):
    title = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50, unique=True)

    class Meta:
        verbose_name = 'Тэг к статье'
        verbose_name_plural = 'Тэги к статьям'
        ordering = ['title']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('tagdetail', kwargs={'slug': self.slug})

    def get_update_url(self):
        return reverse('tagupdate', kwargs={'slug': self.slug})
    
    def get_delete_url(self):
        return reverse('tagdelete', kwargs={'slug': self.slug})
    
    def get_create_url(self):
        return reverse('tagcreate')


class Post(BaseModel):
    title = models.CharField(max_length=150, db_index=True)
    slug = models.SlugField(max_length=150, blank=True)
    body = models.TextField(blank=True, db_index=True)
    tags = models.ManyToManyField('Tag', blank=True, related_name='posts')
    date_pub = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'
        ordering = ['-date_pub']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = gen_slug(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('postdetail', kwargs={'slug': self.slug})

    def get_update_url(self):
        return reverse('postupdate', kwargs={'slug': self.slug})

    def get_delete_url(self):
        return reverse('postdelete', kwargs={'slug': self.slug})

    def get_create_url(self):
        return reverse('postcreate')
