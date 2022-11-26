from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Group(models.Model):
    title = models.CharField("Title of the group", max_length=200)
    slug = models.SlugField(
        "Slug-name of the group", max_length=200, unique=True
    )
    description = models.TextField("Description", blank=True, null=True)

    def __str__(self):
        return self.title


class Post(models.Model):
    text = models.TextField("The main text", null=True)
    pub_date = models.DateTimeField("Publication date",
                                    null=True, auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               verbose_name="Author's name",
                               related_name='posts', null=True)
    group = models.ForeignKey(Group, on_delete=models.SET_NULL,
                              verbose_name="Name of the group",
                              related_name='posts',
                              blank=True, null=True)

    def __str__(self):
        return self.text

    class Meta:
        ordering = ['-pub_date']
