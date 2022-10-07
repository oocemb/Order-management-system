from django.contrib import admin
from django.urls import path, include
from .views import *



urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('calc.urls')),
    path('blog/', include('blog.urls')),
    path('', redirect_main),
    path('', include('social_django.urls', namespace='social')),
    path('accounts/', include('django.contrib.auth.urls')),
]
