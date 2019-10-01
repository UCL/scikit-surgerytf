# coding=utf-8
"""
Setup for scikit-surgerytf
"""

from setuptools import setup, find_packages
import versioneer

# Get the long description
with open('README.rst') as f:
    long_description = f.read()

setup(
    name='scikit-surgerytf',
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    description='scikit-surgerytf is a Python package for Tensor Flow examples and utilities',
    long_description=long_description,
    long_description_content_type='text/x-rst',
    url='https://weisslab.cs.ucl.ac.uk/WEISS/SoftwareRepositories/SNAPPY/scikit-surgerytf',
    author='Matt Clarkson',
    author_email='YOUR-EMAIL@ucl.ac.uk',
    license='Apache Software License 2.0',
    classifiers=[
        'Development Status :: 3 - Alpha',

        'Intended Audience :: Developers',
        'Intended Audience :: Healthcare Industry',
        'Intended Audience :: Information Technology',
        'Intended Audience :: Science/Research',


       'License :: OSI Approved :: Apache Software License',


        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',

        'Topic :: Scientific/Engineering :: Information Analysis',
        'Topic :: Scientific/Engineering :: Medical Science Apps.',
    ],

    keywords='medical imaging',

    packages=find_packages(
        exclude=[
            'doc',
            'tests',
        ]
    ),

    install_requires=[
        'six>=1.10',
        'numpy>=1.11',
    ],

    entry_points={
        'console_scripts': [
            'sksurgerytf=sksurgerytf.__main__:main',
        ],
    },
)
