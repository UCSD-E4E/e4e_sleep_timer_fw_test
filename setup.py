from setuptools import setup, find_packages

setup(
    name='examplePackage',
    version='0.0.0.1',
    author='UCSD Engineers for Exploration',
    author_email='e4e@eng.ucsd.edu',
    entry_points={
        
    },
    packages=find_packages(),
    install_requires=[
        'pyserial',
        'pytest',
    ]
)