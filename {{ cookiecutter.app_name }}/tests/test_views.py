from django.contrib.auth.models import Permission
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
        perms = list(Permission.objects.filter(codename__endswith='{{ cookiecutter.model_name|lower }}'))
        self.normal_user = User.objects.create_user('normal_user', 'normal_user@example.com', 'secret')
        self.normal_user.user_permissions.add(*perms)
        self.no_perms_user = User.objects.create_user('no_perms_user', 'no_perms_user@example.com', 'secret')
        self.wrong_user = User.objects.create_user('wrong_user', 'wrong_user@example.com', 'secret')
        self.wrong_user.user_permissions.add(*perms)

    def assertBasicRedirect(self, response, redirect_url):
        redirect_url = "http://testserver{}".format(redirect_url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, redirect_url)


class {{ cookiecutter.model_name }}ListView(BaseViews):

    def setUp(self):
        super({{ cookiecutter.model_name }}ListView, self).setUp()
        self.url = reverse('{{ cookiecutter.app_name }}:{{ cookiecutter.model_name|lower }}_list')

    def test_login_required(self):
        resp = c.get(self.url)
        self.assertBasicRedirect(resp, '{}?next={}'.format(settings.LOGIN_URL, reverse('{{ cookiecutter.app_name }}:{{ cookiecutter.model_name|lower }}_list')))

    def test_no_perms(self):
        c.login(username='no_perms_user', password='secret')
        resp = c.get(self.url)
        self.assertEqual(resp.status_code, 403)

    def test_list(self):
        c.login(username='normal_user', password='secret')
        resp = c.get(self.url)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual([obj.pk for obj in resp.context['object_list']], [])


class {{ cookiecutter.model_name }}CreateView(BaseViews):

    def setUp(self):
        self.url = reverse('{{ cookiecutter.app_name }}:{{ cookiecutter.model_name|lower }}_create')
        super({{ cookiecutter.model_name }}CreateView, self).setUp()

    def test_login_required(self):
        resp = c.get(self.url)
        self.assertBasicRedirect(resp, '{}?next={}'.format(settings.LOGIN_URL, reverse('{{ cookiecutter.app_name }}:{{ cookiecutter.model_name|lower }}_create')))

    def test_no_perms(self):
        c.login(username='no_perms_user', password='secret')
        resp = c.get(self.url)
        self.assertEqual(resp.status_code, 403)

    def test_create(self):
        c.login(username='normal_user', password='secret')
        resp = c.get(self.url)
        self.assertEqual(resp.status_code, 200)

        resp = c.post(self.url, {'title': 'Title 1 (created)', 'description': 'Description 1 (created)'})
        {{ cookiecutter.model_name|lower }} = {{ cookiecutter.model_name }}.objects.all().get()
        self.assertBasicRedirect(resp, {{ cookiecutter.model_name|lower }}.get_absolute_url())
        self.assertEqual({{ cookiecutter.model_name|lower }}.title, 'Title 1 (created)')
        self.assertEqual({{ cookiecutter.model_name|lower }}.description, 'Description 1 (created)')

    def test_create_with_empty_form(self):
        c.login(username='normal_user', password='secret')
        resp = c.post(self.url)
        self.assertEqual(resp.status_code, 200)
        self.assertFormError(resp, 'form', 'title', 'This field is required.')
        self.assertFormError(resp, 'form', 'description', 'This field is required.')


class {{ cookiecutter.model_name }}DetailView(BaseViews):

    def setUp(self):
        super({{ cookiecutter.model_name }}DetailView, self).setUp()
        self.{{ cookiecutter.model_name|lower }} = {{ cookiecutter.model_name }}Factory(user=self.normal_user)
        self.url = self.{{cookiecutter.model_name | lower}}.get_absolute_url()

    def test_login_required(self):
        resp = c.get(self.url)
        self.assertBasicRedirect(resp, '{}?next={}'.format(settings.LOGIN_URL, self.url))

    def test_no_perms(self):
        c.login(username='no_perms_user', password='secret')
        resp = c.get(self.url)
        self.assertEqual(resp.status_code, 403)

    def test_owner_required(self):
        c.login(username='wrong_user', password='secret')
        resp = c.get(self.url)
        self.assertEqual(resp.status_code, 403)

    def test_detail(self):
        c.login(username='normal_user', password='secret')
        resp = c.get(self.url)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.context_data['object'].title, self.{{ cookiecutter.model_name|lower }}.title)
        self.assertEqual(resp.context_data['object'].description, self.{{ cookiecutter.model_name|lower }}.description)


class {{ cookiecutter.model_name }}UpdateView(BaseViews):

    def setUp(self):
        super({{ cookiecutter.model_name }}UpdateView, self).setUp()
        self.{{ cookiecutter.model_name|lower }} = {{ cookiecutter.model_name }}Factory(user=self.normal_user)
        self.url = reverse('{{ cookiecutter.app_name }}:{{ cookiecutter.model_name|lower }}_update', kwargs={'pk': self.{{ cookiecutter.model_name|lower }}.pk})

    def test_login_required(self):
        resp = c.get(self.url)
        self.assertBasicRedirect(resp, '{}?next={}'.format(settings.LOGIN_URL, self.url))

    def test_no_perms(self):
        c.login(username='no_perms_user', password='secret')
        resp = c.get(self.url)
        self.assertEqual(resp.status_code, 403)

    def test_owner_required(self):
        c.login(username='wrong_user', password='secret')
        resp = c.get(self.url)
        self.assertEqual(resp.status_code, 403)

    def test_update(self):
        c.login(username='normal_user', password='secret')
        resp = c.get(self.url)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.context_data['object'].title, self.{{ cookiecutter.model_name|lower }}.title)
        self.assertEqual(resp.context_data['object'].description, self.{{ cookiecutter.model_name|lower }}.description)

        resp = c.post(self.url, {'title': 'Title (edited)', 'description': 'Description (edited)'})
        {{ cookiecutter.model_name|lower }} = {{ cookiecutter.model_name }}.objects.get(pk=self.{{ cookiecutter.model_name|lower }}.pk)
        self.assertBasicRedirect(resp, {{ cookiecutter.model_name|lower }}.get_absolute_url())
        self.assertEqual({{ cookiecutter.model_name|lower }}.title, 'Title (edited)')
        self.assertEqual({{ cookiecutter.model_name|lower }}.description, 'Description (edited)')

    def test_update_with_empty_form(self):
        c.login(username='normal_user', password='secret')
        resp = c.post(self.url)
        self.assertEqual(resp.status_code, 200)
        self.assertFormError(resp, 'form', 'title', 'This field is required.')
        self.assertFormError(resp, 'form', 'description', 'This field is required.')


class {{ cookiecutter.model_name }}DeleteView(BaseViews):

    def setUp(self):
        super({{ cookiecutter.model_name }}DeleteView, self).setUp()
        self.{{ cookiecutter.model_name|lower }} = {{ cookiecutter.model_name }}Factory(user=self.normal_user)
        self.url = reverse('{{ cookiecutter.app_name }}:{{ cookiecutter.model_name|lower }}_delete', kwargs={'pk': self.{{ cookiecutter.model_name|lower }}.pk})

    def test_login_required(self):
        resp = c.get(self.url)
        self.assertBasicRedirect(resp, '{}?next={}'.format(settings.LOGIN_URL, self.url))

    def test_no_perms(self):
        c.login(username='no_perms_user', password='secret')
        resp = c.get(self.url)
        self.assertEqual(resp.status_code, 403)

    def test_owner_required(self):
        c.login(username='wrong_user', password='secret')
        resp = c.get(self.url)
        self.assertEqual(resp.status_code, 403)

    def test_delete(self):
        c.login(username='normal_user', password='secret')
        resp = c.get(self.url)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.context_data['object'].title, self.{{ cookiecutter.model_name|lower }}.title)
        self.assertEqual(resp.context_data['object'].description, self.{{ cookiecutter.model_name|lower }}.description)

        c.post(self.url, {})
        {{ cookiecutter.app_name }} = {{ cookiecutter.model_name }}.objects.all()
        self.assertEqual(len({{ cookiecutter.app_name }}), 0)
