from django.urls import path

from blog.api import views

app_name = 'api'

urlpatterns = [
    path('posts/', views.PostList.as_view(), name='post_list'),
    path('posts/<int:pk>/', views.PostDetail.as_view(), name='post_detail'),
    path('posts/<int:post_pk>/comments/', views.CommentList.as_view(), name='comment_list'),
    path('posts/<int:post_pk>/comments/<int:pk>/', views.CommentDetail.as_view(), name='comment_detail'),
]
