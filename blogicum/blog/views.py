from django.shortcuts import render, get_object_or_404
from datetime import date

from .models import Post, Category


def index(request):
    template = 'blog/index.html'
    post_list = Post.objects.filter(
        pub_date__date__lt=date.today(),
        is_published=True,
        category__is_published=True
    ).order_by('-id')[:5]
    context = {'post_list': post_list}
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
    context = {'post': post}
    return render(request, template, context)
