"""news_api URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from news.views import category_detail, index, news_detail
from news.api_views import NewsList

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', index),
    url(r'^api/news/$', NewsList.as_view(), name='news_api'),
    url(r'^(?P<slug>\w+)/$', category_detail, name='category_detail'),
    url(r'^(?P<category_slug>[\w-]+)/(?P<slug>[\w-]+)/$', news_detail, name='news_detail'),
]
