from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import TemplateView,ListView,DetailView
from django.views.generic import FormView

from blogs.models import Article, Category, Tag
from core.forms import ContactForm, SearchForm
from settings.models import SiteSettings,Advertisement
from .models import AboutUs, Country, MemberAboutSection, Slider, TeamMember,JapanChamberDirectorsMember

# Create your views here.

class HomeView(ListView):
    model = Slider
    template_name = "./core/home.html"    
    context_object_name = "sliders"

    def get_queryset(self):
        return Slider.objects.filter(is_active=True).order_by('-created_at')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['latest_articles'] = Article.objects.filter(is_published=True).order_by('-created_at')[:3]

        politics_category = Category.objects.filter(title__icontains="سیاست").first()
        culture_category = Category.objects.filter(title__icontains="فرهنگ").first()

        # مقالات هر دسته
        context['politics_articles'] = Article.objects.filter(
            category=politics_category, is_published=True
        ).order_by('-created_at')[:3] if politics_category else []

        context['culture_articles'] = Article.objects.filter(
            category=culture_category, is_published=True
        ).order_by('-created_at')[:3] if culture_category else []
        
        context['site_settings'] = SiteSettings.objects.first()
        context['advertisement_settings'] = Advertisement.objects.filter(is_active=True)
        context['j_members'] = JapanChamberDirectorsMember.objects.all()
        context['search_form'] = SearchForm()
        return context
    
    
class SearchResultsView(ListView):
    model = Article
    template_name = 'core/search_results.html'
    context_object_name = 'articles'

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            return Article.objects.filter(title__icontains=query, is_published=True)
        return Article.objects.none()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tags'] = Tag.objects.all()
        context['cats'] = Category.objects.all()
        context['popular_articles'] = Article.objects.filter(
            is_published=True
        ).order_by('-created_at')[:5]
        return context
    
    
class AboutUsView(TemplateView):
    template_name = "core/about_us.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['about'] = AboutUs.objects.first()
        context['team_members'] = TeamMember.objects.all()
        context['site_settings'] = SiteSettings.objects.first()
        return context
    
    
class ContactUsView(FormView):
    template_name = "core/contact.html"
    form_class = ContactForm
    success_url = reverse_lazy('core:contact')

    def form_valid(self, form):
        form.save()
        from django.contrib import messages
        messages.success(self.request, "پیام شما با موفقیت ارسال شد.")
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['site_settings'] = SiteSettings.objects.first()
        return context
    
    
class BusinessGuideListView(ListView):
    model = Country
    template_name = 'core/guide_list.html'
    context_object_name = 'countries'

    def get_queryset(self):
        return Country.objects.filter(is_active=True)
    

class BusinessGuideDetailView(DetailView):
    model = Country
    template_name = 'core/guide_detail.html'
    context_object_name = 'country'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['sections'] = self.object.sections.filter(is_active=True)
        return context


class MemberAboutSectionView(ListView):
    model = MemberAboutSection
    template_name = 'core/member_about.html'
    context_object_name = 'members'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['sections'] = MemberAboutSection.objects.filter(is_active=True).order_by('created_at')
        return context