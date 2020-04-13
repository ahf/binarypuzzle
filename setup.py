#!/usr/bin/env python3

from setuptools import find_packages, setup

if __name__ == "__main__":
    setup(
        name="binarypuzzle",
        version="0.0.1",
        license="BSD-2-Clause",
        description="",
        author="Alexander Færøy",
        author_email="ahf@0x90.dk",
        url="https://github.com/ahf/binarypuzzle",
        packages=find_packages("src"),
        package_dir={"": "src"},
        install_requires=["z3-solver"],
        tests_require=[],
        classifiers=[],
    )
