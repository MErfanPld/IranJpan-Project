from django.urls import path
from .views import (
    ArticleListView,
    ArticleDetailView,
    CategoryArticleListView,
    TagArticleListView
)

app_name = 'blog'

urlpatterns = [
    path('', ArticleListView.as_view(), name='blog_list'),
    path('<slug:slug>/', ArticleDetailView.as_view(), name='blog_detail'),

    path('category/<slug:slug>/', CategoryArticleListView.as_view(), name='category_blog'),
    path('tag/<slug:slug>/', TagArticleListView.as_view(), name='tag_blog'),
]
