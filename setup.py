try:
    from setuptools import setup
except ImportError :
    raise ImportError("setuptools module required, please go to https://pypi.python.org/pypi/setuptools and follow the instructions for installing setuptools")


setup(
    name='dedupe-variable-name',
    url='https://github.com/dedupeio/dedupe-variable-name',
    version='0.0.14',
    description='Name variable type for dedupe',
    packages=['dedupe.variables'],
    install_requires=['probablepeople >= 0.5', 
                      'parseratorvariable >= 0.0.18',
                      'future'],
    license='The MIT License: http://www.opensource.org/licenses/mit-license.php'
    )
