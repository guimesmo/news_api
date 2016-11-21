from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.contrib import messages

from .models import News, Category, Comment
from .forms import CommentForm

# Create your views here.

def index(request):
    categories = Category.objects.all()
    return render(request, 'index.html', {'categories': categories})


def category_detail(request, slug):
    try:
        category = Category.objects.get(slug=slug)
    except Category.DoesNotExist:
        raise Http404
    news = News.objects.public(category=category)
    return render(request, 'category.html', {'category': category, 'news': news})


def news_detail(request, category_slug, slug):
    new = get_object_or_404(News, category__slug=category_slug, slug=slug)
    comments = Comment.objects.filter(reference_news=new)
    if request.method == 'POST':
        comments_form = CommentForm(request.POST, news_id=new.id)
        if comments_form.is_valid():
            comments_form.save()
            messages.success(request, "Obrigado por comentar!")
            return HttpResponseRedirect(".")
    else:
        comments_form = CommentForm(news_id=new.id)
    return render(request, 'view.html', {'new': new, 'comments': comments,
        'comments_form': comments_form})