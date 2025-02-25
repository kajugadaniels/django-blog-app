from base.models import *
from django.shortcuts import render

def home(request):
    breakingNews = Article.objects.all().order_by('-id')[:4]

    context = {
        'breakingNews': breakingNews
    }

    return render(request, 'pages/index.html', context)