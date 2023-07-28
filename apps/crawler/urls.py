from django.urls import path
from crawler.views import update_data, update_ldsp


app_name = "crawler"
urlpatterns = [
    path('update_data/', update_data, name='update_data'),
    path('update_ldst/', update_ldsp, name='update_ldst'),
]
