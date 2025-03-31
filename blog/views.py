from django.shortcuts import render

from .forms import PostForm
from .models import Post


def index(request):
    # Получение всех постов (select * from blog_post)
    posts = Post.objects.all()
    context = {'title': 'Главная страница', 'posts': posts}
    return render(request, template_name='blog/index.html', context=context)

def about(request):
    context = {'title': 'О сайте'}
    return render(request, template_name='blog/about.html', context=context)

def add_post(request):
    post_form = PostForm()
    context = {'form': post_form}
    return render(request, template_name='blog/post_add.html', context=context)