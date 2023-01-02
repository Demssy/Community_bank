from rest_framework import serializers
from comment.models import Comment
from comment.api.serializers import CommentSerializer
from .models import Blog


class BlogSerializer(serializers.ModelSerializer):

    comments = serializers.SerializerMethodField()

    class Meta:
        model = Blog
        fields = (
            'title', 'description', 'date', 'user', 'comments')

    def get_comments(self, obj):
        comments_qs = Comment.objects.filter_parents_by_object(obj)
        return CommentSerializer(comments_qs, many=True).data