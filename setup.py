#!/usr/bin/env python

from setuptools import setup
import os

long_description = """
pyEdgeworthBox calculates equilibrium, core, pareto effective allocation etc in the pure exchange economy, plots Edgeworth box (microeconomics)
"""

setup(
    name='pyEdgeworthBox',
    version = os.environ.get('CI_COMMIT_TAG', '0.0.0-dev'),
    description='Python Library to draw the Edgeworth box and calculate equilibrium, core, pareto efficient allocations etc',
    long_description=long_description,  # Include the long description
    long_description_content_type='text/plain',  # Specify the content type, can be 'text/markdown' for Markdown
    author='Maxim Litvak',
    author_email='maxim@litvak.eu',
    url='https://gitlab.com/maxlit/pyEdgeworthBox',
    test_suite='test',
    packages=['pyEdgeworthBox'],
    classifiers=[
        # Your classifiers
    ],
)