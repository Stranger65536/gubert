"""
Setup script
"""
from pathlib import Path

from setuptools import setup, find_packages

# The directory containing this file
HERE = Path(__file__).parent
INSTALL_REQUIRES = (HERE / "requirements.txt").read_text().splitlines()

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="gubert",
    version="0.0.3",
    description="Read the latest Real Python tutorials",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/Stranger65536/gubert",
    author="Stranger65536",
    author_email="stranger.65536@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: GNU Affero General "
        "Public License v3 or later (AGPLv3+)",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
    ],
    packages=find_packages(),
    include_package_data=True,
    python_requires='>=3.6',
    install_requires=INSTALL_REQUIRES,
    entry_points={
        "console_scripts": [
            "gubert=gubert.__main__:main",
        ]
    },
)
