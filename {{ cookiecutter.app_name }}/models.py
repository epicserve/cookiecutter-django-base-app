from django.db import models
from django.core.urlresolvers import reverse


class {{ cookiecutter.model_name }}(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('{{ cookiecutter.app_name }}:{{ cookiecutter.model_name|lower }}_detail', kwargs={'pk': self.pk})
