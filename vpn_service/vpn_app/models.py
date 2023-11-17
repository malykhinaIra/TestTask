from django.db import models
from users.models import CustomUser


class Site(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    url = models.URLField()

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        site_statistics, created = SiteStatistics.objects.get_or_create(site=self)

        if created:
            site_statistics.save()


class SiteStatistics(models.Model):
    site = models.OneToOneField('Site', related_name='statistics', on_delete=models.CASCADE)
    hits = models.PositiveIntegerField(default=0)
    data_sent = models.PositiveIntegerField(default=0)
    data_received = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"Statistics for {self.site.name}"
