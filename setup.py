from setuptools import setup, find_packages

setup(
    name='thought-processor',
    version='0.1.0',
    author='Judith Brener',
    description='TODO',
    packages=find_packages(),
    install_requires=['click', 'flask'],
    tests_require=['pytest', 'pytest-cov'],
)
