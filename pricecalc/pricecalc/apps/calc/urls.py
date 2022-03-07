from django.urls import path
from .views import *

#app_name = "calc"
urlpatterns = [
    path('calc/', calc_list, name = 'calc_list'),
    path('calc/<int:calc_id>/', details_list, name = 'details_list'),

    path('adding_detail/', adding_detail,  name='adding_detail'),
    path('adding_furniture/', adding_furniture,  name='adding_furniture'),

    path('<int:calc_id>/leave_comment/', comment, name = 'comment'),
    path('update_data/', update_data,  name='update_data'),
    
]