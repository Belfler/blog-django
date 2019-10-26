from django.contrib.auth import get_user_model
from rest_framework import serializers
from taggit_serializer.serializers import TagListSerializerField, TaggitSerializer

from blog.models import Post, Comment

UserModel = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = ('id', 'username')


class PostDetailSerializer(TaggitSerializer, serializers.ModelSerializer):
    tags = TagListSerializerField()

    class Meta:
        model = Post
        fields = ('id', 'title', 'slug', 'body', 'created', 'published', 'updated', 'status', 'tags')


class PostListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('id', 'title')


class CommentListSerializer(serializers.ModelSerializer):
    author = serializers.CharField(source='name')

    class Meta:
        model = Comment
        fields = ('id', 'author', 'created', 'body')


class CommentDetailSerializer(serializers.ModelSerializer):
    author = serializers.CharField(source='name')

    class Meta:
        model = Comment
        fields = ('id', 'author', 'body', 'created', 'updated')


class CreateCommentSerializer(serializers.ModelSerializer):
    author = serializers.CharField(source='name')
    post = serializers.CharField(read_only=True)

    class Meta:
        model = Comment
        fields = ('id', 'author', 'email', 'body', 'post')
