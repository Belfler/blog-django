from django.urls import path
from django.views.generic import RedirectView

from blog.views import *

app_name = 'blog'

urlpatterns = [
    path('', RedirectView.as_view(pattern_name='blog:post_list')),
    path('posts/', PostList.as_view(), name='post_list'),
    path('posts/<int:year>/', PostList.as_view(filter_by='date', filter_date_type='year'), name='post_list_by_year'),
    path('posts/<int:year>/<int:month>/', PostList.as_view(filter_by='date', filter_date_type='month'),
         name='post_list_by_month'),
    path('posts/<int:year>/<int:month>/<int:day>/', PostList.as_view(filter_by='date', filter_date_type='day'),
         name='post_list_by_day'),
    path('posts/<int:year>/<int:month>/<int:day>/<slug:slug>/', PostDetail.as_view(), name='post_detail'),
    path('tags/<slug:tag_slug>/', PostList.as_view(filter_by='tag'), name='post_list_by_tag'),
    path('feedback/', FeedBack.as_view(), name='feedback'),
]
