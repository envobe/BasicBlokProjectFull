from django.shortcuts import render
from .models import Post, Tag, Category
from .forms import PostForm
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.core.urlresolvers import reverse
from django.http import HttpRequest


def post_list(request):
    """所有已发布文章"""

    postsAll = Post.objects.filter(published_date__isnull=False).order_by('-published_date')
    posts = postsAll
    for post in posts:
        post.detail = post.text[:100] + '【更多】'
    return render(request, 'blog/post_list.html', {'posts' : posts})


def post_draft_list(request):
    postsAll = Post.objects.filter(published_date__isnull=True).order_by('-created_date')
    posts = postsAll
    return render(request, 'blog/post_draft_list.html', {'posts': posts})


def post_detail(request, pk):
    """文章详情"""

    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', {'post': post})


def post_new(request):
    """新建文章"""

    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('blog_post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'blog/post_edit.html', {'form': form, 'is_new': True})


def post_edit(request, pk):
    """编辑文章"""

    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('blog_post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form, 'is_new': False})


def post_remove(request, pk):
    """删除文章"""

    post = get_object_or_404(Post, pk=pk)
    post.delete()
    return redirect('blog_post_list')


def post_publish(request, pk):
    """发布文章"""

    post = get_object_or_404(Post, pk=pk)
    post.publish()
    return redirect('blog_post_detail', pk=pk)
