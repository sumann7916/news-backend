from django.db import models


class NewsCreator(models.Model):
    name = models.CharField(max_length=100)
    url = models.CharField(max_length=100, unique=True)  # Ensuring uniqueness

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class NewsCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)  # Ensuring uniqueness

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class News(models.Model):
    title = models.CharField(max_length=100)
    summary = models.TextField()
    original_link = models.URLField(max_length=200)

    creator = models.ForeignKey(NewsCreator, on_delete=models.CASCADE)
    categories = models.ManyToManyField(NewsCategory, related_name="news")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
