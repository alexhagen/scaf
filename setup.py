"""Setup for scaf."""
#!/usr/bin/env python
from setuptools import setup, find_packages
from setuptools.command.develop import develop
from setuptools.command.install import install

class PreDevelopCommand(develop):
      def run(self):
            requirements = []
            with open('requirements.txt', 'r') as f:
                  requirements = f.read().split()
            dev_requirements = []
            with open('dev_requirements.txt', 'r') as f:
                  dev_requirements = f.read().split()
            requirements.extend(dev_requirements)
            for req in requirements:
                  self.easy_install(req, deps=True)
            super().run()

class PreInstallCommand(install):
      def run(self):
            requirements = []
            with open('requirements.txt', 'r') as f:
                  requirements = f.read().split()
            for req in requirements:
                  self.easy_install(req, deps=True)
            super().run()

setup(name='scaf',
      version=0.1,
      description='Scaffolding for accelerating computational work',
      author='Alex Hagen',
      author_email='alexhagen6@gmail.com',
      url='https://github.com/alexhagen/scaf',
      long_description=open('README.md').read(),
      packages=find_packages(),
      scripts=['bin/scaf'],
      cmdclass=dict(develop=PreDevelopCommand, install=PreInstallCommand),
     )