from django.shortcuts import render, redirect
from .models import Article, Comment, Tag
from django.core.paginator import Paginator
from .forms import CommentForm, PostForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages


def index(request):
    articles = Article.objects.all().order_by('-created_at')
    paginator = Paginator(articles, 3)  # 2つ/ページ
    page_number = request.GET.get('page')   # urlのパス名に'page'があれば、キー（page=1の1部分）を取得
    context = {
        'page_title': 'Blog List',
        'page_article': paginator.get_page(page_number),
        'page_number': page_number,
    }
    return render(request,
        'blog/blogs.html',
        context
    )

def article(request, pk):
    article = Article.objects.get(pk=pk)
    print(article.author.user == request.user)
    if request.method == 'POST':
        if request.POST.get('like_count', None):
            article.like_count += 1
            article.save()
        else:
            form = CommentForm(request.POST)
            if form.is_valid():
                comment = form.save(commit=False)   # DBには反映しないが、変数commentに渡す(CommentモデルのcommentはCommentFormのfieldsで指定した通り、ここに含まれる)
                # 以下、CommentFormで指定しなかったfieldsの定義
                comment.user = request.user.profile         # Commentモデルのuserは、その時のユーザー(formをPOSTしたログインユーザー)
                comment.article = article           # 上で指定したpkのarticle
                comment.save()

    comments = Comment.objects.filter(article=article)  # Commentモデルのarticleフィールド=指定したpkのarticleのコメント
    context = {
        'article': article,
        'comments': comments,
        'my_post': article.author.user == request.user, # 自分の投稿であればTrue, そうでなければfalse
    }

    return render(request,
        'blog/article.html',
        context
    )


def tags(request, slug):
    tag = Tag.objects.get(slug=slug)
    articles = tag.article_set.all()    # tagを参照しているArticle
    # ----- index()関数の使い回し（一部変更） -----
    paginator = Paginator(articles, 10)  # 10こ/ページ
    page_number = request.GET.get('page')   # urlのパス名に'page'があれば、キー（page=1の1部分）を取得
    context = {
        'page_title' : f'# {slug}',
        'page_article': paginator.get_page(page_number),
        'page_number': page_number,
    }
    return render(request,
        'blog/blogs.html',
        context
    )


from django.views.decorators.csrf import ensure_csrf_cookie
from django.http import JsonResponse

@ensure_csrf_cookie # csrf_tokenがないとPOST送信されないため
def like(request, pk):
    d = {'message': 'error'}
    if request.method == 'POST':
        article = Article.objects.get(pk=pk)
        article.like_count += 1
        article.save()

        d['message'] = 'success'
    return JsonResponse(d)      # templateで返すのではなく、Jsonで返す



# articleをお気に入り登録する
@ensure_csrf_cookie
def add_favorite(request, pk):
    article = Article.objects.get(pk=pk)
    profile = request.user.profile

    d = {'message': 'error'}
    if request.method == 'POST':
        if profile in article.favorite.all():
            article.favorite.remove(profile)
        else:
            article.favorite.add(profile)
        d['message'] = 'success'

    return JsonResponse(d)


def add_post(request):
    kwargs = {'user': request.user.profile.username}
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, **kwargs)
        if form.is_valid():
            form.save(commit=False)
            form.author = request.user.profile
            form.save()
            messages.success(request, f'「新しい投稿が完了しました。')
            return redirect('blog:blog')
    else:
        form = PostForm(**kwargs)
        return render(request,
            'mysite/add_post.html',
            context = {
                'form': form,
            }
        )

def my_posts(request):
    articles = Article.objects.filter(author=request.user.profile)
    return render(request,
        'blog/blogs.html',
        context = {
            'page_article': articles
        }
    )

def edit_post(request, pk):
    article = Article.objects.get(pk=pk)
    kwargs = {'user': request.user.profile.username}

    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=article, **kwargs)
        if form.is_valid():
            form.save(commit=False)
            form.author = request.user.profile
            form.save()
            messages.success(request, f'「{article.title}」を投稿しました。')
            return redirect('blog:blog')
    else:
        form = PostForm(instance=article, **kwargs)
        return render(request,
            'mysite/add_post.html',
            context = {
                'form': form,
                'article': article
            }
        )

def delete_post(request, pk):
    article = Article.objects.get(pk=pk)
    
    if request.method == "POST":
        article.delete()
        messages.info(request, f'「{article.title}」を削除しました。')
    return redirect('blog:blog')

    
    