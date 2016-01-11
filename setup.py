import os

try:
    from setuptools import setup
except ImportError:
    from distutils import setup

long_description = open(os.path.join(os.path.dirname(__file__), "README.rst")).read()

setup(
    name="org.cttv.input.validation",
    version="0.1.1",
    description=long_description.split("\n")[0],
    long_description=long_description,
    author="Gautier Koscielny",
    author_email="gautier.x.koscielny@gsk.com",
    url="https://github.com/CTTV",
    #packages=find_packages('.'),
    #package_dir = {'': '.'},
    #namespace_packages = ["org", "org.cttv", "org.cttv.input"],    
    packages=["org.cttv.input.validation"],
    license="Apache2",
    classifiers=[
        "License :: Apache 2",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
    ],
)

