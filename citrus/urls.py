from django.conf.urls import patterns, include, url
from django.contrib import admin

from calc import views

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'citrus.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    # url(r'^admin/', include(admin.site.urls)),
    url(r'^api/calc', views.CalcApi.as_view(), name="calc"),
    url(r'^$',  views.CalcView.as_view(), name='home'),
)
