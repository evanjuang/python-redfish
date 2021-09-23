import os
from setuptools import setup, find_packages


INSTALL_REQUIRES = [
    "Click>=7.0",
    "request",
    "PyYAML"
]

about = {}
with open(os.path.join(os.path.dirname(__file__), 'redfishtool', '__about__.py'), 'r') as f:
    exec(f.read(), about)

setup(
    name='redfishtool',
    version=about['__version__'],
    packages=find_packages(),
    include_package_data=True,
    install_requires=INSTALL_REQUIRES,
    entry_points={
        'console_scripts': [
            'redfishtool = redfishtool.__main__:main']
    }
)
