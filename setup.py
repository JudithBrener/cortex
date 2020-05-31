from setuptools import setup, find_packages

setup(
    name='thought-processor',
    version='0.1.0',
    author='Judith Brener',
    description='Project for Advanced System Design course in Tel-Aviv university taught by Dan Gittik.',
    packages=find_packages(),
    install_requires=['click', 'flask'],
    tests_require=['pytest', 'pytest-cov'],
)
