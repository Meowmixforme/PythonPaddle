"""Setup script for the pythonpaddle package."""
from setuptools import setup, find_packages

setup(
    name="pythonpaddle",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "pygame>=2.0.0",
    ],
    entry_points={
        'console_scripts': [
            'pythonpaddle=pythonpaddle.main:main',
        ],
    },
)