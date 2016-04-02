from __future__ import unicode_literals

import re

from setuptools import find_packages, setup


def get_version(filename):
    with open(filename) as fh:
        metadata = dict(re.findall("__([a-z]+)__ = '([^']+)'", fh.read()))
        return metadata['version']


setup(
    name='Mopidy-AVCNTRL',
    version=get_version('mopidy_avcntrl/__init__.py'),
    url='https://github.com/axelv/mopidy-avcntrl',
    license='Apache License, Version 2.0',
    author='Axel Vanraes',
    author_email='axelvanraes@gmail.com',
    description='"Mopidy extension that interfaces knobs, rotarycontrols, touchpads to the Mopidy Core.',
    long_description=open('README.rst').read(),
    packages=find_packages(exclude=['tests', 'tests.*']),
    zip_safe=False,
    include_package_data=True,
    install_requires=[
        'setuptools',
        'Mopidy >= 1.0',
        'Pykka >= 1.1',
    ],
    entry_points={
        'mopidy.ext': [
            'avcntrl = mopidy_avcntrl:Extension',
        ],
    },
    classifiers=[
        'Environment :: No Input/Output (Daemon)',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        'Topic :: Multimedia :: Sound/Audio :: Players',
    ],
)
