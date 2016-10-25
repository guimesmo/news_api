from django import db
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.template.defaultfilters import slugify

from .managers import NewsManager

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True, db_index=True,
        editable=False)

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('category_detail', args=[self.slug])

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)


class News(models.Model):
    category = models.ForeignKey(Category)
    creation_date = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=100, help_text="Um título para noticia")
    slug = models.SlugField(max_length=100, unique=True, editable=False)
    text = models.TextField(help_text="Inclua um texto simples, sem tags")
    public = models.BooleanField(default=True)

    objects = NewsManager()

    class Meta:
        verbose_name = 'notícia'
        verbose_name_plural = 'notícias'
        ordering = ('-creation_date',)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('news_detail', args=[self.category.slug, self.slug])

    def slugify(self, increment=0):
        self.slug = slugify(self.title)
        equals = self.objects.filter(slug=self.slug).exclude(pk=self.pk).count()
        if equals:
            count = equals
            self.slug = slugify(self.title)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        tries = 1
        while tries:
            try:
                with db.transaction.atomic():
        	        super(News, self).save(*args, **kwargs)
        	        tries = 0
            except db.IntegrityError:
                self.slug = slugify("%s %d" %(self.title, tries))
                tries += 1


class Comment(models.Model):
    reference_news = models.ForeignKey(News)
    comment_datetime = models.DateTimeField(auto_now_add=True)
    author = models.CharField(max_length=100)
    title = models.CharField(max_length=100, default="Sem título")
    comment = models.CharField(max_length=255)

    def __str__(self):
        return "%s de %s" % (self.title, self.author)

