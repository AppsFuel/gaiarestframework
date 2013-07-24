from setuptools import setup, find_packages
import sys
import os

wd = os.path.dirname(os.path.abspath(__file__))
os.chdir(wd)
sys.path.insert(1, wd)

name = 'gaiarestframework'
pkg = __import__('gaiarestframework')

author, email = 'Andrea De Marco', 'andrea.demarco@buongiorno.com'

version = '0.4.5'
classifiers = [
    'Development Status :: 4 - Beta',
    'Framework :: Django',
    'Intended Audience :: Developers',
    'Operating System :: OS Independent',
    'Topic :: Internet :: WWW/HTTP',
    'Topic :: Software Development :: Libraries',
]

readme = open(os.path.join(wd, 'README.rst'),'r').readlines()
description = readme[1]
long_description = ''.join(readme)

try:
    reqs = open(os.path.join(os.path.dirname(__file__), 'requirements.txt')).read()
except (IOError, OSError):
    reqs = ''

setup(
    name=name,
    version=version,
    author=author,
    author_email=email,
    maintainer=author,
    maintainer_email=email,
    description=description,
    long_description=long_description,
    classifiers=classifiers,
    install_requires=reqs,
    packages=find_packages(exclude=('example', 'example.*',)),
    include_package_data=True,
)
