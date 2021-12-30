from django.db import models
import os
from account.models import Profile

class Tag(models.Model):
    slug = models.CharField(    # slug: 半角文字
        primary_key=True,   # slug = id として扱える
        unique=True,
        max_length=20,
    )
    name = models.CharField(
        unique=True,
        max_length=20,
    )
    class Meta:
        ordering = ("slug", ) # slugで昇順ソート

    def __str__(self):
        return self.slug


def upload_blogimage_to(instance, filename):
    return os.path.join('image', 'blog', filename)

class Article(models.Model):
    title = models.CharField(
        max_length=30, 
        default="",
    )
    text = models.TextField(
        default="",
    )
    author = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        default='1'
    )
    created_at = models.DateField(
        auto_now_add=True, 
    )
    updated_at = models.DateField(
        auto_now=True, 
    )
    like_count = models.IntegerField(
       default=0,
    )
    tags = models.ManyToManyField(
        Tag,
        blank=True,
    )
    image = models.ImageField(
        upload_to = upload_blogimage_to,
        default="",
        blank=True,
    )
    favorite = models.ManyToManyField(
        Profile,
        related_name='favorite_by',
        blank=True,
    )
    is_published = models.BooleanField(
        default=False,
    )

    def __str__(self):
        return self.title


class Comment(models.Model):

    comment = models.TextField(
        default="", 
        max_length=500, 
    )
    created_at = models.DateField(
        auto_now_add=True, 
    )
    user = models.ForeignKey(
        Profile, 
        on_delete=models.CASCADE    # Userがいなくなったら、そのコメントは削除
    )    
    article = models.ForeignKey(
        Article, 
        on_delete=models.CASCADE    # 記事がなくなったら、そのコメントは削除
    )