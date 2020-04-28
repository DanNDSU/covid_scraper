from django.urls import path, register_converter

from . import converters

from .views import (
    ScraperListView,
    ScraperDetailView,
    ScraperCreateView,
    ScraperUpdateView,
    ScraperDeleteView,
    ScraperOutputView,
    ScraperMegaOutputView,
    ScraperFurtherScrape,
)

register_converter(converters.URLStringConverter, 'url')

urlpatterns = [
    path('scraper/<int:pk>/delete/', ScraperDeleteView.as_view(), name='scraper_delete'),
    path('scraper/<int:pk>/edit/', ScraperUpdateView.as_view(), name='scraper_edit'),
    path('scraper/new/', ScraperCreateView.as_view(), name='scraper_new'),
    path('scraper/<int:pk>/', ScraperDetailView.as_view(), name='scraper_detail'),
    path('', ScraperListView.as_view(), name = 'scrapers'),
    path('scraper/<int:pk>/output/', ScraperOutputView.as_view(), name = 'output'),
    path('megascrape/', ScraperMegaOutputView.as_view(), name = 'megascrape'),
    path('scraper/furtherscrape/<str:name>/<path:seed>', ScraperFurtherScrape.as_view(), name = 'scraper_further_output'),
]
