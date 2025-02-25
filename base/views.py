from base.models import *
from datetime import timedelta
from django.utils import timezone
from django.shortcuts import render

def home(request):
    breakingNews = Article.objects.all().order_by('-id')[:4]
    
    # Define the time threshold for 24 hours ago
    timeThreshold = timezone.now() - timedelta(hours=24)
    # Retrieve the article with the most views in the last 24 hours
    topArticle = Article.objects.filter(created_at__gte=timeThreshold).order_by('-views').first()
    
    context = {
        'breakingNews': breakingNews,
        'topArticle': topArticle,
    }
    
    return render(request, 'pages/index.html', context)
