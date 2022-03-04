from django.contrib import admin
from django.urls import path, include
from .views import *



urlpatterns = [
    path('admin/', admin.site.urls),
    path('', redirect_blog),
    path('', include('calc.urls')),
    path('', include('myauth.urls')),
    path('blog/', include('blog.urls')),
    path('', include('social_django.urls', namespace='social')),
    path('accounts/', include('django.contrib.auth.urls')),
]
