from django.views.generic import ListView, DetailView
from .models import News, NewsCategory


class NewsListView(ListView):
    model = News
    template_name = 'news/news_list.html'
    context_object_name = 'news_list'
    # paginate_by = 2

    def get_queryset(self):
        return News.objects.filter(is_published=True)


class NewsDetailView(DetailView):
    model = News
    template_name = 'news/news_detail.html'
    context_object_name = 'news'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cats'] = NewsCategory.objects.filter(is_active=True)
        context['prev_news'] = News.objects.filter(
            id__lt=self.object.id
        ).order_by('-id').first()
        context['next_news'] = News.objects.filter(
            id__gt=self.object.id
        ).order_by('id').first()
        context['popular_news'] = News.objects.filter(
            is_published=True
        ).order_by('-created_at')[:5]
        return context


class CategoryNewsListView(ListView):
    model = News
    template_name = 'news/category_news_list.html'
    context_object_name = 'news_list'
    paginate_by = 9

    def get_queryset(self):
        self.category = NewsCategory.objects.get(
            slug=self.kwargs['slug'],
            is_active=True
        )
        return self.category.news.filter(is_published=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.category
        return context
