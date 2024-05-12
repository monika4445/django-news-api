from django.contrib import admin
from .models import News, Tag
from .forms import NewsForm

class NewsAdmin(admin.ModelAdmin):
    form = NewsForm

admin.site.register(News, NewsAdmin)
admin.site.register(Tag)
