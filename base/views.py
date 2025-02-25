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
    
    # Retrieve 3 trending articles from the last 24 hours, excluding the topArticle to avoid duplication
    if topArticle:
        trendingArticles = Article.objects.filter(created_at__gte=timeThreshold).exclude(id=topArticle.id).order_by('-views')[:3]
    else:
        trendingArticles = Article.objects.filter(created_at__gte=timeThreshold).order_by('-views')[:3]
    
    # Retrieve 2 articles in random order
    randomArticles = Article.objects.all().order_by('?')[:2]
    
    context = {
        'breakingNews': breakingNews,
        'topArticle': topArticle,
        'trendingArticles': trendingArticles,
        'randomArticles': randomArticles,
    }
    
    return render(request, 'pages/index.html', context)
