import requests
from datetime import datetime, timedelta
from .models import Article, Category
from django.utils import timezone
from .nlp_utils import summarize_article, extract_keywords

def fetch_news(api_key, category=None, days_back=3, max_articles=100):
    """
    Fetch articles from NewsAPI and save them to the database.
    Returns the number of new articles saved.
    """

    from_date = (timezone.now() - timedelta(days=days_back)).strftime('%Y-%m-%d')
    base_url = 'https://newsapi.org/v2/everything'

    params = {
        'apiKey': api_key,
        'from': from_date,
        'language': 'en',
        'sortBy': 'publishedAt',
        'pageSize': max_articles
    }
    
    if category:
        params['q'] = category  # q = NewsAPI's parameter name for search queries

    try:
        response = requests.get(base_url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching news: {e}")
        return 0
    
    articles_data = data.get('articles', [])
    saved_count = 0

    print(f"DEBUG: API returned {len(articles_data)} articles")

    for article_data in articles_data:
        if not article_data.get('title') or not article_data.get('url'):
            continue

        if Article.objects.filter(url=article_data['url']).exists():
            print(f"  Skipping duplicate: {article_data.get('title', 'Unknown')[:50]}")
            continue

        article_category = Category.objects.first()  # every article MUST have a category (fk); default category is the first created one
        if category:
            article_category = Category.objects.filter(
                name__icontains=category
            ).first() or article_category

        source_data = article_data.get('source')
        if isinstance(source_data, dict):
            source_name = source_data.get('name', 'Unknown')
        elif source_data:
            source_name = str(source_data)
        else:
            source_name = 'Unknown'

        published_date = article_data.get('publishedAt')
        if published_date == '':
            published_date = None

        try:
            article = Article.objects.create(
                title=article_data.get('title', '')[:200],     # [:200] slices the string to max 200 char
                url=article_data['url'],
                source=source_name[:100],
                author=article_data.get('author', 'Unknown')[:100] if article_data.get('author') else 'Unknown',
                description=article_data.get('description', '') or '',
                content=article_data.get('content', '') or '',
                published_at=published_date,
                image_url=article_data.get('urlToImage', '') or '',
                category=article_category,
            )

            combined_text = ' '.join([
                article_data.get('title', ''),
                article_data.get('description', ''),
                article_data.get('content', '')
            ])

            print(f"Processing NLP for: {article.title[:50]}...")
            article.keywords = extract_keywords(combined_text)
            article.summary = summarize_article(article.content) or ''
            article.save()

            saved_count += 1

        except Exception as e:
            print(f"Error saving article: '{article_data.get('title', 'Unknown')}': {e}")
            continue

    return saved_count

    

    