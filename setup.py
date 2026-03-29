
import os
import sys
import setuptools

physicsLab_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "physicsLab")
sys.path.append(physicsLab_dir)

import version as v

setuptools.setup(
    name="physicsLab",
    version=str(v.__version__),
    license="MIT",
    author="Arendelle",
    author_email="Arendelle_@outlook.com",
    description="Python API for Quantum-Physics App",
    long_description="show description in [github](https://github.com/SekaiArendelle/physicsLab)",
    long_description_content_type="text/markdown",
    url="https://github.com/SekaiArendelle/physicsLab",
    packages=setuptools.find_packages(include=["physicsLab", "physicsLab.*"]),
    install_requires=["typing-extensions", "requests"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: Chinese (Simplified)",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
)
