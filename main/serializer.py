from rest_framework import serializers
from .models import News, Tag

class NewsSerializer(serializers.ModelSerializer):
    tags = serializers.SerializerMethodField()

    class Meta:
        model = News
        fields = ["id", "title", "content", "image", "tags", "views", "likes", "dislikes"]

    def get_tags(self, obj):
        return list(obj.tags.values_list("name", flat=True))