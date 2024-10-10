from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from django.http import Http404
from .models import Post, Category


def index(request):
    current_time = timezone.now()
    post_list = Post.objects.filter(
        pub_date__lte=current_time,
        is_published=True,
        category__is_published=True
    ).order_by('-pub_date')[:5]
    return render(request, 'blog/index.html', {'post_list': post_list})


def post_detail(request, id):
    post = get_object_or_404(Post, pk=id)
    if any([
        post.pub_date > timezone.now(),
        not post.is_published,
        not post.category.is_published
    ]):
        raise Http404("Эта публикация недоступна.")

    return render(request, 'blog/detail.html', {'post': post})


def category_posts(request, category_slug):
    category = get_object_or_404(Category, slug=category_slug)
    if not category.is_published:
        raise Http404("Эта категория недоступна.")

    current_time = timezone.now()
    post_list = Post.objects.filter(
        category=category,
        is_published=True,
        pub_date__lte=current_time
    ).order_by('-pub_date')

    return render(request, 'blog/category.html', {
        'category': category,
        'post_list': post_list,
    })
