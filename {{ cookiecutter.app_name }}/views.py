from django.views import generic
from django.core.urlresolvers import reverse
from django.contrib import messages
from .models import {{ cookiecutter.model_name }}


class {{ cookiecutter.model_name }}Index(generic.ListView):
    model = {{ cookiecutter.model_name }}


class {{ cookiecutter.model_name }}Detail(generic.DetailView):
    model = {{ cookiecutter.model_name }}


class {{ cookiecutter.model_name }}Add(generic.CreateView):
    model = {{ cookiecutter.model_name }}

    def form_valid(self, form):
        messages.success(self.request, 'The {{ cookiecutter.model_name|lower }} "{}" was added successfully.'.format(form.instance.title))
        return super({{ cookiecutter.model_name }}Add, self).form_valid(form)


class {{ cookiecutter.model_name }}Edit(generic.UpdateView):
    model = {{ cookiecutter.model_name }}

    def form_valid(self, form):
        messages.success(self.request, 'The {{ cookiecutter.model_name|lower }} "{}" was changed successfully.'.format(form.instance.title))
        return super({{ cookiecutter.model_name }}Edit, self).form_valid(form)


class {{ cookiecutter.model_name }}Delete(generic.DeleteView):
    model = {{ cookiecutter.model_name }}

    def get_success_url(self):
        messages.success(self.request, 'The {{ cookiecutter.model_name|lower }} "{}" was deleted successfully.'.format(self.object))
        return reverse('{{ cookiecutter.app_name }}:{{ cookiecutter.model_name|lower }}_index')
