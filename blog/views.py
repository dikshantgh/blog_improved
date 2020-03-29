from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic import TemplateView, ListView, DetailView, CreateView, FormView
from django.views.generic.edit import FormMixin, UpdateView, DeleteView, ModelFormMixin
from taggit.models import Tag, TaggedItem

from blog.forms import ContactForm, CommentForm
from blog.models import Post, Comment


class HomePageView(TemplateView):
    template_name = 'blog/home.html'


class AboutPageView(TemplateView):
    template_name = 'blog/about.html'


class PostListView(ListView):
    model = Post
    template_name = 'blog/post_list.html'
    """This limits the number of objects per page and adds a paginator and page_obj to the context. 
    To allow your users to navigate between pages, add links to the next and previous page, in your 
    template like this:"""
    paginate_by = 5
    # queryset = Post.objects.all()
    context_object_name = 'post_list'

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            return Post.published.filter(Q(title__icontains=query) | Q(author__username__icontains=query))
        return Post.published.all()


class PostDetailView(FormMixin, DetailView):
    model = Post
    template_name = 'blog/post_detail.html'
    form_class = CommentForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["similar_posts"] = self.object.tags.similar_objects()[:4]
        return context

    def dispatch(self, request, *args, **kwargs):
        self.get_object().get_hits()
        return super().dispatch(request, *args, **kwargs)


class PostCreateView(CreateView):
    model = Post
    template_name = 'blog/post_create.html'
    fields = ('title', 'tags', 'body', 'publish', 'status')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class ContactFormView(FormView):
    form_class = ContactForm
    template_name = 'blog/contact.html'
    success_url = '/'


class PostUpdateView(UpdateView):
    model = Post
    template_name = 'blog/post_update.html'
    fields = ('title', 'tags', 'body', 'publish', 'status')


class PostDeleteView(DeleteView):
    model = Post
    template_name = 'blog/post_delete.html'
    success_url = reverse_lazy('blog:post_list')


class PostByTagListView(ListView):
    model = Post
    template_name = 'blog/post_list_by_tag.html'
    context_object_name = 'post_list'
    paginate_by = 5

    def get_queryset(self):
        query = self.kwargs['tag_slug'] # get_object_or_404(Tag, slug = tag_slug)
        # return queryset.filter(tags__in=[p])
        return get_list_or_404(Post, tags__slug=query)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=None, **kwargs)
        context['tag_name'] = self.kwargs['tag_slug']
        return context
