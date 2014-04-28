Cookiecutter Django Basic App
=============================

A cookiecutter template to create a Django app within an existing Django project, with a boilerplate that includes:
    * A barebones Django model.
    * Django CRUD views and templates using Django's Class Based Views.
    * Django form templates that output `Bootstrap <http://getbootstrap.com/>`_ HTML using `django-bootstrap-form <https://github.com/tzangms/django-bootstrap-form>`_.
    * Tests for all of the views.
    * Model instances generated using `factory boy <https://github.com/rbarrois/factory_boy>`_ for the tests.

Quickstart
==========

1. Install `cookiecutter <https://github.com/audreyr/cookiecutter>`_, and the apps listed in requirements.txt.  Install them all with:

.. code-block:: console

    pip install -r https://raw.github.com/epicserve/cookiecutter-django-basic-app/master/requirements.txt


2. Run cookiecutter using this template.  Note that **it will overwrite existing files without warning if you already have an app dir of the same name**, so make sure your code is checked in or backed up.

.. code-block:: console

    cookiecutter git@github.com:epicserve/cookiecutter-django-basic-app.git


3. You'll need to add ``bootstrapform``, to your INSTALLED_APPS, along with your new app:

.. code-block:: python

    INSTALLED_APPS = (
        ...
        'bootstrapform',
        '{{ cookiecutter.app_name }}',
    )

4. And don't forget to hook up your urls.py:

.. code-block:: python

    url(r'^{{ cookiecutter.app_name }}/', include('{{ cookiecutter.app_name }}.urls', namespace='{{ cookiecutter.app_name }}')),


5. Run your newly created tests:

.. code-block:: console

    python manage.py test new-app-name


Feel free to fork and make it your own, or send anything back up which you think may be generally useful.