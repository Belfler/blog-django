from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank, TrigramSimilarity
from django.shortcuts import render, get_object_or_404
from django.views.generic import View, ListView, DetailView, FormView
from django.views.generic.detail import SingleObjectMixin
from taggit.models import Tag

from blog.models import Post, Comment
from blog.forms import FeedBackForm, CommentForm, SearchForm
from blog.utils import months


class PostList(ListView):
    """
    View that displays last published posts or posts filtered by tag, date or search.
    """
    context_object_name = 'posts'
    template_name = 'blog/post/list.html'
    paginate_by = 5

    filter_by = None
    filter_date_type = None

    def filter_by_date(self):
        queryset = Post.published_man.filter(published__year=self.kwargs['year'])
        if self.filter_date_type in ('month', 'day'):
            queryset = queryset.filter(published__month=self.kwargs['month'])
        if self.filter_date_type == 'day':
            queryset = queryset.filter(published__day=self.kwargs['day'])
        return queryset

    def filter_by_tag(self):
        tag = get_object_or_404(Tag, slug=self.kwargs['tag_slug'])
        self.kwargs['tag'] = tag
        queryset = Post.published_man.filter(tags__exact=tag)
        return queryset

    def filter_by_search(self):
        if 'query' not in self.request.GET:
            query = ''
            queryset = Post.published_man.none()
        else:
            query = self.request.GET['query']
            search_vector = SearchVector('title', weight='A') + SearchVector('body', weight='B')
            search_query = SearchQuery(query)
            queryset = (Post.published_man.annotate(rank=SearchRank(search_vector, search_query))
                        .filter(rank__gte=0.3).order_by('-rank'))
        self.kwargs['query'] = query
        return queryset

    def get_queryset(self):
        if self.filter_by:
            queryset = getattr(self, 'filter_by_' + self.filter_by)()
        else:
            queryset = Post.published_man.all()
        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        context['filter_by'] = self.filter_by
        if self.filter_by == 'tag':
            context['tag'] = self.kwargs['tag']
        elif self.filter_by == 'search':
            context['query'] = self.kwargs['query']
        elif self.filter_by == 'date':
            context['year'] = self.kwargs.get('year')
            context['month'] = months.get(self.kwargs.get('month'), '')
            context['day'] = self.kwargs.get('day', '')
        return context


class DisplayPost(DetailView):
    """
    View that processes GET requests for displaying Post.
    """
    model = Post
    template_name = 'blog/post/detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = self.get_object()
        context['comments'] = post.comments.filter(active=True)
        context['comment_form'] = CommentForm()
        context['search_form'] = SearchForm()
        context['similar_posts'] = post.get_similar_posts(n_posts=5)
        return context


class CommentPost(SingleObjectMixin, FormView):
    """
    View that processes POST requests for commenting Post.
    """
    model = Post
    form_class = CommentForm

    def get_success_url(self):
        return self.get_object().get_absolute_url(anchor='comments')

    def form_valid(self, form):
        cd = form.cleaned_data
        Comment(post=self.get_object(), name=cd['name'], email=cd['email'], body=cd['body']).save()
        return super().form_valid(form)


class PostDetail(View):
    """
    View that combines DisplayPost and CommentPost for dispatching GET and POST requests.
    """
    def get(self, request, *args, **kwargs):
        view = DisplayPost.as_view()
        return view(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        view = CommentPost.as_view()
        return view(request, *args, **kwargs)


class FeedBack(FormView):
    template_name = 'blog/feedback.html'
    form_class = FeedBackForm
    success_url = '/blog/feedback/'

    def form_valid(self, form):
        form.print_in_console()
        return render(self.request, self.template_name, context={'sent': True})


class Search(FormView):
    form_class = SearchForm
    success_url = '/search/'
