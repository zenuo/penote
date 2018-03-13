# -*- coding: utf-8 -*-

# Learn more: https://github.com/kennethreitz/setup.py

from setuptools import setup, find_packages

with open('README') as f:
    readme = f.read()

setup(
    name='penote',
    version='0.1.0',
    description='一个简单的手写体博客',
    long_description=readme,
    author='Yuan Zhen',
    author_email='zenuor@gmail.com',
    url='https://code.aliyun.com/yuanzhen/penote.git',
    license=license,
    packages=find_packages(exclude=('tests', 'docs'))
)
