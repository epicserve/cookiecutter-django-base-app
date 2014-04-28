from django.contrib import admin
from .models import {{ cookiecutter.model_name }}


class {{ cookiecutter.model_name }}Admin(admin.ModelAdmin):
    list_display = ('title', )
    search_fields = ('title', )
admin.site.register({{ cookiecutter.model_name }}, {{ cookiecutter.model_name }}Admin)
