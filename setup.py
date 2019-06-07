from setuptools import setup, find_packages

setup(name='meta-analysis',
      version='0.1',
      description='Modules for performing meta-analysis',
      author="Kris Bitney",
      keywords="meta-analysis meta analysis",
      packages=find_packages(),
      install_requires=['numpy>=1.16.3', 'scipy>=1.2.1'])