from django.db import models

class Scraper(models.Model):
    name = models.CharField(max_length=100)
    ip_address = models.GenericIPAddressField()
    port = models.PositiveSmallIntegerField()
    seed = models.URLField(blank=True)

    def __str__(self):
        return self.name
