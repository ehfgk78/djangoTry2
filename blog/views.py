from django.shortcuts import render

# Create your views here.
from django.utils import timezone

from blog.models import Post


def post_list(request):
    # posts = Post.objects.all()
    # published 만 게시
    posts = Post.objects.filter(published_date__isnull=False).filter(published_date__lte=timezone.now())
    data = {
        "post_list": posts,
    }
    # return HttpResponse("Post List")
    return render(request, 'post_list.html', context=data)


def post_detail(request, detail_pk):
    # post = Post.objects.filter(pk=detail_pk)[0]
    post = Post.objects.get(pk=detail_pk)
    data = {
        'post': post
    }
    return render(request, 'post_detail.html', context=data)
