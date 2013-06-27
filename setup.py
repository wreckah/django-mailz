from setuptools import setup, find_packages

setup(
    name='django-mailz',
    version='0.1',
    description='Autoresponder and sending emails queuing by django-celery.',
    long_description='',
    author='Alexander Pokatilov',
    author_email='wreckah@ya.ru',
    package_dir = {'': 'django_mailz'},
    packages = find_packages('django_mailz'),
    install_requires = ['django-celery'],
)
