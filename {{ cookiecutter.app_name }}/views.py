from braces import views
from django.views import generic
from django.core.exceptions import PermissionDenied
from django.core.urlresolvers import reverse
from django.contrib import messages
from .models import {{ cookiecutter.model_name }}
from .forms import {{ cookiecutter.model_name }}Form


class OwnerRequiredMixin(object):

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()

        if request.user != self.object.user:
            raise PermissionDenied

        return super(OwnerRequiredMixin, self).dispatch(request, *args, **kwargs)

class {{ cookiecutter.model_name }}List(views.MultiplePermissionsRequiredMixin, views.StaticContextMixin, generic.ListView):
    permissions = {'any': ('{{ cookiecutter.app_name }}.add_{{ cookiecutter.model_name|lower }}', '{{ cookiecutter.app_name }}.change_{{ cookiecutter.model_name|lower }}', '{{ cookiecutter.app_name }}.delete_{{ cookiecutter.model_name|lower }}')}
    raise_exception = True
    static_context = {'page_title': '{{ cookiecutter.model_name }}s'}
    model = {{ cookiecutter.model_name }}

    def get_queryset(self):
        return {{ cookiecutter.model_name }}.objects.filter(user=self.request.user)


class {{ cookiecutter.model_name }}Detail(views.MultiplePermissionsRequiredMixin, OwnerRequiredMixin, generic.DetailView):
    permissions = {'any': ('{{ cookiecutter.app_name }}.add_{{ cookiecutter.model_name|lower }}', '{{ cookiecutter.app_name }}.change_{{ cookiecutter.model_name|lower }}', '{{ cookiecutter.app_name }}.delete_{{ cookiecutter.model_name|lower }}')}
    raise_exception = True
    model = {{ cookiecutter.model_name }}


class {{ cookiecutter.model_name }}Create(views.PermissionRequiredMixin, views.UserFormKwargsMixin, views.StaticContextMixin, generic.CreateView):
    permission_required = '{{ cookiecutter.app_name }}.add_{{ cookiecutter.model_name|lower }}'
    raise_exception = True
    model = {{ cookiecutter.model_name }}
    form_class = {{ cookiecutter.model_name }}Form
    static_context = {'page_title': 'Add {{ cookiecutter.model_name }}'}

    def form_valid(self, form):
        messages.success(self.request, 'The {{ cookiecutter.model_name|lower }} "{}" was added successfully.'.format(form.instance.title))
        return super({{ cookiecutter.model_name }}Create, self).form_valid(form)


class {{ cookiecutter.model_name }}Update(views.PermissionRequiredMixin, OwnerRequiredMixin, views.UserFormKwargsMixin, views.StaticContextMixin, generic.UpdateView):
    permission_required = '{{ cookiecutter.app_name }}.change_{{ cookiecutter.model_name|lower }}'
    raise_exception = True
    model = {{cookiecutter.model_name}}
    form_class = {{cookiecutter.model_name}}Form
    static_context = {'page_title': 'Update {{ cookiecutter.model_name }}'}

    def form_valid(self, form):
        messages.success(self.request, 'The {{ cookiecutter.model_name|lower }} "{}" was changed successfully.'.format(form.instance.title))
        return super({{ cookiecutter.model_name }}Update, self).form_valid(form)


class {{ cookiecutter.model_name }}Delete(views.PermissionRequiredMixin, OwnerRequiredMixin, generic.DeleteView):
    permission_required = '{{ cookiecutter.app_name }}.delete_{{ cookiecutter.model_name|lower }}'
    raise_exception = True
    model = {{ cookiecutter.model_name }}

    def get_success_url(self):
        messages.success(self.request, 'The {{ cookiecutter.model_name|lower }} "{}" was deleted successfully.'.format(self.object))
        return reverse('{{ cookiecutter.app_name }}:{{ cookiecutter.model_name|lower }}_list')
