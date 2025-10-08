from django.db import models
from django.contrib.auth.models import User

class Category (models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = 'Categories'
    
class Article (models.Model):
    title = models.CharField(max_length=200)
    url = models.URLField(unique=True)
    source = models.TextField(max_length=100)
    author = models.CharField(max_length=200, blank=True, null=True)
    description = models.TextField(blank=True)
    published_at = models.DateTimeField()
    content = models.TextField(blank=True, null=True)
    summary = models.TextField(blank=True, null=True)
    keywords = models.CharField(max_length=500, blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, blank=True, null=True)
    image_url = models.URLField(blank=True, null=True)
    fetched_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ['-published_at']  # when querying articles, '-' -> in descending order

class UserPreferences(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    favorite_categories = models.ManyToManyField(Category, blank=True)
    read_articles = models.ManyToManyField(Article, blank=True, related_name='readers')

    def __str__(self):
        return f"{self.user.username}'s preferences"

    class Meta:
        verbose_name_plural = 'User Preferences'    

