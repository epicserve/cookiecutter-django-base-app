from django import forms
from .models import {{ cookiecutter.model_name }}


class {{ cookiecutter.model_name }}Form(forms.ModelForm):

    class Meta:
        model = {{ cookiecutter.model_name }}
        fields = ('title', 'description')

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super({{ cookiecutter.model_name }}Form, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        if not self.instance.pk:
            self.instance.user = self.user
        self.instance = super({{ cookiecutter.model_name }}Form, self).save()

        return self.instance
