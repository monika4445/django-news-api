from django.urls import path
from main import views 
from django.conf.urls.static import static
from django.conf import settings
from main import statistics_views

urlpatterns = [
    path('news/create', views.NewsListCreate.as_view(), name='news-create'),
    path('news/<int:pk>/', views.NewsByIdList.as_view(), name='news-detail'),
    path('news/', views.NewsListView.as_view(), name='news-list'),
    path('news/tag/<str:tag_name>/', views.NewsByTagList.as_view(), name='news-by-tag'),
    path('news/statistics/', statistics_views.statistics, name='statistics'),
    path('news/<int:pk>/like/', views.like_dislike_news, name='like_news'),


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)