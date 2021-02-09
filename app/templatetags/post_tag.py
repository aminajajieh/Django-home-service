from django import template
from app.models import Posts
from django.shortcuts import render,get_object_or_404


register = template.Library()

@register.inclusion_tag('latest_posts.html')
def latest_posts():

    context = {
        'l_posts': Posts.objects.filter(active=True)[0:2],
    }
    return context