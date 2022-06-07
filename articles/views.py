from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from .models import Category, Comment, Post, Tag


def article_list(request):
    posts = Post.objects.all()
    categories = Category.objects.all()
    tags = Tag.objects.all()

    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'title': "記事一覧",
        # 'posts': posts,
        'page_obj': page_obj,
        'categories': categories,
        'tags': tags
    }
    return render(request, 'articles/articlelist.html', context)


def article_search(request):
    q = str(request.GET.get('q'))
    # print(word)
    posts = Post.objects.filter(title__icontains=q)
    categories = Category.objects.all()
    tags = Tag.objects.all()
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    # print(q)
    print(page_number)
    page_obj = paginator.get_page(page_number)

    context = {
        'title': f'検索結果：{q}',
        'page_obj': page_obj,
        'categories': categories,
        'tags': tags,
        'q': q
    }
    return render(request, 'articles/articlelist.html', context)


def article_category(request, category):
    posts = Post.objects.filter(category__name=category)
    categories = Category.objects.all()
    tags = Tag.objects.all()
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'title': f'カテゴリ：{category}',
        'page_obj': page_obj,
        'categories': categories,
        'tags': tags
    }
    return render(request, 'articles/articlelist.html', context)


def article_tag(request, tag):
    posts = Post.objects.filter(tags__name=tag)
    categories = Category.objects.all()
    tags = Tag.objects.all()
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'title': f'タグ：{tag}',
        'page_obj': page_obj,
        'categories': categories,
        'tags': tags,
    }
    return render(request, 'articles/articlelist.html', context)


def article_detail(request, pk):
    post = get_object_or_404(Post, id=pk)
    user_id = request.user.id
    is_liked = str(user_id) in [str(i.id) for i in post.liked.all()]

    # print([str(i.id) for i in study.liked.all()])
    context = {
        'post': post,
        'is_liked': is_liked
    }
    # print(study.content)
    return render(request, 'articles/articledetail.html', context)


@login_required
def like_unlike_article(request, pk):
    # いいねをするもしくは外すUser
    user = request.user
    try:
        # いいねされるまたは外される学習項目
        to_like = Post.objects.get(id=pk)

        if user in to_like.liked.all():
            to_like.liked.remove(user)
            to_like.save()

            return JsonResponse({'data': 'unlike'})
        else:
            to_like.liked.add(user)
            to_like.save()
            return JsonResponse({'data': 'like'})
    except Exception as e:
        # print(e)
        pass


@login_required
def create_comment(request, article_id):
    if request.method == "POST":
        text = request.POST.get('comment', None)
        post = Post.objects.filter(id=article_id).first()

        Comment.objects.create(
            comment=text, commented_by=request.user, post=post)
        return redirect('articles:article-detail', article_id)


@login_required
def delete_comment(request, comment_id):
    if request.method == "POST":
        data = get_object_or_404(Comment, id=comment_id)
        data.delete()
        article_id = str(data.post.id)
        return redirect('articles:article-detail', article_id)
