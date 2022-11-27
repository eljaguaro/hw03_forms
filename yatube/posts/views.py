from django.shortcuts import render, get_object_or_404
from .models import Post, Group
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from .forms import PostForm
from django.shortcuts import redirect
from .models import User


ten_slice = 10
# Главная страница
# @login_required
def index(request):
    post_list = Post.objects.select_related('author').all()
    paginator = Paginator(post_list, ten_slice)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj,
    }
    template = 'posts/index.html'
    return render(request, template, context)


# Страница со сгруппированными постами
def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    post_list = group.posts.all()
    paginator = Paginator(post_list, ten_slice)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'group': group,
        'page_obj': page_obj
    }
    template = 'posts/group_list.html'
    return render(request, template, context)


def profile(request, username):
    author = User.objects.filter(username=username)[0]
    posts = Post.objects.select_related('author').filter(author=author)
    num_of_posts = len(posts)
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'author': author,
        'postsnum': num_of_posts,
        # 'username' : username,
        'page_obj': page_obj
    }
    return render(request, 'posts/profile.html', context)


@login_required
def post_create(request):
    groups = Group.objects.all()
    # Проверяем, получен POST-запрос или какой-то другой:
    if request.method == 'POST':
        # Создаём объект формы класса ContactForm
        # и передаём в него полученные данные
        form = PostForm(request.POST)

        # Если все данные формы валидны - работаем с "очищенными данными" формы
        if form.is_valid():
            # Берём валидированные данные формы из словаря form.cleaned_data
            new_post = form.save(commit=False)
            new_post.author = request.user
            # new_post.group = group
            # При необходимости обрабатываем данные
            # ...
            # сохраняем объект в базу
            form.save()

            # Функция redirect перенаправляет пользователя
            # на другую страницу сайта, чтобы защититься
            # от повторного заполнения формы
            return redirect(f'/profile/{request.user.username}/')

        # Если условие if form.is_valid() ложно и данные не прошли валидацию -
        # передадим полученный объект в шаблон,
        # чтобы показать пользователю информацию об ошибке

        # Заодно заполним все поля формы данными, прошедшими валидацию,
        # чтобы не заставлять пользователя вносить их повторно
        return render(request, 'posts/create_post.html', {'form': form})

    # Если пришёл не POST-запрос - создаём и передаём в шаблон пустую форму
    # пусть пользователь напишет что-нибудь
    form = PostForm()
    return render(request, 'posts/create_post.html',
                  {'form': form, 'groups': groups})


def post_detail(request, post_id):
    # Здесь код запроса к модели и создание словаря контекста
    post = Post.objects.select_related('author').filter(pk=post_id)[0]
    author = post.author.username
    num_of_posts = len(Post.objects.filter(author=post.author))
    title = post.text[:30]
    if request.user.username == author:
        is_author = True
    else:
        is_author = False
    context = {
        'post': post,
        'postsnum': num_of_posts,
        'title': title,
        'author': author,
        'is_author': is_author
    }
    return render(request, 'posts/post_detail.html', context)

@login_required
def post_edit(request, post_id):
    is_edit = True
    groups = Group.objects.all()
    post = Post.objects.select_related('author').filter(pk=post_id)[0]
    # Проверяем, получен POST-запрос или какой-то другой:
    if post.author != request.user:
        return redirect(f'/posts/{post_id}/')
    if request.method == 'POST':
        # Создаём объект формы класса ContactForm
        # и передаём в него полученные данные
        form = PostForm(request.POST)
        # Если все данные формы валидны - работаем с "очищенными данными" формы
        if form.is_valid():
            # Берём валидированные данные формы из словаря form.cleaned_data
            post.save()
            # post.text = form.cleaned_data['text']
            # post.group = form.cleaned_data['group']
            return redirect(f'/posts/{post_id}/')
        # Post.objects.filter(pk=post_id)[0].text = text
        return render(request, 'posts/create_post.html',
                      {'form': form, 'groups': groups,
                       'id': post_id, 'post': post, 'is_edit': is_edit})

    # Если пришёл не POST-запрос - создаём и передаём в шаблон пустую форму
    # пусть пользователь напишет что-нибудь
    form = PostForm()
    return render(request, 'posts/create_post.html',
                  {'form': form, 'groups': groups,
                   'id': post_id, 'post': post, 'is_edit': is_edit})
