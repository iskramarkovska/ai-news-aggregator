from django.core.management.base import BaseCommand
from articles.models import Category, Article
from articles.news_fetcher import fetch_news
import os

class Command(BaseCommand):
    help = 'Populate initial categories and fetch news articles'

    def handle(self, *args, **options):
        self.stdout.write('Creating categories...')
        
        # Create categories
        categories = ['Technology', 'Business', 'Sports', 'Entertainment', 'Health', 'Science']
        for cat_name in categories:
            category, created = Category.objects.get_or_create(name=cat_name)
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created category: {cat_name}'))
            else:
                self.stdout.write(f'Category already exists: {cat_name}')
        
        # Check if we already have articles
        article_count = Article.objects.count()
        if article_count > 0:
            self.stdout.write(self.style.SUCCESS(f'Articles already exist ({article_count} total). Skipping fetch.'))
            return
        
        # Fetch articles
        api_key = os.environ.get('NEWSAPI_KEY')
        if not api_key:
            self.stdout.write(self.style.ERROR('NEWSAPI_KEY not found in environment'))
            return
        
        self.stdout.write('Fetching technology articles...')
        try:
            count = fetch_news(api_key, category='technology', max_articles=15)
            self.stdout.write(self.style.SUCCESS(f'✓ Fetched {count} technology articles'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error fetching technology: {e}'))
        
        self.stdout.write('Fetching business articles...')
        try:
            count = fetch_news(api_key, category='business', max_articles=10)
            self.stdout.write(self.style.SUCCESS(f'✓ Fetched {count} business articles'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error fetching business: {e}'))
        
        self.stdout.write('Fetching sports articles...')
        try:
            count = fetch_news(api_key, category='sports', max_articles=10)
            self.stdout.write(self.style.SUCCESS(f'✓ Fetched {count} sports articles'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error fetching sports: {e}'))
        
        total_articles = Article.objects.count()
        self.stdout.write(self.style.SUCCESS(f'\n🎉 Done! Total articles: {total_articles}'))