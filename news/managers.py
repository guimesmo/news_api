from django.db import models

class NewsManager(models.Manager):
    def public(self, **kwargs):
        return self.filter(public=True, **kwargs)