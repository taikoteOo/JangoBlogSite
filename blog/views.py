from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from .forms import PostForm
from .models import Post


def index(request):
    # Получение всех постов, отсортированных по дате публикации (select * from blog_post order by created_at DESC)
    posts = Post.objects.all().order_by('-created_at')
    count_posts = Post.objects.count()
    # Показываем по 3 поста на странице
    per_page = 3
    paginator = Paginator(posts, per_page)
    #Получаем номер страницы из url
    page_number = request.GET.get('page')
    # Получаем объекты для текущей страницы
    page_obj = paginator.get_page(page_number)
    context = {
        'title': 'Главная страница',
        'page_obj': page_obj,
        'count_posts': count_posts,
        'post_text': 'Последние посты'
    }
    return render(request, template_name='blog/index.html', context=context)

def about(request):
    count_posts = Post.objects.count()
    context = {'title': 'О сайте', 'count_posts': count_posts}
    return render(request, template_name='blog/about.html', context=context)

@login_required
def add_post(request):
    if request.method == 'GET':
        post_form = PostForm(author=request.user)
        context = {'form': post_form, 'title': 'Добавить пост'}
        return render(request, template_name='blog/post_add.html', context=context)
    if request.method == 'POST':
        post_form = PostForm(data = request.POST, files=request.FILES, author=request.user)
        if post_form.is_valid():
            # post = Post()
            # post.title = post_form.cleaned_data['title']
            # post.text = post_form.cleaned_data['text']
            # post.author = post_form.cleaned_data['author'] # request.user
            # post.image = post_form.cleaned_data['image']
            post_form.save()
            return index(request)

def read_post(request, slug):
    # post = Post.objects.get(pk=pk)
    post = get_object_or_404(Post, slug=slug)
    context = {'post': post, 'title': post.title}
    return render(request, template_name='blog/post_detail.html', context=context)

@login_required
def update_post(request, slug):
    post = get_object_or_404(Post, slug=slug)
    if request.method == 'POST':
        post_form = PostForm(data = request.POST, files=request.FILES, author=request.user)
        if post_form.is_valid():
            post.title = post_form.cleaned_data['title']
            post.text = post_form.cleaned_data['text']
            post.author = post_form.cleaned_data['author']  # request.user
            post.image = post_form.cleaned_data['image']
            post.save()
            return read_post(request, post.slug)
    else:
        post_form = PostForm(initial={
            'title': post.title,

            'text': post.text,
            'image': post.image,
        }, author=request.user)
        return render(request, template_name='blog/post_edit.html', context={'form': post_form})

@login_required
def delete_post(request, pk):
    # post = Post.objects.get(pk=pk)
    post = get_object_or_404(Post, pk=pk)
    context = {'post':post}
    if request.method == 'POST':
        post.delete()
        return redirect('blog:index')
    return render(request, template_name='blog/post_delete.html', context=context)

def user_posts(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    # posts = user.posts.all()
    posts = Post.objects.filter(author=user).select_related('author')
    context = {'user': user, 'posts': posts}
    return render(request, template_name='blog/user_posts.html', context=context)

@login_required
def user_info(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    context = {'user': user}
    return render(request, template_name='blog/user_info.html', context=context)

def page_not_found(request, exception):
    return render(request, template_name='blog/404.html', context={'title':'404'})

def forbidden(request, exception):
    return render(request, template_name='blog/403.html', context={'title':'403'})

def server_error(request):
    return render(request, template_name='blog/500.html', context={'title':'500'})

def search_post(request):
    query = request.GET.get('query')
    query_text = Q(title__icontains=query) | Q(text__icontains=query)
    results = Post.objects.filter(query_text)
    per_page = 3
    paginator = Paginator(results, per_page)
    # Получаем номер страницы из url
    page_number = request.GET.get('page')
    # Получаем объекты для текущей страницы
    page_obj = paginator.get_page(page_number)
    count_posts = results.count()
    context = {
        'title': 'Главная страница',
        'page_obj': page_obj,
        'count_posts': count_posts,
        'post_text': 'Результаты поиска'
    }
    return render(request, template_name='blog/index.html', context=context)