from django.shortcuts import get_object_or_404, render
from django.utils.timezone import now

from .models import Category, Post
from .constants import POSTS_PER_PAGE


def get_filtered_posts(manager):
    return manager.filter(
        pub_date__lte=now(),
        is_published=True,
        category__is_published=True
    ).select_related('author', 'location', 'category')


def index(request):
    post_list = get_filtered_posts(Post.objects)[:POSTS_PER_PAGE]
    return render(request, 'blog/index.html', {'post_list': post_list})


def post_detail(request, post_id):
    post = get_object_or_404(get_filtered_posts(Post.objects), pk=post_id)
    return render(request, 'blog/detail.html', {'post': post})


def category_posts(request, category_slug):
    category = get_object_or_404(
        Category, slug=category_slug,
        is_published=True)
    post_list = get_filtered_posts(category.posts.all())
    return render(request, 'blog/category.html', {
        'category': category,
        'post_list': post_list,
    })
