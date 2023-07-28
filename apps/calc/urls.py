from django.urls import path

from calc.views import (
    calcs_list, adding_calc, calc_details, crud_furniture, crud_detail, leave_comment, adding_new_furniture
)

# app_name = "calc"
urlpatterns = [
    path('calcs/', calcs_list, name='calc_list'),
    path('adding_calc/', adding_calc, name='adding_calc'),
    path('calc/<int:calc_id>/', calc_details, name='calc_details'),

    path('crud_detail/', crud_detail, name='crud_detail'),
    path('crud_furniture/', crud_furniture, name='crud_furniture'),
    path('leave_comment/<int:calc_id>/', leave_comment, name='leave_comment'),
    path('adding_new_furniture/<int:calc_id>/', adding_new_furniture, name='adding_new_furniture'),
]
