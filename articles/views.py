from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import *
from .trending import get_trending_topics
from .recommendations import get_personalized_recommendations

def homepage(request):
    articles = Article.objects.all()[:20]
    categories = Category.objects.all()

    context = {
        'articles': articles,
        'categories': categories,
    }

    return render(request, 'articles/homepage.html', context)

def article_details(request, article_id):
    article = get_object_or_404(Article, id=article_id)

    context = {
        'article': article,
    }

    return render(request, 'articles/article_details.html', context)

def category_articles(request, category_slug):
    category = get_object_or_404(Category, name=category_slug)
    articles = Article.objects.filter(category=category)[:20]
    categories = Category.objects.all()

    context = {
        'articles': articles,
        'categories': categories,
        'selected_category': category,
    }

    return render(request, 'articles/category_articles.html', context)

def trending_topics(request):
    trending = get_trending_topics(limit=10, days=7)

    context = {
        'trending_topics': trending,
    }

    return render(request, 'articles/trending.html', context)

@login_required
def personalized_feed(request):
    recommendations = get_personalized_recommendations(request.user, limit=20)

    context = {
        'articles': recommendations
    }

    return render(request, 'articles/personalized_feed.html', context)

def search_articles(request):
    query = request.GET.get('q', '')
    articles = []

    if query:
        articles = Article.objects.filter(
            Q(title__icontains=query) |
            Q(content__icontains=query) |
            Q(keywords__icontains=query) |
            Q(summary__icontains=query)
        )[:20]

    context = {
        'articles': articles,
        'query': query,
    }

    return render(request, 'articles/search.html', context)

@login_required
def mark_as_read(request, article_id):
    article = get_object_or_404(Article, id=article_id)

    user_pref, created = UserPreferences.objects.get_or_create(user=request.user)
    user_pref.read_articles.add(article)

    return redirect('article_details', article_id=article.id)