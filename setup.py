from setuptools import setup, find_packages
import sys, os

version = '0.1'

setup(name='pyC14',
      version=version,
      description="pyC14 is a radiocarbon (14C) calibration and plotting program",
      long_description="""\
""",
      classifiers=[
        'Development Status :: 2 - Alpha',
        'Environment :: Console',
        'Intended Audience :: Science/Research',
        'License :: GNU General Public License (GPL)',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Scientific/Engineering',
        ],
      keywords='radiocarbon calibration oxcal',
      author='Christophe Le Bourlot',
      author_email='Christophe.Le-Bourlot@INSA-Lyon.Fr',
      url='https://github.com/AlephThot/pyC14',
      license='GNU GPLv3',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      package_data={'pyC14': ['data/*.14c']},
      include_package_data=True,
      zip_safe=False,
      #install_requires=[
         ## -*- Extra requirements: -*-
        #'numpy >= 1.2.0',
        #'matplotlib >= 0.98.5',
        #'scipy >= 0.6.0'
      #],
      #entry_points= {
        #'console_scripts': [
            #'iosacal = iosacal.cli:main',
            #]
        #},
      )
