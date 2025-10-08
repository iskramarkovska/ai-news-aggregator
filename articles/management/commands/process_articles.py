from django.core.management.base import BaseCommand
from articles.models import Article
from articles.nlp_utils import summarize_article, extract_keywords

class Command(BaseCommand):
    help_text = 'Process articles with NLP: generate summaries and extract keywords.'

    def handle(self, *args, **options):
        """
        Main command logic - process all articles withour summaries.
        """

        articles = Article.objects.filter(summary__isnull=True) | Article.objects.filter(summary='')
        total = articles.count()
        self.stdout.write(f"Found {total} articles to process...")

        if total == 0:
            self.stdout.write(self.style.WARNING('No articles need processing.'))
            return
        
        processed = 0
        failed = 0

        for i, article in enumerate(articles, start=1):
            self.stdout.write(f"Processing {i}/{total}: {article.title[:50]}...")
            
            if article.summary and len(article.summary ):
                keywords = extract_keywords(article.summary)
            else:
                combined_text = f"{article.title} {article.content}"
                keywords = extract_keywords(combined_text)
            
            summary = summarize_article(article.content)

            if keywords or summary:
                article.keywords = keywords
                article.summary = summary or ''
                article.save()
                processed += 1
                self.stdout.write(f"Processed successfully!")

            else:
                failed += 1
                self.stdout.write(f"Failed to process!")

        self.stdout.write('')
        self.stdout.write(self.style.SUCCESS(f"Finished! Processed {processed}/{total} articles."))

        if failed > 0:
            self.stdout.write(self.style.WARNING(f"Failed to process {failed}/{total} articles."))

        
