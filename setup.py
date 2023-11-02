import io

import setuptools

from pathlib import Path

this_directory = Path(__file__).parent
long_description = this_directory.joinpath("README.md").read_text()


def _get_requirements():
    """Relax dependencies tha have been hard pinned in requirements.txt"""
    with io.open("requirements.txt", encoding="utf-8") as requirements:
        return [line.replace("==", ">=") for line in requirements.readlines()]


setuptools.setup(
    name="font-finder",
    version="0.1.0",
    description="A helper library for finding TTFont objects in a directory.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="ftCLI",
    author_email="ftCLI@proton.me",
    url="https://github.com/ftCLI/FontFinder",
    packages=setuptools.find_packages(),
    include_package_data=True,
    install_requires=_get_requirements(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    zip_safe=False,
)
