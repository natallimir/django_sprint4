from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from datetime import date
from django.core.paginator import Paginator
from django.views.generic import (
    CreateView, UpdateView, DeleteView, DetailView
)
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest
from django.urls import reverse

from .models import Post, Category, Comment
from .forms import PostForm, CommentForm


User = get_user_model()


def index(request):
    template = 'blog/index.html'
    post_list = Post.objects.filter(
        pub_date__date__lt=date.today(),
        is_published=True,
        category__is_published=True
    ).order_by('-id')
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'post_list': post_list,
        'page_obj': page_obj
    }
    return render(request, template, context)


def category_posts(request, category_slug):
    template = 'blog/category.html'
    category = get_object_or_404(
        Category.objects.filter(
            slug=category_slug,
            is_published=True
        )
    )
    post_list = Post.objects.filter(
        pub_date__date__lt=date.today(),
        category__slug=category_slug,
        is_published=True,
    ).order_by('-id')
    context = {
        'category': category,
        'post_list': post_list
    }
    return render(request, template, context)


def post_detail(request, id):
    template = 'blog/detail.html'
    post = get_object_or_404(
        Post.objects.filter(
            pub_date__date__lt=date.today(),
            is_published=True,
            category__is_published=True
        ),
        pk=id
    )
    context = {
        'post': post,
        'form': CommentForm
    }
    return render(request, template, context)


class PostCreateView(CreateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/create.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(UpdateView):
    model = Post
    form_class = PostForm


class PostDeleteView(DeleteView):
    model = Post
    success_url = reverse_lazy('birthday:list')


class ProfileDetailView(DetailView):
    model = User
    template_name = 'blog/profile.html'
    slug_field = 'username'
    slug_url_kwarg = 'username'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class CommentCreateView(LoginRequiredMixin, CreateView):
    post = None
    model = Comment
    form_class = CommentForm

    def dispatch(self, request: HttpRequest, *args, **kwargs):
        self.post = get_object_or_404(Post, pk=kwargs['pk'])
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.post = self.post
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('blog:posts', kwargs={'pk': self.post.pk})
