from base.models import *
from datetime import timedelta
from django.utils import timezone
from django.db.models import Count
from django.shortcuts import render

def home(request):
    breakingNews = Article.objects.all().order_by('-id')[:4]
    
    # Define the time threshold for 24 hours ago
    timeThreshold = timezone.now() - timedelta(hours=24)
    
    # Retrieve the article with the most views in the last 24 hours
    topArticle = Article.objects.filter(created_at__gte=timeThreshold).order_by('-views').first()
    
    # Retrieve 3 trending articles from the last 24 hours, excluding the topArticle to avoid duplication
    if topArticle:
        trendingArticles = Article.objects.filter(created_at__gte=timeThreshold)\
                                          .exclude(id=topArticle.id)\
                                          .order_by('-views')[:3]
    else:
        trendingArticles = Article.objects.filter(created_at__gte=timeThreshold)\
                                          .order_by('-views')[:3]
    
    # Retrieve 2 articles in random order
    randomArticles = Article.objects.all().order_by('?')[:2]
    
    # Retrieve all categories
    categories = Category.objects.all()
    
    # Retrieve the recent article from the last 24 hours (most recent creation date)
    recentArticle = Article.objects.filter(created_at__gte=timeThreshold)\
                                   .order_by('-created_at')\
                                   .first()
    
    # Retrieve 6 articles, one from each category (for 6 randomly selected categories)
    categoryArticles = []
    categoriesList = list(Category.objects.all())
    random.shuffle(categoriesList)
    for category in categoriesList:
        article = Article.objects.filter(category=category).order_by('?').first()
        if article:
            categoryArticles.append(article)
            if len(categoryArticles) == 6:
                break
    
    # Advanced logic:
    # Determine the category that has the most articles overall.
    mostPopulatedCategory = Category.objects.annotate(articleCount=Count('article'))\
                                            .order_by('-articleCount')\
                                            .first()
    # From that category, retrieve one article that is recent (within the last 24 hours) and has the most views.
    if mostPopulatedCategory:
        advancedArticle = Article.objects.filter(category=mostPopulatedCategory, created_at__gte=timeThreshold)\
                                           .order_by('-views')\
                                           .first()
    else:
        advancedArticle = None

    # Retrieve 3 related articles to the advancedArticle.
    # Related articles are defined as those in the same category as advancedArticle, created in the last 24 hours, and not the advancedArticle itself.
    if advancedArticle:
        relatedArticles = Article.objects.filter(
            category=advancedArticle.category,
            created_at__gte=timeThreshold
        ).exclude(id=advancedArticle.id).order_by('-created_at')[:3]
    else:
        relatedArticles = None

    # New logic: Retrieve the most liked article in the last 24 hours.
    # Annotate each article with its like count using the reverse accessor 'like'
    mostLikedArticle = Article.objects.filter(created_at__gte=timeThreshold)\
        .annotate(like_count=Count('like'))\
        .order_by('-like_count')\
        .first()
    
    context = {
        'breakingNews': breakingNews,
        'topArticle': topArticle,
        'trendingArticles': trendingArticles,
        'randomArticles': randomArticles,
        'categories': categories,
        'recentArticle': recentArticle,
        'categoryArticles': categoryArticles,
        'advancedArticle': advancedArticle,
        'relatedArticles': relatedArticles,
        'mostLikedArticle': mostLikedArticle,
    }
    
    return render(request, 'pages/index.html', context)