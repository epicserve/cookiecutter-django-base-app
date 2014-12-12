from django.views import generic
from django.core.urlresolvers import reverse
from django.contrib import messages
from .models import {{ cookiecutter.model_name }}


class {{ cookiecutter.model_name }}List(generic.ListView):
    model = {{ cookiecutter.model_name }}


class {{ cookiecutter.model_name }}Detail(generic.DetailView):
    model = {{ cookiecutter.model_name }}


class {{ cookiecutter.model_name }}Create(generic.CreateView):
    model = {{ cookiecutter.model_name }}
    fields = ('title', 'description')

    def form_valid(self, form):
        messages.success(self.request, 'The {{ cookiecutter.model_name|lower }} "{}" was added successfully.'.format(form.instance.title))
        return super({{ cookiecutter.model_name }}Create, self).form_valid(form)


class {{ cookiecutter.model_name }}Update(generic.UpdateView):
    model = {{ cookiecutter.model_name }}
    fields = ('title', 'description')

    def form_valid(self, form):
        messages.success(self.request, 'The {{ cookiecutter.model_name|lower }} "{}" was changed successfully.'.format(form.instance.title))
        return super({{ cookiecutter.model_name }}Update, self).form_valid(form)


class {{ cookiecutter.model_name }}Delete(generic.DeleteView):
    model = {{ cookiecutter.model_name }}

    def get_success_url(self):
        messages.success(self.request, 'The {{ cookiecutter.model_name|lower }} "{}" was deleted successfully.'.format(self.object))
        return reverse('{{ cookiecutter.app_name }}:{{ cookiecutter.model_name|lower }}_list')
