from django import template
from django.utils.safestring import mark_safe
from markdown import markdown

from blog.models import Post, Comment
from blog.forms import SearchForm

register = template.Library()


@register.simple_tag
def total_posts():
    return Post.published_man.count()


@register.inclusion_tag('blog/latest_comments.html')
def show_latest_comments(n_comments=5):
    latest_comments = Comment.objects.order_by('-created')[:n_comments]
    return {'latest_comments': latest_comments}


@register.filter(name='markdown')
def markdown_format(text):
    return mark_safe(markdown(text))


@register.simple_tag
def search_form():
    return SearchForm()
