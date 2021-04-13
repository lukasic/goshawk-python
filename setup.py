from os.path import join as path_join, dirname
from setuptools import setup, find_packages

version = '0.1'

with open("README.md", "r") as f:
    long_description = f.read()

with open("requirements.txt", "r") as f:
    install_reqs = f.read().split()

setup(
    name='goshawk',
    version=version,
    description=('Goshawk python libraries.'),
    long_description=long_description,
    author='Lukas Kasic',
    author_email='src@lksc.sk',
    url='https://github.com/lukasic/goshawk-python',
    packages=find_packages(),
    install_requires = install_reqs,
    keywords=['goshawk', "blocklist", "allowlist"],
    classifiers=[
        'Development Status :: 1 - Planning',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
    ],
)
