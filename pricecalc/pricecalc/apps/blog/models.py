from django.db import models
from django.urls import reverse
from base.services import gen_slug



class Tag(models.Model):
    """Класс тега к посту
    """
    title = models.CharField(max_length = 50)
    slug =  models.SlugField(max_length = 50, unique=True)

    class Meta:
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



class Post(models.Model):
    """Модель поста
    """
    title = models.CharField(max_length=150, db_index=True)
    slug = models.SlugField(max_length=150, blank=True)
    body = models.TextField(blank=True, db_index=True)
    tags = models.ManyToManyField('Tag', blank=True, related_name='posts')
    date_pub = models.DateTimeField(auto_now_add=True)

    def get_absolute_url(self):
        return reverse('postdetail', kwargs={'slug': self.slug})

    def get_update_url(self):
        return reverse('postupdate', kwargs={'slug': self.slug})
    
    def get_delete_url(self):
        return reverse('postdelete', kwargs={'slug': self.slug})

    def get_create_url(self):
        return reverse('postcreate')

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = gen_slug(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ['-date_pub']
