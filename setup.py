#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
    name='decker',
    version='0.0.1',
    description='TTS deck builder',
    author='Doug Black',
    author_email='doug@dougblack.io',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'certifi==2015.9.6.2',
        'requests>=2.8.1',
        'flask',
        'Flask-RESTful',
        'Pillow',
    ],
)
