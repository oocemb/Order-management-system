from django.contrib import admin
from django.urls import path, include

from config.views import redirect_main


urlpatterns = [
    path('', redirect_main),
    path('', include('calc.urls')),
    path('', include('crawler.urls')),
    path('blog/', include('blog.urls')),

    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('', include('social_django.urls', namespace='social')),
]
