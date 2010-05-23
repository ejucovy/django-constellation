from setuptools import setup, find_packages
import sys, os

version = '0.1'

setup(name='django-constellation',
      version=version,
      description="django administrative interface to planet, and a planet farm, with some social features",
      long_description="""\
""",
      classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='planet news river feed stream social collaboration',
      author='Ethan Jucovy',
      author_email='ejucovy@gmail.com',
      url='http://constellation.socialplanning.org',
      license='GPLv3',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=False,
      install_requires=[
        "planet",
        "djangohelpers",
        ],
      dependency_links=[
        "http://www.planetplanet.org/download/planet-2.0.tar.bz2#egg=planet"
        ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
