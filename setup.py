from distutils.core import setup
from setuptools import find_packages

setup(
    name="cake-cutting",
    version="1.0",
    packages=find_packages(
        exclude=(
            "cake_cutting.test"
        )
    )
)