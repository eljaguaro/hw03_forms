from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Group(models.Model):
    title = models.CharField(
        "Название группы", max_length=200,
        help_text='Максимум 100 символов')
    slug = models.SlugField(
        "Краткое название группы",
        max_length=200, unique=True, help_text='Максимум 200 символов'
    )
    description = models.TextField("Описание",
                                   blank=True,
                                   null=True,
                                   help_text='Максимум 300 символов')

    def __str__(self):
        return self.title


class Post(models.Model):
    text = models.TextField(verbose_name="текст",
                            help_text='Основной текст поста', null=True)
    pub_date = models.DateTimeField(verbose_name="Дата публикации",
                                    help_text='Дата публикации поста',
                                    null=True, auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               verbose_name="Автор",
                               help_text='Имя автора поста',
                               related_name='posts', null=True)
    group = models.ForeignKey(Group, on_delete=models.SET_NULL,
                              verbose_name="группа",
                              help_text='Название группы поста',
                              related_name='posts',
                              blank=True, null=True)

    def __str__(self):
        return self.text[:30]

    class Meta:
        ordering = ['-pub_date']
