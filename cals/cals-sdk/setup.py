from setuptools import find_packages, setup

# read in version
__version__ = open('VERSION').read().strip()

# read in requirements.txt
requirements = open('requirements.txt').readlines()
requirements = [r.strip() for r in requirements]

setup(
    name='cals_sdk',
    version=__version__,
    description='The Continual Active Learning System SDK',
    author='Saif Khan',
    packages=find_packages(),
    install_requires=requirements,
)
