from django.http import HttpResponseRedirect
from django.urls import reverse

from crawler.tasks import update_makmart_data_task, update_ldstp_task


def update_data(request):
    """Обновление базы данных фурнитуры"""
    update_makmart_data_task.delay()
    return HttpResponseRedirect(reverse('calc_list'))


def update_ldsp(request):
    """Обновление базы данных ЛДСП"""
    update_ldstp_task.delay()
    return HttpResponseRedirect(reverse('calc_list'))
