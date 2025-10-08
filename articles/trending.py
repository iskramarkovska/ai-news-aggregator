from collections import Counter
from .models import Article

def get_trending_topics(limit=10, days=7):
    """
    Analyze all articles and return the most frequently mentioned keywords.
    Returns a list of tuples: [(keyword, count), ...]
    """
    from django.utils import timezone
    from datetime import timedelta

    cutoff_date = timezone.now() - timedelta(days=days)

    articles = Article.objects.filter(
        fetched_at__gte=cutoff_date,
        keywords__isnull=False
    ).exclude(keywords='')

    if not articles.exists():
        return []
    
    all_keywords = []
    for article in articles:
        if not article.keywords or article.keywords.strip() == '':
            continue

        keywords = article.keywords.split(',')
        keywords = [k.strip().lower() for k in keywords if k.strip()]
        all_keywords.extend(keywords)

    keyword_counts = Counter(all_keywords)
    trending = keyword_counts.most_common(limit)

    return trending
