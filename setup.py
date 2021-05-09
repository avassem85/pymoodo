import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pymoodo",
    version="0.0.3",
    author="Alex van Assem",
    author_email="avassem@gmail.com",
    description="Python client to communicate with Moodo API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/avassem85/pymoodo",
    packages=setuptools.find_packages(),
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
)