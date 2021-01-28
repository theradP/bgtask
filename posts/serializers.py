from rest_framework import serializers
from .models import Post, Comment


class PostSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = ('id', 'content', 'image', 'created', 'updated')


class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = ('id', 'post', 'body')