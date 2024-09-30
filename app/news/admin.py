from django.contrib import admin
from .models import News, NewsCategory, NewsCreator


admin.site.register(News)
admin.site.register(NewsCategory)
admin.site.register(NewsCreator)
