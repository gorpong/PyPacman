"""Setup configuration for ASCII Pac-Man game."""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="ascii-pacman",
    version="1.0.0",
    author="ASCII Game Studio",
    description="A terminal-based ASCII version of the classic Pac-Man arcade game",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/ascii-pacman",
    packages=find_packages(),
    package_data={
        'ascii_pacman': ['data/*.py'],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Games/Entertainment :: Arcade",
    ],
    python_requires=">=3.8",
    install_requires=[
        # No external dependencies - using only stdlib
    ],
    entry_points={
        "console_scripts": [
            "ascii-pacman=ascii_pacman.main:main",
        ],
    },
)
