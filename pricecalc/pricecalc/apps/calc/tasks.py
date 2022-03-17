from http.client import HTTPException

from pricecalc.celery import app
from calc.crawler import multiproc


@app.task
def update_data_furniture():
    i = 1
    while i < 5:
        multiproc(i)
        print(f'loop # {i}')
        i += 1


# @app.task
# def send_spam_email():
#     for contact in User.objects.all():
#         send_email(
#             'You subscrib', # title
#             'We spam you', # text
#             'ooo@ooo.com', # from email
#             [contact.email],
#             fail_silently=False,
#         )

# my_task.apply_async((args,kwargs),(countdown=60),) # запустит через 60 сек а не сразу


@app.task(bind=True) # default_retry_delay=3 * 60
def update_data_regularly(self):
    i = 1
    while i < 3:  
        multiproc(i)
        i += 1
    try:
        return 'Success'
    except HTTPException as exc:
        raise self.retry(exc=exc, countdown=60)
    

