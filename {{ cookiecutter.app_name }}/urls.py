from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required
from . import views


urlpatterns = patterns(
    '',
    url(r'^$', login_required(views.{{ cookiecutter.model_name }}List.as_view()), name='{{ cookiecutter.model_name|lower }}_list'),
    url(r'^add/$', login_required(views.{{ cookiecutter.model_name }}Create.as_view()), name='{{ cookiecutter.model_name|lower }}_create'),
    url(r'^(?P<pk>[\d]+)/$', login_required(views.{{ cookiecutter.model_name }}Detail.as_view()), name='{{ cookiecutter.model_name|lower }}_detail'),
    url(r'^(?P<pk>[\d]+)/edit/$', login_required(views.{{ cookiecutter.model_name }}Update.as_view()), name='{{ cookiecutter.model_name|lower }}_update'),
    url(r'^(?P<pk>[\d]+)/delete/$', login_required(views.{{ cookiecutter.model_name }}Delete.as_view()), name='{{ cookiecutter.model_name|lower }}_delete'),
)
