from base.views import *
from django.conf import settings
from django.urls import path, re_path
from django.conf.urls.static import static

app_name = 'base'

urlpatterns = [
    path('', home, name="home"),
    path('article/<slug:slug>/', showArticle, name='showArticle'),
    path('category/<slug:category_slug>/', showCategoryArticles, name='showCategoryArticles'),
    path('tag/<slug:tag_slug>/', showTagArticles, name='tag_articles'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
