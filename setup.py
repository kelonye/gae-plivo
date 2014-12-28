#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
    name='gae-plivo',
    version='0.0.2',
    description='Pesapal NDB Model',
    author='Mitchel Kelonye',
    author_email='kelonyemitchel@gmail.com',
    url='https://github.com/kelonye/gae-plivo',
    packages=['gae_plivo',],
    package_dir = {'gae_plivo': 'lib'},
    license='MIT',
    zip_safe=True
)