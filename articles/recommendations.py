from django.db.models import Q, Count
from .models import Article, UserPreferences
from collections import Counter

def get_personalized_recommendations(user, limit=10):
    """
    Get personalized article recommendations for a user based on:
    - Their favorite categories
    - Keywords from articles they've read
    - Excluding articles they've already read
    Returns a QuerySet of recommended articles.
    """
    try:
        preferences = UserPreferences.objects.get(user=user)
    except UserPreferences.DoesNotExist:
        preferences = UserPreferences.objects.create(user=user)

    favorite_categories = preferences.favorite_categories.all()
    read_articles = preferences.read_articles.all()
    read_articles_ids = list(read_articles.values_list('id', flat=True))

    user_keywords = []
    for article in read_articles:
        if article.keywords:
            keywords = [k.strip().lower() for k in article.keywords.split(',')]
            user_keywords.extend(keywords)

    if user_keywords:
        keyword_counts = Counter(user_keywords)
        top_keywords = [kw for kw, count in keyword_counts.most_common(5)]
    else:
        top_keywords = []

    recommendations = Article.objects.exclude(id__in=read_articles_ids)
    if favorite_categories.exists():
        recommendations = recommendations.filter(category__in=favorite_categories)

    if top_keywords:
        # Builds OR query: article contains kw1 OR kw2 OR kw3...
        keyword_query = Q()

        for keyword in top_keywords:
            keyword_query |= Q(keywords__icontains=keyword)

        keyword_filtered = recommendations.filter(keyword_query)
        if keyword_filtered.exists():
            recommendations = keyword_filtered
            
    recommendations = recommendations.order_by('-published_at')[:limit]
    return recommendations
    