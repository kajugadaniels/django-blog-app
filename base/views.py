from base.models import *
from django.shortcuts import render

def home(request):
    mostRecent = Article.objects.all().order_by('-id')[:2]

    context = {
        'mostRecent': mostRecent
    }

    return render(request, 'pages/index.html', context)