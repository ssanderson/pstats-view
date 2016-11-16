from __future__ import print_function

import sys
from distutils.version import StrictVersion
from setuptools import setup

MIN_PIP_VERSION = StrictVersion('7.1.0')


setup(
    name='pstats-view',
    version='0.1',
    description='A Graphical Viewer for CProfile Output',
    author='Scott Sanderson',
    author_email='scoutoss@gmail.com',
    packages=['pstatsviewer'],
    license='Apache 2.0',
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        'Framework :: IPython',
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: Apache Software License',
        'Natural Language :: English',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
        'Operating System :: OS Independent',
        'Intended Audience :: Science/Research',
        'Topic :: Office/Business :: Financial',
        'Topic :: Scientific/Engineering :: Information Analysis',
    ],
    install_requires=[
        'notebook',
        'qgrid>=0.3.1',
        'seaborn',
    ],
    url="https://github.com/ssanderson/pstats-view"
)
