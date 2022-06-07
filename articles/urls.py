from django.urls import path
from .views import (
    article_list,
    article_search,
    article_detail,
    like_unlike_article,
    article_tag,
    article_category,
    create_comment,
    delete_comment
)

app_name = 'articles'

urlpatterns = [
    path('', article_list, name='article-list'),
    path('search', article_search, name='article-search'),
    path('detail/<uuid:pk>', article_detail, name='article-detail'),
    path('detail/like/<uuid:pk>', like_unlike_article, name='like'),
    path('category/<str:category>', article_category, name='article-category'),
    path('tag/<str:tag>', article_tag, name='article-tag'),
    path('comment/<uuid:article_id>', create_comment, name='comment-create'),
    path('comment-delete/<uuid:comment_id>',
         delete_comment, name='comment-delete'),

]
