try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

with open('README') as file:
    long_description = file.read()

setup(
    name='quora',
    version='0.1.22',
    description='Fetches and parses data from Quora.',
    long_description=long_description,
    author='Christopher Su',
    author_email='chris+py@christopher.su',
    url='https://github.com/csu/pyquora',
    packages=['quora'],
    install_requires=[
        "beautifulsoup4 == 4.3.2",
        "feedparser == 5.1.3",
        "requests == 2.20.0"
    ]
)