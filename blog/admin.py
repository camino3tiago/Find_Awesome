from django.contrib import admin
from .models import Article, Comment, Tag


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    fields = ('comment', 'user', 'article', 'created_at', )
    readonly_fields = ('created_at',)
    list_display = ('article', 'user',)

class TagInline(admin.TabularInline):   # admin.~Inlineにも複数種のインラインがある模様（StackedInlineなど）
    model = Article.tags.through

class ArticleAdmin(admin.ModelAdmin):
    inlines = [TagInline,]  # ↑で作成したTagTabularInlineをインラインとしてArticle欄に挿入
    exclude = ['tags',]     # tags欄を非表示

admin.site.register(Article, ArticleAdmin)
admin.site.register(Tag)