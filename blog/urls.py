from django.urls import path
from django.views.generic import RedirectView

from blog.views import *

app_name = 'blog'

urlpatterns = [
    path('', RedirectView.as_view(pattern_name='blog:post_list')),
    path('posts/', PostListView.as_view(), name='post_list'),
    path('posts/<int:year>/', PostListView.as_view(filter_by='y')),
    path('posts/<int:year>/<int:month>/', PostListView.as_view(filter_by='ym')),
    path('posts/<int:year>/<int:month>/<int:day>/', PostListView.as_view(filter_by='ymd')),
    path('posts/<int:year>/<int:month>/<int:day>/<slug:slug>/', PostDetailView.as_view(), name='post_detail'),
    path('feedback/', FeedBackView.as_view(), name='feedback'),
]
