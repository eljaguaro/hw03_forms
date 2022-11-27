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
    text = models.TextField(verbose_name="Основной текст", null=True)
    pub_date = models.DateTimeField(verbose_name="Дата публикации",
                                    null=True, auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               verbose_name="Имя автора",
                               related_name='posts', null=True)
    group = models.ForeignKey(Group, on_delete=models.SET_NULL,
                              verbose_name="Имя группы",
                              related_name='posts',
                              blank=True, null=True)

    def __str__(self):
        return self.text[:30]

    class Meta:
        ordering = ['-pub_date']
