from django.urls import path
from .views import *

#app_name = "calc"
urlpatterns = [
    path('users/', users, name = 'users'),
    path('add_user/', add_user, name = 'add_user'),
    path('calc/', index_calc, name = 'index_calc'),
    path('calcul/<int:user_id>/', calculation, name = 'calculation'),
    path('<int:user_id>/add_calculation/', add_calculation, name = 'add_calculation'),
    path('<int:calc_id>/', detail, name = 'detail'),
    path('<int:calc_id>/leave_comment/', comment, name = 'comment'),
]