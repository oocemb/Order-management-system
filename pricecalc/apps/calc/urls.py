from django.urls import path
from .views import *


#app_name = "calc"
urlpatterns = [
    path('calc/', calc_list, name = 'calc_list'),
    path('adding_calc/', adding_calc, name = 'adding_calc'),
    path('calc/<int:calc_id>/', calc_details_form, name = 'calc_details_form'),

    path('adding_detail/', adding_detail,  name='adding_detail'),
    path('adding_furniture/', adding_furniture,  name='adding_furniture'),
    path('leave_comment/<int:calc_id>/', leave_comment, name = 'leave_comment'),
    path('adding_new_furniture/<int:calc_id>/', adding_new_furniture, name = 'adding_new_furniture'),

    path('update_data/', update_data,  name='update_data'),
    path('update_ldst/', update_ldsp,  name='update_ldst'),
]