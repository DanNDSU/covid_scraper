# relies on django's class based views

from django.views.generic.base import TemplateView
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import Scraper
from .client import GetOutput
from .mega_client import MegaScrape
from django.urls import reverse_lazy

# webpage: a list of all our scrapers
class ScraperListView(ListView):
    model = Scraper
    template_name = 'scrapers.html'

# webpage: a look at a single scraper
class ScraperDetailView(DetailView):
    model = Scraper
    template_name = 'scraper_detail.html'

# holds the output of a single scraper
class ScraperOutputView(TemplateView):
    template_name = 'scraper_output.html'
    def get_context_data(self, **kwargs):
        scraper = Scraper.objects.get(pk=self.kwargs['pk'])
        # Here is the portal to the clien (GetOutput function)
        context = {'messages': GetOutput(scraper.ip_address, scraper.port, scraper.seed, scraper.name),
                   'ip_address': str(scraper.ip_address), 'port': str(scraper.port), 'seed': str(scraper.seed)}
        return context

# when the first srape runs, this allows scraping of a new url from the output page
class ScraperFurtherScrape(TemplateView):
    template_name = 'scraper_output.html'
    def get_context_data(self, **kwargs):
        scraper = Scraper.objects.get(name=self.kwargs['name'])
        scraper.seed = self.kwargs['seed']
        context = {'messages': GetOutput(scraper.ip_address, scraper.port, scraper.seed, scraper.name),
                   'ip_address': str(scraper.ip_address), 'port': str(scraper.port)}
        return context

# the output of our distributed scrape
class ScraperMegaOutputView(TemplateView):
    template_name = 'scraper_mega_output.html'
    def get_context_data(self, **kwargs):
        scrapers = Scraper.objects.all()
        context = {'messages': MegaScrape(scrapers),}
        return context

# logic for web form to make a new scraper
class ScraperCreateView(CreateView):
    model = Scraper
    template_name = 'scraper_new.html'
    fields = ['name', 'ip_address', 'port', 'seed']
    success_url = reverse_lazy('scrapers')

# logic for web form to edit a scraper
class ScraperUpdateView(UpdateView):
    model = Scraper
    template_name = 'scraper_edit.html'
    fields = ['name', 'ip_address', 'port', 'seed']
    success_url = reverse_lazy('scrapers')

# logic for web form to remove a scraper 
class ScraperDeleteView(DeleteView):
    model = Scraper
    template_name = 'scraper_delete.html'
    success_url = reverse_lazy('scrapers')
