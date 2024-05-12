from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.db.models import Sum, Avg
from .models import News

@login_required
def statistics(request):
    if not request.user.is_superuser:
        # If the user is not a superuser, redirect them to a page indicating they do not have permission
        return render(request, 'permission_denied.html')

    # Overall statistics
    total_views = News.objects.aggregate(total_views=Sum('views'))['total_views']
    average_views_per_article = News.objects.aggregate(average_views=Avg('views'))['average_views']
    most_viewed_articles = News.objects.order_by('-views')[:5]
    least_viewed_articles = News.objects.order_by('views')[:5]
    articles_views = {article.title: article.views for article in News.objects.all()}

    context = {
        'total_views': total_views,
        'average_views_per_article': average_views_per_article,
        'most_viewed_articles': most_viewed_articles,
        'least_viewed_articles': least_viewed_articles,
        'articles_views': articles_views,
    }
    return render(request, 'statistics.html', context)
