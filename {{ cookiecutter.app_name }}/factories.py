import factory
from . import models


class {{ cookiecutter.model_name }}Factory(factory.DjangoModelFactory):
    FACTORY_FOR = models.{{ cookiecutter.model_name }}

    title = factory.Sequence(lambda n: 'Title {0}'.format(n))
    description = factory.Sequence(lambda n: 'Description {0}'.format(n))
