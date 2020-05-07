from django.db import models

# Builds our scraper database object
class Scraper(models.Model):
    name = models.CharField(max_length=100)
    ip_address = models.GenericIPAddressField()
    port = models.PositiveSmallIntegerField()

    # the internet address that will be scraped
    seed = models.URLField(blank=True)

    def __str__(self):
        return self.name
