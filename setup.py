from setuptools import setup, find_packages

setup(name="avalonplex-core",
      version="1.0.3",
      author="Avalon Plex",
      url="https://github.com/AvalonPlex/avalonplex-core",
      python_requires=">=3.6",
      packages=find_packages(exclude=["tests"]))
