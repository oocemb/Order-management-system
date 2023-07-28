from django.shortcuts import redirect


def redirect_main(request):
    """ Перенаправляет на основную страницу"""
    return redirect('calc_list', permanent=True)
