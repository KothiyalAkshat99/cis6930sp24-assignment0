from setuptools import setup, find_packages

setup(
	name='assignment0',
	version='2.0',
	author='Akshat Kothiyal',
	author_email='kothiyalakshat@ufl.edu',
	packages=find_packages(exclude=('tests', 'docs', 'resources')),
	setup_requires=['pytest-runner'],
	tests_require=['pytest']	
)