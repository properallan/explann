from setuptools import setup

with open('requirements/main.txt') as f:
    requirements = f.read().splitlines()

setup(
    name='explann',
    version='0.0.1',
    description='EXperimental PLANNing python package for factorial design of experiments',
    author='Allan Moreira de Carvalho',
    author_email='properallan@gmail.com',
    packages=['explann'],
    install_requires= requirements,
)