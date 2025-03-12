import random
from base.models import *
from datetime import timedelta
from django.utils import timezone
from django.db.models import Count
from django.contrib.auth import get_user_model
from django.shortcuts import render, get_object_or_404

def home(request):
    User = get_user_model()
    
    breakingNews = Article.objects.all().order_by('-id')[:4]
    
    # Define the time thresholds
    timeThreshold = timezone.now() - timedelta(hours=24)
    weekTimeThreshold = timezone.now() - timedelta(days=7)
    
    # Retrieve the article with the most views in the last 24 hours
    topArticle = Article.objects.filter(created_at__gte=timeThreshold, status='published').order_by('-views').first()
    
    # Retrieve 3 trending articles from the last 24 hours, excluding the topArticle to avoid duplication
    if topArticle:
        trendingArticles = Article.objects.filter(created_at__gte=timeThreshold, status='published')\
                                          .exclude(id=topArticle.id)\
                                          .order_by('-views')[:3]
    else:
        trendingArticles = Article.objects.filter(created_at__gte=timeThreshold, status='published')\
                                          .order_by('-views')[:3]
    
    # Retrieve 2 articles in random order
    randomArticles = Article.objects.filter(status='published').order_by('?')[:2]
    
    # Retrieve all categories
    categories = Category.objects.all()
    
    # Retrieve the recent article from the last 24 hours (most recent creation date)
    recentArticle = Article.objects.filter(created_at__gte=timeThreshold, status='published')\
                                   .order_by('-created_at')\
                                   .first()
    
    # Retrieve 6 articles, one from each category (for 6 randomly selected categories)
    categoryArticles = []
    categoriesList = list(Category.objects.all())
    random.shuffle(categoriesList)
    for category in categoriesList:
        article = Article.objects.filter(category=category, status='published').order_by('?').first()
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
        advancedArticle = Article.objects.filter(category=mostPopulatedCategory, created_at__gte=timeThreshold, status='published')\
                                           .order_by('-views')\
                                           .first()
    else:
        advancedArticle = None

    # Retrieve 3 related articles to the advancedArticle.
    if advancedArticle:
        relatedArticles = Article.objects.filter(
            category=advancedArticle.category,
            created_at__gte=timeThreshold, status='published'
        ).exclude(id=advancedArticle.id).order_by('-created_at')[:3]
    else:
        relatedArticles = None

    # Retrieve the most liked article in the last 24 hours.
    mostLikedArticle = Article.objects.filter(created_at__gte=timeThreshold, status='published')\
        .annotate(like_count=Count('like'))\
        .order_by('-like_count')\
        .first()
    
    # Retrieve 3 articles with the most comments (ordered by comment count and then by like count)
    mostCommentedArticles = Article.objects.annotate(
        comment_count=Count('comment'),
        like_count=Count('like')
    ).order_by('-comment_count', '-like_count')[:3]
    
    # Retrieve the most viewed article in the last 7 days.
    mostViewedWeeklyArticle = Article.objects.filter(created_at__gte=weekTimeThreshold, status='published')\
                                              .order_by('-views')\
                                              .first()
    
    # Retrieve 3 more most viewed articles in the last 7 days (excluding the one above)
    if mostViewedWeeklyArticle:
        mostViewedWeeklyArticles = Article.objects.filter(created_at__gte=weekTimeThreshold, status='published')\
                                                  .exclude(id=mostViewedWeeklyArticle.id)\
                                                  .order_by('-views')[:3]
    else:
        mostViewedWeeklyArticles = Article.objects.filter(created_at__gte=weekTimeThreshold, status='published')\
                                                  .order_by('-views')[:3]
    
    # NEW LOGIC: For one random category, retrieve:
    # (a) One recent article in that category.
    # (b) Four most viewed articles in that category (excluding the recent article).
    # (c) Two articles with the most comments in that category (excluding the ones already selected).
    randomCategory = Category.objects.order_by('?').first()
    if randomCategory:
        recentArticleInCategory = Article.objects.filter(category=randomCategory, status='published')\
                                                   .order_by('-created_at')\
                                                   .first()
        
        if recentArticleInCategory:
            mostViewedArticlesInCategory = list(
                Article.objects.filter(category=randomCategory, status='published')
                .exclude(id=recentArticleInCategory.id)
                .order_by('-views')
            )
        else:
            mostViewedArticlesInCategory = list(
                Article.objects.filter(category=randomCategory, status='published')
                .order_by('-views')
            )
        mostViewedArticlesInCategory = mostViewedArticlesInCategory[:4]
        
        # Exclude articles selected in (a) and (b) from most commented selection.
        excluded_ids = set()
        if recentArticleInCategory:
            excluded_ids.add(recentArticleInCategory.id)
        for art in mostViewedArticlesInCategory:
            excluded_ids.add(art.id)
        
        mostCommentedArticlesInCategory = list(
            Article.objects.filter(category=randomCategory, status='published')
            .exclude(id__in=excluded_ids)
            .annotate(comment_count=Count('comment'))
            .order_by('-comment_count')
        )[:2]
    else:
        randomCategory = None
        recentArticleInCategory = None
        mostViewedArticlesInCategory = []
        mostCommentedArticlesInCategory = []
    
    # NEW LOGIC: For another random category, which must be different from the above randomCategory,
    # retrieve:
    # (1) The most recent article in that category.
    # (2) Two most viewed articles in that category from the past 7 days (excluding the recent article if exists).
    if randomCategory:
        otherCategory = Category.objects.exclude(id=randomCategory.id).order_by('?').first()
    else:
        otherCategory = Category.objects.order_by('?').first()
    
    if otherCategory:
        otherRecentArticle = Article.objects.filter(category=otherCategory, status='published')\
                                              .order_by('-created_at')\
                                              .first()
        if otherRecentArticle:
            otherMostViewedArticles = list(
                Article.objects.filter(category=otherCategory, created_at__gte=weekTimeThreshold, status='published')
                .exclude(id=otherRecentArticle.id)
                .order_by('-views')
            )
        else:
            otherMostViewedArticles = list(
                Article.objects.filter(category=otherCategory, created_at__gte=weekTimeThreshold, status='published')
                .order_by('-views')
            )
        otherMostViewedArticles = otherMostViewedArticles[:2]
    else:
        otherCategory = None
        otherRecentArticle = None
        otherMostViewedArticles = []
    
    # NEW LOGIC: Retrieve articles that have a video_url.
    # 1. The most recent article with a video_url.
    videoArticleRecent = Article.objects.filter(video_url__isnull=False, status='published')\
                                        .order_by('-created_at')\
                                        .first()
    
    # 2. Two most viewed articles with a video_url (excluding the recent video article if exists).
    if videoArticleRecent:
        videoArticleMostViewed = Article.objects.filter(video_url__isnull=False, status='published')\
                                                .exclude(id=videoArticleRecent.id)\
                                                .order_by('-views')[:2]
    else:
        videoArticleMostViewed = Article.objects.filter(video_url__isnull=False, status='published')\
                                                .order_by('-views')[:2]
    
    # NEW LOGIC: Retrieve all authors from the user model.
    authors = User.objects.filter(is_staff=False)
    
    # NEW LOGIC: For 3 random categories, retrieve:
    # - The most recent (featured) article in that category.
    # - Two additional recent articles in that category (excluding the featured article).
    recentArticlesByCategory = []
    randomCategoriesForRecent = Category.objects.order_by('?')[:3]
    for cat in randomCategoriesForRecent:
        featured = Article.objects.filter(category=cat, status='published').order_by('-created_at').first()
        if featured:
            others = Article.objects.filter(category=cat, status='published').exclude(id=featured.id).order_by('-created_at')[:2]
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
    sponsoredArticles = Article.objects.filter(sponsored=True, status='published').order_by('-created_at')
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
    
    return render(request, 'pages/index.html', context)

def showArticle(request, slug):
    """
    Retrieve a published article by its slug along with its associated image URLs
    and any other URL fields (e.g., video_url, sponsored_link).
    """
    # Retrieve the article or return 404 if not found or not published.
    article = get_object_or_404(Article, slug=slug, status='published')
    
    # Retrieve all associated images for the article.
    images = article.articleimage_set.all()
    
    # Retrieve all categories
    categories = Category.objects.all()
    
    # Build a dictionary of URL fields for easy access in the template.
    # (Assuming article has video_url and sponsored_link fields)
    urls = {
        'video': article.video_url,
        'sponsored': article.sponsored_link,
    }
    
    context = {
        'categories': categories,
        'article': article,
        'images': images,
        'urls': urls,
    }
    
    return render(request, 'pages/article_detail.html', context)

def showCategoryArticles(request, category_slug):
    """
    Retrieve all published articles for a given category (by slug) and also gather additional
    sidebar data including:
      - Trending post: the article with the most views in the last 24 hours.
      - Popular posts: the most viewed article in the last 7 days and three additional popular articles.
      - All tags in random order.
      - The second most recent sponsored article for the category.
    """
    # Retrieve all categories
    categories = Category.objects.all()

    # Retrieve the category; 404 if not found.
    category = get_object_or_404(Category, slug=category_slug)
    
    # Retrieve all published articles for the category, ordered by most recent.
    articles = Article.objects.filter(category=category, status='published').order_by('-created_at')
    
    # Define time thresholds.
    timeThreshold = timezone.now() - timedelta(hours=24)
    weekTimeThreshold = timezone.now() - timedelta(days=7)
    
    # Retrieve the trending post for this category (most viewed in the last 24 hours).
    topArticle = Article.objects.filter(category=category, status='published', created_at__gte=timeThreshold)\
                                .order_by('-views').first()
    
    # Retrieve the most viewed article in the last 7 days for this category.
    mostViewedWeeklyArticle = Article.objects.filter(category=category, status='published', created_at__gte=weekTimeThreshold)\
                                             .order_by('-views').first()
    if mostViewedWeeklyArticle:
        mostViewedWeeklyArticles = Article.objects.filter(category=category, status='published', created_at__gte=weekTimeThreshold)\
                                                  .exclude(id=mostViewedWeeklyArticle.id)\
                                                  .order_by('-views')[:3]
    else:
        mostViewedWeeklyArticles = Article.objects.filter(category=category, status='published', created_at__gte=weekTimeThreshold)\
                                                  .order_by('-views')[:3]
    
    # Retrieve all tags in random order.
    tags = Tag.objects.all().order_by('?')
    
    # Retrieve sponsored articles for the category, then get the second most recent one.
    sponsoredArticles = Article.objects.filter(category=category, status='published', sponsored=True).order_by('-created_at')
    sponsoredArticleRecent2 = None
    if sponsoredArticles.exists():
        firstSponsored = sponsoredArticles.first()
        sponsoredArticleRecent2 = sponsoredArticles.exclude(id=firstSponsored.id).first()
    
    context = {
        'categories': categories,
        'category': category,
        'articles': articles,
        'topArticle': topArticle,
        'mostViewedWeeklyArticle': mostViewedWeeklyArticle,
        'mostViewedWeeklyArticles': mostViewedWeeklyArticles,
        'tags': tags,
        'sponsoredArticleRecent2': sponsoredArticleRecent2,
    }
    
    return render(request, 'pages/category_articles.html', context)

def showTagArticles(request, tag_slug):
    """
    Retrieve all published articles associated with a given tag, identified by its slug.
    Additionally, gather sidebar data including:
      - Trending post: the article with the most views in the last 24 hours with this tag.
      - Popular posts: the most viewed article in the last 7 days and three additional popular articles with this tag.
      - All categories and tags (for sidebar display).
      - The second most recent sponsored article for this tag.
    """
    # Retrieve the tag or return 404 if not found.
    tag = get_object_or_404(Tag, slug=tag_slug)
    
    # Retrieve all published articles that have this tag, ordered by most recent.
    articles = Article.objects.filter(tags=tag, status='published').order_by('-created_at')
    
    # Define time thresholds.
    timeThreshold = timezone.now() - timedelta(hours=24)
    weekTimeThreshold = timezone.now() - timedelta(days=7)
    
    # Retrieve trending post for this tag (most viewed article in the last 24 hours).
    topArticle = Article.objects.filter(tags=tag, status='published', created_at__gte=timeThreshold)\
                                .order_by('-views').first()
    
    # Retrieve the most viewed article in the last 7 days for this tag.
    mostViewedWeeklyArticle = Article.objects.filter(tags=tag, status='published', created_at__gte=weekTimeThreshold)\
                                             .order_by('-views').first()
    if mostViewedWeeklyArticle:
        mostViewedWeeklyArticles = Article.objects.filter(tags=tag, status='published', created_at__gte=weekTimeThreshold)\
                                                  .exclude(id=mostViewedWeeklyArticle.id)\
                                                  .order_by('-views')[:3]
    else:
        mostViewedWeeklyArticles = Article.objects.filter(tags=tag, status='published', created_at__gte=weekTimeThreshold)\
                                                  .order_by('-views')[:3]
    
    # Retrieve all categories (for sidebar).
    categories = Category.objects.all()
    
    # Retrieve all tags in random order.
    all_tags = Tag.objects.all().order_by('?')
    
    # Retrieve sponsored articles for this tag and get the second most recent one.
    sponsoredArticles = Article.objects.filter(tags=tag, status='published', sponsored=True).order_by('-created_at')
    sponsoredArticleRecent2 = None
    if sponsoredArticles.exists():
        firstSponsored = sponsoredArticles.first()
        sponsoredArticleRecent2 = sponsoredArticles.exclude(id=firstSponsored.id).first()
    
    context = {
        'tag': tag,
        'articles': articles,
        'topArticle': topArticle,
        'mostViewedWeeklyArticle': mostViewedWeeklyArticle,
        'mostViewedWeeklyArticles': mostViewedWeeklyArticles,
        'categories': categories,
        'tags': all_tags,
        'sponsoredArticleRecent2': sponsoredArticleRecent2,
    }
    
    return render(request, 'pages/tag_articles.html', context)