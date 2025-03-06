import random
from datetime import timedelta
from django.utils import timezone
from django.db.models import Count
from django.shortcuts import render, get_object_or_404
from django.contrib.auth import get_user_model
from base.models import Article, Category, Tag

def home(request):
    """
    Home view: Retrieves published articles and associated data for the homepage.
    Only articles with status 'published' are shown.
    """
    User = get_user_model()
    
    breakingNews = Article.objects.filter(status='published').order_by('-id')[:4]
    
    # Define the time thresholds.
    timeThreshold = timezone.now() - timedelta(hours=24)
    weekTimeThreshold = timezone.now() - timedelta(days=7)
    
    # Retrieve the article with the most views in the last 24 hours.
    topArticle = Article.objects.filter(status='published', created_at__gte=timeThreshold)\
                                .order_by('-views').first()
    
    # Retrieve 3 trending articles from the last 24 hours, excluding the topArticle.
    if topArticle:
        trendingArticles = Article.objects.filter(status='published', created_at__gte=timeThreshold)\
                                          .exclude(id=topArticle.id)\
                                          .order_by('-views')[:3]
    else:
        trendingArticles = Article.objects.filter(status='published', created_at__gte=timeThreshold)\
                                          .order_by('-views')[:3]
    
    # Retrieve 2 articles in random order.
    randomArticles = Article.objects.filter(status='published').order_by('?')[:2]
    
    # Retrieve all categories.
    categories = Category.objects.all()
    
    # Retrieve the most recent article from the last 24 hours.
    recentArticle = Article.objects.filter(status='published', created_at__gte=timeThreshold)\
                                   .order_by('-created_at')\
                                   .first()
    
    # Retrieve 6 articles (one from each of 6 randomly selected categories).
    categoryArticles = []
    categoriesList = list(Category.objects.all())
    random.shuffle(categoriesList)
    for category in categoriesList:
        article = Article.objects.filter(status='published', category=category).order_by('?').first()
        if article:
            categoryArticles.append(article)
            if len(categoryArticles) == 6:
                break
    
    # Advanced logic: Determine the category with the most articles.
    mostPopulatedCategory = Category.objects.annotate(articleCount=Count('article'))\
                                            .order_by('-articleCount')\
                                            .first()
    if mostPopulatedCategory:
        advancedArticle = Article.objects.filter(status='published', category=mostPopulatedCategory, created_at__gte=timeThreshold)\
                                           .order_by('-views')\
                                           .first()
    else:
        advancedArticle = None

    # Retrieve 3 related articles to the advancedArticle.
    if advancedArticle:
        relatedArticles = Article.objects.filter(status='published',
                                                   category=advancedArticle.category,
                                                   created_at__gte=timeThreshold)\
                                          .exclude(id=advancedArticle.id)\
                                          .order_by('-created_at')[:3]
    else:
        relatedArticles = None

    # Retrieve the most liked article in the last 24 hours.
    mostLikedArticle = Article.objects.filter(status='published', created_at__gte=timeThreshold)\
                                      .annotate(like_count=Count('like'))\
                                      .order_by('-like_count')\
                                      .first()
    
    # Retrieve 3 articles with the most comments.
    mostCommentedArticles = Article.objects.filter(status='published')\
                                           .annotate(comment_count=Count('comment'),
                                                     like_count=Count('like'))\
                                           .order_by('-comment_count', '-like_count')[:3]
    
    # Retrieve the most viewed article in the last 7 days.
    mostViewedWeeklyArticle = Article.objects.filter(status='published', created_at__gte=weekTimeThreshold)\
                                              .order_by('-views')\
                                              .first()
    
    # Retrieve 3 more most viewed articles in the last 7 days (excluding the one above).
    if mostViewedWeeklyArticle:
        mostViewedWeeklyArticles = Article.objects.filter(status='published', created_at__gte=weekTimeThreshold)\
                                                  .exclude(id=mostViewedWeeklyArticle.id)\
                                                  .order_by('-views')[:3]
    else:
        mostViewedWeeklyArticles = Article.objects.filter(status='published', created_at__gte=weekTimeThreshold)\
                                                  .order_by('-views')[:3]
    
    # NEW LOGIC: For one random category, retrieve:
    # (a) One recent article.
    # (b) Four most viewed articles (excluding the recent one).
    # (c) Two articles with the most comments (excluding those already selected).
    randomCategory = Category.objects.order_by('?').first()
    if randomCategory:
        recentArticleInCategory = Article.objects.filter(status='published', category=randomCategory)\
                                                   .order_by('-created_at')\
                                                   .first()
        if recentArticleInCategory:
            mostViewedArticlesInCategory = list(
                Article.objects.filter(status='published', category=randomCategory)
                .exclude(id=recentArticleInCategory.id)
                .order_by('-views')
            )
        else:
            mostViewedArticlesInCategory = list(
                Article.objects.filter(status='published', category=randomCategory)
                .order_by('-views')
            )
        mostViewedArticlesInCategory = mostViewedArticlesInCategory[:4]
        
        excluded_ids = set()
        if recentArticleInCategory:
            excluded_ids.add(recentArticleInCategory.id)
        for art in mostViewedArticlesInCategory:
            excluded_ids.add(art.id)
        
        mostCommentedArticlesInCategory = list(
            Article.objects.filter(status='published', category=randomCategory)
            .exclude(id__in=excluded_ids)
            .annotate(comment_count=Count('comment'))
            .order_by('-comment_count')
        )[:2]
    else:
        randomCategory = None
        recentArticleInCategory = None
        mostViewedArticlesInCategory = []
        mostCommentedArticlesInCategory = []
    
    # NEW LOGIC: For another random category (different from the above), retrieve:
    # (1) The most recent article.
    # (2) Two most viewed articles in the past 7 days (excluding the recent one if exists).
    if randomCategory:
        otherCategory = Category.objects.exclude(id=randomCategory.id).order_by('?').first()
    else:
        otherCategory = Category.objects.order_by('?').first()
    
    if otherCategory:
        otherRecentArticle = Article.objects.filter(status='published', category=otherCategory)\
                                              .order_by('-created_at')\
                                              .first()
        if otherRecentArticle:
            otherMostViewedArticles = list(
                Article.objects.filter(status='published', category=otherCategory, created_at__gte=weekTimeThreshold)
                .exclude(id=otherRecentArticle.id)
                .order_by('-views')
            )
        else:
            otherMostViewedArticles = list(
                Article.objects.filter(status='published', category=otherCategory, created_at__gte=weekTimeThreshold)
                .order_by('-views')
            )
        otherMostViewedArticles = otherMostViewedArticles[:2]
    else:
        otherCategory = None
        otherRecentArticle = None
        otherMostViewedArticles = []
    
    # NEW LOGIC: Retrieve articles with a video_url.
    videoArticleRecent = Article.objects.filter(status='published', video_url__isnull=False)\
                                        .order_by('-created_at')\
                                        .first()
    if videoArticleRecent:
        videoArticleMostViewed = Article.objects.filter(status='published', video_url__isnull=False)\
                                                .exclude(id=videoArticleRecent.id)\
                                                .order_by('-views')[:2]
    else:
        videoArticleMostViewed = Article.objects.filter(status='published', video_url__isnull=False)\
                                                .order_by('-views')[:2]
    
    # NEW LOGIC: Retrieve all authors.
    authors = User.objects.all()
    
    # NEW LOGIC: For 3 random categories, retrieve:
    # - The most recent (featured) article.
    # - Two additional recent articles (excluding the featured one).
    recentArticlesByCategory = []
    randomCategoriesForRecent = Category.objects.order_by('?')[:3]
    for cat in randomCategoriesForRecent:
        featured = Article.objects.filter(status='published', category=cat)\
                                  .order_by('-created_at')\
                                  .first()
        if featured:
            others = Article.objects.filter(status='published', category=cat)\
                                    .exclude(id=featured.id)\
                                    .order_by('-created_at')[:2]
        else:
            others = []
        recentArticlesByCategory.append({
            'category': cat,
            'featuredArticle': featured,
            'otherArticles': others,
        })
    
    # NEW LOGIC: Retrieve all tags in random order.
    tags = Tag.objects.all().order_by('?')
    
    # NEW LOGIC: Retrieve two distinct recent sponsored articles.
    sponsoredArticles = Article.objects.filter(status='published', sponsored=True).order_by('-created_at')
    sponsoredArticleRecent = sponsoredArticles.first()
    sponsoredArticleRecent2 = sponsoredArticles.exclude(id=sponsoredArticleRecent.id).first() if sponsoredArticleRecent else None
    
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
        # Random category block #1
        'randomCategory': randomCategory,
        'recentArticleInCategory': recentArticleInCategory,
        'mostViewedArticlesInCategory': mostViewedArticlesInCategory,
        'mostCommentedArticlesInCategory': mostCommentedArticlesInCategory,
        # Random category block #2 (different from randomCategory)
        'otherCategory': otherCategory,
        'otherRecentArticle': otherRecentArticle,
        'otherMostViewedArticles': otherMostViewedArticles,
        # Video articles block
        'videoArticleRecent': videoArticleRecent,
        'videoArticleMostViewed': videoArticleMostViewed,
        # Authors block
        'authors': authors,
        # Recent articles by category block (3 categories)
        'recentArticlesByCategory': recentArticlesByCategory,
        # Tags block
        'tags': tags,
        # Sponsored articles block
        'sponsoredArticleRecent': sponsoredArticleRecent,
        'sponsoredArticleRecent2': sponsoredArticleRecent2,
    }
    
    return render(request, 'pages/category_articles.html', context)

def showArticle(request, slug):
    """
    Retrieve a published article by its slug along with its associated images and URL fields.
    """
    article = get_object_or_404(Article, slug=slug, status='published')
    
    # Retrieve all associated images for the article.
    images = article.articleimage_set.all()
    
    # Build a dictionary of URL fields.
    urls = {
        'video': article.video_url,
        'sponsored': article.sponsored_link,
    }
    
    context = {
        'article': article,
        'images': images,
        'urls': urls,
    }
    
    return render(request, 'pages/article_detail.html', context)

def showCategoryArticles(request, category_slug):
    """
    Retrieve all published articles for a given category along with sidebar data including:
      - Trending post (most viewed in last 24 hours)
      - Popular posts (most viewed in last 7 days)
      - All tags in random order
      - The second most recent sponsored article for the category.
    """
    category = get_object_or_404(Category, slug=category_slug)
    
    articles = Article.objects.filter(status='published', category=category).order_by('-created_at')
    
    # Define time thresholds.
    timeThreshold = timezone.now() - timedelta(hours=24)
    weekTimeThreshold = timezone.now() - timedelta(days=7)
    
    topArticle = Article.objects.filter(category=category, status='published', created_at__gte=timeThreshold)\
                                .order_by('-views').first()
    
    mostViewedWeeklyArticle = Article.objects.filter(category=category, status='published', created_at__gte=weekTimeThreshold)\
                                             .order_by('-views').first()
    if mostViewedWeeklyArticle:
        mostViewedWeeklyArticles = Article.objects.filter(category=category, status='published', created_at__gte=weekTimeThreshold)\
                                                  .exclude(id=mostViewedWeeklyArticle.id)\
                                                  .order_by('-views')[:3]
    else:
        mostViewedWeeklyArticles = Article.objects.filter(category=category, status='published', created_at__gte=weekTimeThreshold)\
                                                  .order_by('-views')[:3]
    
    tags = Tag.objects.all().order_by('?')
    
    sponsoredArticles = Article.objects.filter(category=category, status='published', sponsored=True)\
                                       .order_by('-created_at')
    sponsoredArticleRecent2 = None
    if sponsoredArticles.exists():
        firstSponsored = sponsoredArticles.first()
        sponsoredArticleRecent2 = sponsoredArticles.exclude(id=firstSponsored.id).first()
    
    context = {
        'category': category,
        'articles': articles,
        'topArticle': topArticle,
        'mostViewedWeeklyArticle': mostViewedWeeklyArticle,
        'mostViewedWeeklyArticles': mostViewedWeeklyArticles,
        'tags': tags,
        'sponsoredArticleRecent2': sponsoredArticleRecent2,
    }
    
    return render(request, 'pages/category_articles.html', context)