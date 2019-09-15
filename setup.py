#!/usr/bin/env python

from setuptools import setup

readme = open('README.rst').read()

requirements = [
    'pytest>=2.3' 
]

setup(
    name='pytest-test-this',
    version='0.3.0',
    description='Plugin for py.test to run relevant tests, based on naively checking if a test contains a reference to the symbol you supply',
    long_description=readme + '\n',
    author='Anders Hovmöller',
    author_email='boxed@killingar.net',
    url='https://github.com/boxed/pytest-test-this',
    py_modules=['pytest_test_this'],
    entry_points={'pytest11': ['pycharm = pytest_test_this']},
    include_package_data=True,
    install_requires=requirements,
    license="BSD",
    zip_safe=False,
    keywords='pytest,py.test,pycharm',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Operating System :: POSIX',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: MacOS :: MacOS X',
        'Topic :: Software Development :: Testing',
        'Topic :: Software Development :: Libraries',
        'Topic :: Utilities',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        "Framework :: Pytest"
    ],
)
