from django.urls import path
from . import views

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('article/<int:article_id>/', views.article_details, name='article_details'),
    path('category/<slug:category_slug>/', views.category_articles, name='category_articles'),
    path('trending/', views.trending_topics, name='trending_topics'),
    path('for-you/', views.personalized_feed, name='personalized_feed'),
    path('search/', views.search_articles, name='search'),
    path('article/<int:article_id>/mark_read', views.mark_as_read, name='mark_as_read'),
]