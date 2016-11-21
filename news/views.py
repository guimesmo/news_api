from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.contrib import messages
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import News, Category, Comment
from .forms import CommentForm
from .serializers import CategoryModelSerializer, NewsModelSerializer

# Create your views here.

class IndexView(APIView):
    def get(self, request):
        categories = Category.objects.all()
        serializer = CategoryModelSerializer(categories, many=True)
        return Response(serializer.data)
index = IndexView.as_view()


class CategoryDetailView(APIView):
    def get_object(self, slug):
        try:
            return Category.objects.get(slug__iexact=slug)
        except Category.DoesNotExist:
            raise Http404

    def get(self, request, slug, format=None):
        category = self.get_object(slug)
        serializer = NewsModelSerializer(category.news_set.all(), many=True)
        return Response(serializer.data)
category_detail = CategoryDetailView.as_view()


class NewsDetailView(APIView):
    def get_object(self, category_slug, slug):
        try:
            return News.objects.public(category__slug__iexact=category_slug, slug__iexact=slug).get()
        except News.DoesNotExist:
            raise Http404

    def get(self, request, category_slug, slug, format=None):
        object = self.get_object(category_slug, slug)
        serializer = NewsModelSerializer(object)
        return Response(serializer.data)

    def post(self, request, category_slug, slug):
        object = self.get_object(category_slug, slug)
        serializer = NewsModelSerializer(object, request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
news_detail = NewsDetailView.as_view()