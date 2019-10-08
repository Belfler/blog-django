from django.shortcuts import render, reverse
from django.views.generic import View, ListView, DetailView, FormView
from django.views.generic.detail import SingleObjectMixin
from django.views.generic.edit import ModelFormMixin

from blog.models import Post, Comment
from blog.forms import FeedBackForm, CommentForm


class PostListView(ListView):
    context_object_name = 'posts'
    template_name = 'blog/post/list.html'
    paginate_by = 2

    filter_by = None

    def get_queryset(self):
        queryset = Post.published_man.all()
        if self.filter_by is not None:
            queryset = queryset.filter(published__year=self.kwargs['year'])
            if 'm' in self.filter_by:
                queryset = queryset.filter(published__month=self.kwargs['month'])
            if 'd' in self.filter_by:
                queryset = queryset.filter(published__day=self.kwargs['day'])
        return queryset


class DisplayPost(DetailView):
    """
    View that processes GET requests for displaying Post.
    """
    model = Post
    template_name = 'blog/post/detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = self.get_object().comments.filter(active=True)
        context['form'] = CommentForm()
        return context


class CommentPost(SingleObjectMixin, FormView):
    """
    View that processes POST requests for commenting Post.
    """
    model = Post
    form_class = CommentForm

    def get_success_url(self):
        return self.get_object().get_absolute_url(anchor_id='comments')

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


class FeedBackView(FormView):
    template_name = 'blog/feedback.html'
    form_class = FeedBackForm
    success_url = '/blog/feedback/'

    def form_valid(self, form):
        form.print_in_console()
        return render(self.request, self.template_name, context={'sent': True})
