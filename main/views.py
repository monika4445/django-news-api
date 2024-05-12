from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.views import View
from .models import News, Tag
import logging
from .serializer import NewsSerializer
from django.shortcuts import render


class NewsListCreate(generics.ListCreateAPIView):
    queryset = News.objects.all()
    serializer_class = NewsSerializer

    def perform_create(self, serializer):
        news_instance = serializer.save()

        # Handle tags creation or retrieval
        tags_data = self.request.data.get('tags', [])
        for tag_name in tags_data:
            tag, _ = Tag.objects.get_or_create(name=tag_name)
            news_instance.tags.add(tag)

    def post(self, request, *args, **kwargs):
        user = request.user
        if not user.is_superuser:
            return Response({"error": "Only superusers or admins can create news articles."}, status=status.HTTP_403_FORBIDDEN)

        data = request.data.copy()  
        data['tags'] = request.data.get('tags', [])  # Ensure 'tags' is an empty list if not provided
        serializer = self.get_serializer(data=data)
        if serializer.is_valid():
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class NewsListView(generics.ListAPIView):
    queryset = News.objects.all()
    serializer_class = NewsSerializer
    
    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)

        context = {
            'news_list': serializer.data,
        }
        # Render the news.html template with the news queryset and additional context
        return render(request, 'news.html', context)

    
logger = logging.getLogger(__name__)

class NewsByIdList(View):
    def get(self, request, pk):
        try:
            news = News.objects.get(pk=pk)
            # Increment the views field
            news.views += 1
            news.save()
            # Additional context data
            context = {
                'id': pk,
                'news': news,
                'title': news.title,
                'img_url': news.image.url  
            }
            return render(request, 'news_card.html', context)
        except News.DoesNotExist as e:
            logger.error(f"News with id {pk} does not exist: {e}")
            # Render the error template without exposing the error message
            return render(request, 'error.html', status=404)
        
    
class NewsByTagList(generics.ListAPIView):
    serializer_class = NewsSerializer

    def get_queryset(self):
        tag_name = self.kwargs['tag_name']
        tag = get_object_or_404(Tag, name=tag_name)
        return News.objects.filter(tags=tag)
