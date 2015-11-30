#!/usr/bin/env python

from setuptools import setup,find_packages
import os


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

#Dependencies - python eggs
install_requires = [
        'setuptools',
        'Django',
]

setup(name='django-toast-messages',
    version='0.1',
    description='jQuery-powered sexy floating messages',
    long_description=read('README.rst'),
    author='Arpaso',
    author_email='arvid@arpaso.com',
    url='https://github.com/Arpaso/toastmessage',
    download_url='https://github.com/Arpaso/toastmessage/tarball/0.1',
    packages=['toastmessage', ],
    include_package_data = True,    # include everything in source control
    zip_safe=False,
    keywords=['django', 'toastmessage', 'django-toastmessage', 'tag'],
    classifiers = [
        "Programming Language :: Python :: 2",
        "Development Status :: 4 - Beta",
        'Environment :: Web Environment',
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Software Development :: User Interfaces",
        "Framework :: Django",
        ],
)
