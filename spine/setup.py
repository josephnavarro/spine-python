#!/usr/bin/env python
from setuptools import setup

setup(
    name='spine-python',
    version='1.0b9',
    description='A Pure Python Spine runtime.',
    author='Joey Navarro',
    author_email='therealjoeynavarro@aol.com',
    url='https://github.com/josephnavarro/spine-python/spine',
    package_dir={'spine': 'src'},
    packages=['spine', 'spine.Atlas', 'spine.Animation'],
    classifiers=['License :: OSI Approved :: BSD License']
)
