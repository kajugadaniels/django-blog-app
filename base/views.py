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
    if advancedArticle:
        relatedArticles = Article.objects.filter(
            category=advancedArticle.category,
            created_at__gte=timeThreshold
        ).exclude(id=advancedArticle.id).order_by('-created_at')[:3]
    else:
        relatedArticles = None

    # Retrieve the most liked article in the last 24 hours.
    mostLikedArticle = Article.objects.filter(created_at__gte=timeThreshold)\
        .annotate(like_count=Count('like'))\
        .order_by('-like_count')\
        .first()
    
    # Retrieve 3 articles with the most comments (ordered by comment count then by like count)
    mostCommentedArticles = Article.objects.annotate(
        comment_count=Count('comment'),
        like_count=Count('like')
    ).order_by('-comment_count', '-like_count')[:3]
    
    # Retrieve the most viewed article in the last 7 days.
    weekTimeThreshold = timezone.now() - timedelta(days=7)
    mostViewedWeeklyArticle = Article.objects.filter(created_at__gte=weekTimeThreshold)\
                                              .order_by('-views')\
                                              .first()
    
    # Retrieve 3 more most viewed articles in the last 7 days (excluding the one above)
    if mostViewedWeeklyArticle:
        mostViewedWeeklyArticles = Article.objects.filter(created_at__gte=weekTimeThreshold)\
                                                  .exclude(id=mostViewedWeeklyArticle.id)\
                                                  .order_by('-views')[:3]
    else:
        mostViewedWeeklyArticles = Article.objects.filter(created_at__gte=weekTimeThreshold)\
                                                  .order_by('-views')[:3]
    
    # NEW LOGIC: For one random category, retrieve:
    # 1. One recent article in that category.
    # 2. Four most viewed articles in that category (excluding the recent article if it exists).
    # 3. Two articles with the most comments in that category (excluding articles from (1) & (2)).
    randomCategory = Category.objects.order_by('?').first()
    if randomCategory:
        recentArticleInCategory = Article.objects.filter(category=randomCategory).order_by('-created_at').first()
        
        # Retrieve four most viewed articles in the category, excluding the recent article if exists.
        if recentArticleInCategory:
            mostViewedArticlesInCategory = list(
                Article.objects.filter(category=randomCategory).exclude(id=recentArticleInCategory.id)
                .order_by('-views')
            )
        else:
            mostViewedArticlesInCategory = list(
                Article.objects.filter(category=randomCategory).order_by('-views')
            )
        mostViewedArticlesInCategory = mostViewedArticlesInCategory[:4]
        
        # Exclude articles already selected in (1) and (2) from most commented selection.
        excluded_ids = set()
        if recentArticleInCategory:
            excluded_ids.add(recentArticleInCategory.id)
        for art in mostViewedArticlesInCategory:
            excluded_ids.add(art.id)
        
        mostCommentedArticlesInCategory = list(
            Article.objects.filter(category=randomCategory).exclude(id__in=excluded_ids)
            .annotate(comment_count=Count('comment'))
            .order_by('-comment_count')
        )[:2]
    else:
        randomCategory = None
        recentArticleInCategory = None
        mostViewedArticlesInCategory = []
        mostCommentedArticlesInCategory = []
    
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
        'mostCommentedArticles': mostCommentedArticles,
        'mostViewedWeeklyArticle': mostViewedWeeklyArticle,
        'mostViewedWeeklyArticles': mostViewedWeeklyArticles,
        # New random category block
        'randomCategory': randomCategory,
        'recentArticleInCategory': recentArticleInCategory,
        'mostViewedArticlesInCategory': mostViewedArticlesInCategory,
        'mostCommentedArticlesInCategory': mostCommentedArticlesInCategory,
    }
    
    return render(request, 'pages/index.html', context)