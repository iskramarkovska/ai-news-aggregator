from django.core.management.base import BaseCommand
from articles.models import Category
from articles.news_fetcher import fetch_news
import os

class Command(BaseCommand):
    help = 'Fetch initial news articles'

    def handle(self, *args, **options):
        # Create categories
        categories = ['Technology', 'Business', 'Sports', 'Entertainment', 'Health', 'Science']
        for cat_name in categories:
            Category.objects.get_or_create(name=cat_name)
            self.stdout.write(f'Category {cat_name} ready')
        
        # Fetch articles
        api_key = os.environ.get('NEWSAPI_KEY')
        if api_key:
            self.stdout.write('Fetching technology articles...')
            count = fetch_news(api_key, category='technology', max_articles=15)
            self.stdout.write(f'Fetched {count} articles')