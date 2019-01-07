# -*- coding: utf-8 -*-

from setuptools import setup, find_packages


with open('README.md') as readme_fd:
    readme = readme_fd.read()

requires = [
    'selenium>=3.14'
]

setup(
    name='pageman',
    version='0.1',
    description='Page object model',
    long_description=readme,
    author='Reed Yeh',
    author_email='reed_yeh@trendmicro.com',
    url='',
    packages=find_packages(exclude=('tests', 'poc')),
    install_requires=requires,
)
