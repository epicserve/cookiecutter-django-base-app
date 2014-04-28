from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required
from . import views


urlpatterns = patterns(
    '',
    url(r'^$', login_required(views.{{ cookiecutter.model_name }}Index.as_view()), name='{{ cookiecutter.model_name|lower }}_index'),
    url(r'^add/$', login_required(views.{{ cookiecutter.model_name }}Add.as_view()), name='{{ cookiecutter.model_name|lower }}_add'),
    url(r'^(?P<pk>[\d]+)/$', login_required(views.{{ cookiecutter.model_name }}Detail.as_view()), name='{{ cookiecutter.model_name|lower }}_detail'),
    url(r'^(?P<pk>[\d]+)/edit/$', login_required(views.{{ cookiecutter.model_name }}Edit.as_view()), name='{{ cookiecutter.model_name|lower }}_edit'),
    url(r'^(?P<pk>[\d]+)/delete/$', login_required(views.{{ cookiecutter.model_name }}Delete.as_view()), name='{{ cookiecutter.model_name|lower }}_delete'),
)
