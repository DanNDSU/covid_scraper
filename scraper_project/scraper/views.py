from django.views.generic.base import TemplateView
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import Scraper
from .client import GetOutput
from .mega_client import MegaScrape
from django.urls import reverse_lazy

class ScraperListView(ListView):
    model = Scraper
    template_name = 'scrapers.html'

class ScraperDetailView(DetailView):
    model = Scraper
    template_name = 'scraper_detail.html'

class ScraperOutputView(TemplateView):
    template_name = 'scraper_output.html'
    def get_context_data(self, **kwargs):
        scraper = Scraper.objects.get(pk=self.kwargs['pk'])
        # Here is the portal to the clien (GetOutput function)
        context = {'messages': GetOutput(scraper.ip_address, scraper.port, scraper.seed, scraper.name),
                   'ip_address': str(scraper.ip_address), 'port': str(scraper.port), 'seed': str(scraper.seed)}
        return context

class ScraperFurtherScrape(TemplateView):
    template_name = 'scraper_output.html'
    def get_context_data(self, **kwargs):
        scraper = Scraper.objects.get(name=self.kwargs['name'])
        scraper.seed = self.kwargs['seed']
        context = {'messages': GetOutput(scraper.ip_address, scraper.port, scraper.seed, scraper.name),
                   'ip_address': str(scraper.ip_address), 'port': str(scraper.port)}
        return context

class ScraperMegaOutputView(TemplateView):
    template_name = 'scraper_mega_output.html'
    def get_context_data(self, **kwargs):
        scrapers = Scraper.objects.all()
        context = {'messages': MegaScrape(scrapers),}
        return context

class ScraperCreateView(CreateView):
    model = Scraper
    template_name = 'scraper_new.html'
    fields = ['name', 'ip_address', 'port', 'seed']
    success_url = reverse_lazy('scrapers')

class ScraperUpdateView(UpdateView):
    model = Scraper
    template_name = 'scraper_edit.html'
    fields = ['name', 'ip_address', 'port', 'seed']
    success_url = reverse_lazy('scrapers')

class ScraperDeleteView(DeleteView):
    model = Scraper
    template_name = 'scraper_delete.html'
    success_url = reverse_lazy('scrapers')
