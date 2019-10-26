from rest_framework import generics
from rest_framework.permissions import IsAdminUser, IsAuthenticated, IsAuthenticatedOrReadOnly, SAFE_METHODS

from blog.models import Post, Comment
from blog.api.serializers import (PostDetailSerializer, PostListSerializer,
                                  CommentDetailSerializer, CommentListSerializer, CreateCommentSerializer)
from blog.api.permissions import IsAdminOrReadOnly


class PostList(generics.ListCreateAPIView):
    permission_classes = (IsAdminOrReadOnly,)

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return PostDetailSerializer
        else:
            return PostListSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_queryset(self):
        if self.request.user.is_staff:
            return Post.objects.all()
        else:
            return Post.published_man.all()


class PostDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = PostDetailSerializer
    permission_classes = (IsAdminOrReadOnly,)

    def get_queryset(self):
        if self.request.user.is_staff:
            return Post.objects.all()
        else:
            return Post.published_man.all()


class CommentList(generics.ListCreateAPIView):
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CreateCommentSerializer
        else:
            return CommentListSerializer

    def perform_create(self, serializer):
        if self.request.user.is_staff:
            post_manager = Post.objects.all()
        else:
            post_manager = Post.published_man.all()
        serializer.save(post=post_manager.get(pk=self.kwargs['post_pk']))

    def get_queryset(self):
        if self.request.user.is_staff:
            return Comment.objects.all()
        else:
            return Comment.active_comments.all()


class CommentDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAdminOrReadOnly,)
    serializer_class = CommentDetailSerializer

    def get_queryset(self):
        if self.request.user.is_staff:
            return Post.objects.get(pk=self.kwargs['post_pk']).comments.all()
        else:
            return Post.published_man.get(pk=self.kwargs['post_pk']).comments.filter(active=True)
