from django.test import Client, TestCase
from django.core.urlresolvers import reverse
from django.contrib.auth import get_user_model
from django.conf import settings
from ..factories import {{ cookiecutter.model_name }}Factory
from ..models import {{ cookiecutter.model_name }}

User = get_user_model()
c = Client()


class BaseViews(TestCase):

    def setUp(self):
        self.normal_user = User.objects.create_user('normal_user', 'normal_user@example.com', 'secret')
        self.normal_user.save()

    def assertBasicRedirect(self, response, redirect_url):
        redirect_url = "http://testserver{}".format(redirect_url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, redirect_url)


class {{ cookiecutter.model_name }}IndexViews(BaseViews):

    def test_index_login_required(self):
        resp = c.get(reverse('{{ cookiecutter.app_name }}:{{ cookiecutter.model_name|lower }}_index'))
        self.assertBasicRedirect(resp, '{}?next={}'.format(settings.LOGIN_URL, reverse('{{ cookiecutter.app_name }}:{{ cookiecutter.model_name|lower }}_index')))

    def test_index(self):
        c.login(username='normal_user', password='secret')
        resp = c.get(reverse('{{ cookiecutter.app_name }}:{{ cookiecutter.model_name|lower }}_index'))
        self.assertEqual(resp.status_code, 200)
        self.assertEqual([obj.pk for obj in resp.context['object_list']], [])


class {{ cookiecutter.model_name }}AddViews(BaseViews):

    def setUp(self):
        super({{ cookiecutter.model_name }}AddViews, self).setUp()

    def test_add_login_required(self):
        resp = c.get(reverse('{{ cookiecutter.app_name }}:{{ cookiecutter.model_name|lower }}_add'))
        self.assertBasicRedirect(resp, '{}?next={}'.format(settings.LOGIN_URL, reverse('{{ cookiecutter.app_name }}:{{ cookiecutter.model_name|lower }}_add')))

    def test_add(self):
        c.login(username='normal_user', password='secret')
        url = reverse('{{ cookiecutter.app_name }}:{{ cookiecutter.model_name|lower }}_add')
        resp = c.get(url)
        self.assertEqual(resp.status_code, 200)

        resp = c.post(url, {'title': 'Title 1 (added)', 'description': 'Description 1 (added)'})
        {{ cookiecutter.model_name|lower }} = {{ cookiecutter.model_name }}.objects.all().get()
        self.assertBasicRedirect(resp, {{ cookiecutter.model_name|lower }}.get_absolute_url())
        self.assertEqual({{ cookiecutter.model_name|lower }}.title, 'Title 1 (added)')
        self.assertEqual({{ cookiecutter.model_name|lower }}.description, 'Description 1 (added)')

    def test_add_with_empty_form(self):
        c.login(username='normal_user', password='secret')
        url = reverse('{{ cookiecutter.app_name }}:{{ cookiecutter.model_name|lower }}_add')
        resp = c.post(url)
        self.assertEqual(resp.status_code, 200)
        self.assertFormError(resp, 'form', 'title', 'This field is required.')
        self.assertFormError(resp, 'form', 'description', 'This field is required.')


class {{ cookiecutter.model_name }}DetailViews(BaseViews):

    def setUp(self):
        self.{{ cookiecutter.model_name|lower }} = {{ cookiecutter.model_name }}Factory()
        super({{ cookiecutter.model_name }}DetailViews, self).setUp()

    def test_detail_login_required(self):
        url = self.{{ cookiecutter.model_name|lower }}.get_absolute_url()
        resp = c.get(url)
        self.assertBasicRedirect(resp, '{}?next={}'.format(settings.LOGIN_URL, url))

    def test_detail(self):
        c.login(username='normal_user', password='secret')
        url = self.{{ cookiecutter.model_name|lower }}.get_absolute_url()
        resp = c.get(url)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.context_data['object'].title, self.{{ cookiecutter.model_name|lower }}.title)
        self.assertEqual(resp.context_data['object'].description, self.{{ cookiecutter.model_name|lower }}.description)


class {{ cookiecutter.model_name }}EditViews(BaseViews):

    def setUp(self):
        self.{{ cookiecutter.model_name|lower }} = {{ cookiecutter.model_name }}Factory()
        super({{ cookiecutter.model_name }}EditViews, self).setUp()

    def test_edit_login_required(self):
        url = self.{{ cookiecutter.model_name|lower }}.get_absolute_url()
        resp = c.get(url)
        self.assertBasicRedirect(resp, '{}?next={}'.format(settings.LOGIN_URL, url))

    def test_edit(self):
        c.login(username='normal_user', password='secret')
        url = reverse('{{ cookiecutter.app_name }}:{{ cookiecutter.model_name|lower }}_edit', kwargs={'pk': self.{{ cookiecutter.model_name|lower }}.pk})
        resp = c.get(url)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.context_data['object'].title, self.{{ cookiecutter.model_name|lower }}.title)
        self.assertEqual(resp.context_data['object'].description, self.{{ cookiecutter.model_name|lower }}.description)

        resp = c.post(url, {'title': 'Title (edited)', 'description': 'Description (edited)'})
        {{ cookiecutter.model_name|lower }} = {{ cookiecutter.model_name }}.objects.get(pk=self.{{ cookiecutter.model_name|lower }}.pk)
        self.assertBasicRedirect(resp, {{ cookiecutter.model_name|lower }}.get_absolute_url())
        self.assertEqual({{ cookiecutter.model_name|lower }}.title, 'Title (edited)')
        self.assertEqual({{ cookiecutter.model_name|lower }}.description, 'Description (edited)')

    def test_edit_with_empty_form(self):
        c.login(username='normal_user', password='secret')
        url = reverse('{{ cookiecutter.app_name }}:{{ cookiecutter.model_name|lower }}_edit', kwargs={'pk': self.{{ cookiecutter.model_name|lower }}.pk})
        resp = c.post(url)
        self.assertEqual(resp.status_code, 200)
        self.assertFormError(resp, 'form', 'title', 'This field is required.')
        self.assertFormError(resp, 'form', 'description', 'This field is required.')


class DeleteViews(BaseViews):

    def setUp(self):
        self.{{ cookiecutter.model_name|lower }} = {{ cookiecutter.model_name }}Factory()
        super(DeleteViews, self).setUp()

    def test_delete_login_required(self):
        url = reverse('{{ cookiecutter.app_name }}:{{ cookiecutter.model_name|lower }}_delete', kwargs={'pk': self.{{ cookiecutter.model_name|lower }}.pk})
        resp = c.get(url)
        self.assertBasicRedirect(resp, '{}?next={}'.format(settings.LOGIN_URL, url))

    def test_delete(self):
        c.login(username='normal_user', password='secret')
        url = reverse('{{ cookiecutter.app_name }}:{{ cookiecutter.model_name|lower }}_delete', kwargs={'pk': self.{{ cookiecutter.model_name|lower }}.pk})
        resp = c.get(url)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.context_data['object'].title, self.{{ cookiecutter.model_name|lower }}.title)
        self.assertEqual(resp.context_data['object'].description, self.{{ cookiecutter.model_name|lower }}.description)

        c.post(url, {})
        {{ cookiecutter.app_name }} = {{ cookiecutter.model_name }}.objects.all()
        self.assertEqual(len({{ cookiecutter.app_name }}), 0)
