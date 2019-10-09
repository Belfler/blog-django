from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.models import User
from taggit.managers import TaggableManager


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status='published')


class Post(models.Model):
    objects = models.Manager()
    published_man = PublishedManager()

    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('published', 'Published'),
    ]
    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250, unique_for_date='published')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts')
    body = models.TextField()
    published = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')
    tags = TaggableManager()

    class Meta:
        ordering = ('-published',)

    def __str__(self):
        return self.title

    def get_absolute_url(self, anchor=''):
        url = reverse('blog:post_detail',
                      args=[self.published.year, self.published.month, self.published.day, self.slug])
        if anchor:
            url += ('#' + anchor)
        return url

    def get_similar_posts(self, n_posts):
        posts_tagged_similarly = Post.published_man.order_by().filter(tags__in=self.tags.all())
        other_posts = Post.published_man.exclude(pk__in=posts_tagged_similarly).order_by()
        union = posts_tagged_similarly.exclude(pk=self.pk).annotate(n_tags=models.Count('tags')).\
            union(other_posts.annotate(n_tags=models.Value(0, models.IntegerField()))).order_by('-n_tags', '-published')
        return union[:n_posts]


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=50)
    email = models.EmailField()
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ('created',)

    def __str__(self):
        return f'Comment by {self.name} on {self.post}'
