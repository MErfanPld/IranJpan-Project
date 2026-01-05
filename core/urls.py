from django.urls import path
from .views import *

app_name = 'core'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('search/', SearchResultsView.as_view(), name='search_results'),
    path('about-us/', AboutUsView.as_view(), name="about_us"),
    path('contact/', ContactUsView.as_view(), name='contact'),
    path('guide/', BusinessGuideListView.as_view(), name='guide_country_list'),
    path('guide/<slug:slug>/', BusinessGuideDetailView.as_view(), name='guide_country_detail'),
    path('memebr/', MemberAboutSectionView.as_view(), name='member_about'),
]
