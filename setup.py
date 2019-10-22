#!/usr/bin/env python3


import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

with open('VERSION', 'r') as v:
    version = v.read()

with open('requirements.txt') as f:
    required = f.read().splitlines()

setuptools.setup(
    name="HSTools",
    version=version,
    author="Anthony M. Castronova",
    author_email="acastronova@cuahsi.org",
    description="A humble collection of HydroShare tools written in Python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/castronova/hstools",
    packages=setuptools.find_packages(),
    install_requires=required,
    py_modules=['hstools'],
    scripts=['bin/hs'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
        "Natural Language :: English",
        "Topic :: Scientific/Engineering :: Hydrology",
    ],
    python_requires='>=3.6',
)
