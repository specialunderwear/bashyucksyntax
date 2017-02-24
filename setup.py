"""
This this thing give you a command called ``dryfab``, you can use instead of
fab.

If use ``dryfab``, it will just show the commands fabric would run instead of
executing them. So go ahead, pipe that to a file and never write anymore bash
script ahhahaha.
"""

from setuptools import setup, find_packages


__version__ = "0.0.1"


setup(
    # package name in pypi
    name='bashyucksyntax',
    # extract version from module.
    version=__version__,
    description="Add --dry-run to fabric",
    long_description=__doc__,
    classifiers=[],
    keywords='yuck fabric deploy bash',
    author='Lars van de Kerkhof',
    author_email='yuck@permanentmarkers.nl',
    url='https://github.com/specialunderwear/bashyucksyntax',
    license='GPL v3',
    # include all packages in the egg, except the test package.
    packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
    # include non python files
    include_package_data=True,
    zip_safe=False,
    # specify dependencies
    install_requires=[
        'setuptools',
        'fabric'
    ],
    # mark test target to require extras.
    extras_require = {
        'test':  ["mock"]
    },
    # generate scripts
    entry_points={
        'console_scripts':[
            'dryfab = bashyucksyntax.main:main',
        ]
    }
)
