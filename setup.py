try:
    from setuptools import setup
except ImportError:
    raise ImportError(
        "setuptools module required, please go to https://pypi.python.org/pypi/setuptools and follow the instructions for installing setuptools"
    )


setup(
    name="dedupe-variable-name",
    url="https://github.com/datamade/dedupe-variables-name",
    version="1.0.0",
    description="Name variable type for dedupe",
    packages=["namevariable"],
    install_requires=["probablepeople >= 0.5", "parseratorvariable >= 1.0.0"],
    license="The MIT License: http://www.opensource.org/licenses/mit-license.php",
)
