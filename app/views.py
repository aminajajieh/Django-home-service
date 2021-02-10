from django.shortcuts import render
from django.shortcuts import render
from .models import *
from django.shortcuts import render,get_object_or_404
from django.core.paginator import PageNotAnInteger,Paginator,EmptyPage
from django.views.generic import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.db.models import F
from django.db.models import Count
from django.db.models import Q
from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView, View
from django.conf import settings
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, View
from django.shortcuts import redirect
from django.utils import timezone
import uuid
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.core.paginator import PageNotAnInteger,Paginator,EmptyPage
from .forms import *

# Create your views here.
@login_required(login_url='/admin/login')
def worker(request,id):
    for i in ClientService.objects.all():
        i.save()
    worker = get_object_or_404(Worker,id=id)
    works = worker.works.filter(active=True)
    return render(request,'worker.html',context={'works':works,'worker':worker})
@login_required(login_url='/admin/login')
def client(request,id):
    for i in ClientService.objects.all():
        i.save()
    client = get_object_or_404(Client,id=id)
    services = client.services.filter(active=True)
    return render(request,'client.html',context={'works':services,'client':client})

def post(request,slug):
    for i in ClientService.objects.all():
        i.save()
    site = SiteEdit.objects.get(id=1)

    post = get_object_or_404(Posts,slug=slug)
    return render(request,'post.html',context={'post':post,'title':post.title,'site':site,'descripe':post.content,'tags':post.content})
def home(request):
    for i in ClientService.objects.all():
        i.save()
    site = SiteEdit.objects.get(id=1)
    img4 = '"'+str(site.img4.url)+'"'
    img5 = '"'+str(site.img5.url)+'"'
    img6 = '"'+str(site.img6.url)+'"'



    return render(request,'home.html',context={'img4':img4,'img5':img5,'img6':img6,'title':site.title,'site':site,'descripe':site.content,'tags':site.content})




def blog(request):
    for i in ClientService.objects.all():
        i.save()
    site = SiteEdit.objects.get(id=1)

    posts = Posts.objects.filter(active=True)
    paginator = Paginator(posts, 6)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_page)
    return render(request,'blog.html',context={'site':site,'page': page, 'posts':posts,'title': 'المقالات','descripe':site.content,'tags':site.content})

def about(request):
    for i in ClientService.objects.all():
        i.save()
    site = SiteEdit.objects.get(id=1)
    return render(request,'about.html',context={'site':site,'title':'من نحن','descripe':site.content,'tags':site.content})
def close(request):
    for i in ClientService.objects.all():
        i.save()
    site = SiteEdit.objects.get(id=1)

    return render(request,'close.html',context={'site':site})
def contact(request):
    for i in ClientService.objects.all():
        i.save()
    site = SiteEdit.objects.get(id=1)
    if request.method == 'POST':
        comment_form = Contact(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.save()
            messages.info(request, "تم الارسال بنجاح")
            comment_form = Contact()
    else:
        comment_form = Contact()
    return render(request,'contact-us.html',context={'title':'تواصل معنا','site':site,'form':comment_form,'descripe':site.content,'tags':site.content})
from background_task import background
from django.contrib.auth.models import User
from .models import ClientService

@background(schedule=1)
def notify_user():
    s = ClientService.objects.all()
    for a in s:
        a.save()
notify_user(schedule=1,repeat=3600, repeat_until=None)