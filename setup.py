import os
from setuptools import setup, find_packages

f = open(os.path.join(os.path.dirname(__file__), 'README.md'))
readme = f.read()
f.close()

setup(
    name='django-scout',
    version='0.1-alpha',
    description='A django app that provides a production site monitoring wall.',
    long_description=readme,
    author='Darian Moody, Alfredo Aguirre, The Team',
    author_email='mail@djm.org.uk',
    url='https://github.com/theteam/django-scout',
    packages=find_packages(exclude=['tests']),
    include_package_data=True,
    install_requires=['requests>=0.4',
                      'lockfile>=0.9.1'],
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Framework :: Django',
        ],
    #test_suite='contextual.tests.run_tests.run_tests',
)
