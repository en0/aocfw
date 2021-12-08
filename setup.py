from setuptools import setup


with open("README.md", "r") as fh:
    long_description = fh.read()


setup(
    name="aocfw",
    version="1.0.1",
    description="Advent Of Code Python Framework",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Ian Laird",
    author_email="irlaird@gmail.com",
    url="https://github.com/en0/aocfw",
    packages=["aocfw"],
    install_requires=["pyioc3", "requests"],
    entry_points={"console_scripts": ['aocfw=aocfw.cli.entry:main']},
    classifiers=[
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
