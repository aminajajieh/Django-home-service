from background_task import background
from django.contrib.auth.models import User
from .models import ClientService
@background(schedule=1)
def notify_user():
    s = ClientService.objects.all()
    for a in s:
        a.price += 1
        a.save()
