from django.contrib import admin
from .models import News, Category, Comment


class CommentInline(admin.StackedInline):
    model = Comment
    extra = 0


class NewsAdmin(admin.ModelAdmin):
    list_display = ('creation_date', 'title',)
    inlines = [CommentInline,]


# Register your models here.
admin.site.register(News, NewsAdmin)
admin.site.register(Category)