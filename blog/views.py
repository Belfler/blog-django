from django.shortcuts import render
from django.views.generic import ListView, DetailView, FormView

from blog.models import Post
from blog.forms import FeedBackForm


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


class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post/detail.html'


class FeedBackView(FormView):
    template_name = 'blog/feedback.html'
    form_class = FeedBackForm
    success_url = '/blog/feedback/'

    def form_valid(self, form):
        form.print_in_console()
        return render(self.request, self.template_name, context={'sent': True})
