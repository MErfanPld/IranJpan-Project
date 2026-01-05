from django.views.generic import (
    ListView, DetailView, CreateView
)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect

from settings.models import SiteSettings
from .models import Article, Category, Tag
from .forms import ArticleForm, CommentForm
from django.db.models import F


class ArticleListView(ListView):
    model = Article
    template_name = 'blog/blog_list.html'
    paginate_by = 6
    context_object_name = 'articles'

    def get_queryset(self):
        return Article.objects.filter(is_published=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tags'] = Tag.objects.all()
        context['site_settings'] = SiteSettings.objects.first()
        context['cats'] = Category.objects.all()
        context['popular_articles'] = Article.objects.filter(
            is_published=True
        ).order_by('-created_at')[:5]
        return context
    

class ArticleDetailView(DetailView):
    model = Article
    template_name = 'blog/blog_detail.html'
    form_class = CommentForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comment_form'] = CommentForm()
        context['site_settings'] = SiteSettings.objects.first()
        context['prev_article'] = Article.objects.filter(
            id__lt=self.object.id, is_published=True
        ).order_by('-id').first()
        context['next_article'] = Article.objects.filter(
            id__gt=self.object.id, is_published=True
        ).order_by('id').first()
        return context

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        Article.objects.filter(pk=obj.pk).update(
            view_count=F('view_count') + 1
        )
        obj.refresh_from_db()
        return obj

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.article = self.object
            comment.user = request.user
            comment.save()
        return redirect(self.object.get_absolute_url())


# class ArticleCreateView(LoginRequiredMixin, CreateView):
#     model = Article
#     form_class = ArticleForm
#     template_name = 'blog/article_form.html'

#     def form_valid(self, form):
#         form.instance.author = self.request.user
#         return super().form_valid(form)


class CategoryArticleListView(ListView):
    template_name = 'blog/blog_list.html'

    def get_queryset(self):
        return Article.objects.filter(
            category__slug=self.kwargs['slug'],
            is_published=True
        )
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tags'] = Tag.objects.all()
        context['site_settings'] = SiteSettings.objects.first()
        context['cats'] = Category.objects.all()
        context['popular_articles'] = Article.objects.filter(
            is_published=True
        ).order_by('-created_at')[:5]
        return context

class TagArticleListView(ListView):
    template_name = 'blog/blog_list.html'

    def get_queryset(self):
        return Article.objects.filter(
            tags__slug=self.kwargs['slug'],
            is_published=True
        )
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tags'] = Tag.objects.all()
        context['site_settings'] = SiteSettings.objects.first()
        context['cats'] = Category.objects.all()
        context['popular_articles'] = Article.objects.filter(
            is_published=True
        ).order_by('-created_at')[:5]
        return context