import uuid
from django.db import models
from django.contrib.auth import get_user_model
from django.db.models.deletion import CASCADE, RestrictedError
from django.conf import settings
import os
from django.utils.safestring import mark_safe


class Tag(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


def upload_avatar_path(instance, filename):
    proj_avarar_path = 'proj/proj_{0}.jpg'.format(str(instance.id))
    full_path = os.path.join(settings.MEDIA_ROOT, proj_avarar_path)
    # '/'.join(['avatars', str(instance.id) + str(".") + str(ext)])
    # ext = filename.split('.')[-1]
    if os.path.exists(full_path):
        os.remove(full_path)
        # return profile_avarar_name_0
    # else:
    return proj_avarar_path


class Project(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField('タイトル', max_length=120)
    overview = models.TextField('プレビュー')
    tags = models.ManyToManyField(
        Tag, blank=True, related_name='proj_tags')
    created_at = models.DateTimeField('登録日時', auto_now_add=True)
    updated_at = models.DateTimeField('更新日時', auto_now=True)
    img = models.ImageField(blank=True, null=True,
                            upload_to=upload_avatar_path)

    class Meta:
        ordering = ['-created_at', ]

    def __str__(self):
        return f"{self.title}-{self.category}"

    def get_text_markdownx(self):
        return mark_safe(markdownify(self.content))

    def get_preview_content(self):
        return self.overview[:200]
