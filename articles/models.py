import uuid
from django.db import models
from django.contrib.auth import get_user_model
from django.db.models.deletion import CASCADE, RestrictedError
from django.conf import settings
import os
from markdownx.models import MarkdownxField
from django.utils.safestring import mark_safe
from markdownx.utils import markdownify


class Category(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Tag(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


def upload_avatar_path(instance, filename):
    profile_avarar_path = 'post/post_{0}.jpg'.format(str(instance.id))
    full_path = os.path.join(settings.MEDIA_ROOT, profile_avarar_path)
    # '/'.join(['avatars', str(instance.id) + str(".") + str(ext)])
    # ext = filename.split('.')[-1]
    if os.path.exists(full_path):
        os.remove(full_path)
        # return profile_avarar_name_0
    # else:
    return profile_avarar_path


class Post(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField('タイトル', max_length=120)
    content = MarkdownxField('テキスト')
    overview = models.TextField('プレビュー', blank=True, null=True)
    category = models.ForeignKey(
        Category, blank=True, null=True, related_name='category_post', on_delete=CASCADE)
    tags = models.ManyToManyField(
        Tag, blank=True, related_name='post_tags')
    liked = models.ManyToManyField(
        get_user_model(), blank=True, related_name='favorite_post')
    created_at = models.DateTimeField('登録日時', auto_now_add=True)
    updated_at = models.DateTimeField('更新日時', auto_now=True)
    # img = models.ImageField(blank=True, null=True,
    #                         upload_to=upload_avatar_path)

    class Meta:
        ordering = ['-created_at', ]

    def __str__(self):
        return f"{self.title}-{self.category}"

    def get_text_markdownx(self):
        return mark_safe(markdownify(self.content))

    def get_preview_content(self):
        return self.overview[:200]


class Comment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    comment = models.CharField(max_length=200)
    commented_by = models.ForeignKey(
        get_user_model(), related_name='user_comment',
        blank=True, null=True,
        on_delete=models.CASCADE
    )
    commented_at = models.DateTimeField('登録日時', auto_now_add=True)
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name='comment')
    created_at = models.DateTimeField('登録日時', auto_now_add=True)

    class Meta:
        ordering = ['-commented_at', ]

    def __str__(self):
        return self.comment
