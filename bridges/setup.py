#!/usr/bin/env python3
"""
SpiralSafe Hardware Integration Bridges
Setup script for pip installation
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read README for long description
readme_file = Path(__file__).parent / "README.md"
long_description = readme_file.read_text(encoding="utf-8") if readme_file.exists() else ""

setup(
    name="spiralsafe-bridges",
    version="0.1.0",
    description="Hardware integration bridges for SpiralSafe ecosystem (ATOM trail, Hologram, Tartarus Pro)",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Hope&&Sauced Collaborative",
    author_email="",
    url="https://github.com/toolate28/SpiralSafe",
    project_urls={
        "Documentation": "https://github.com/toolate28/SpiralSafe/blob/main/bridges/README.md",
        "Source": "https://github.com/toolate28/SpiralSafe",
        "Tracker": "https://github.com/toolate28/SpiralSafe/issues",
    },
    license="MIT",
    packages=find_packages(exclude=["tests", "tests.*"]),
    python_requires=">=3.10",
    install_requires=[
        "aiofiles>=23.0.0",
        "watchdog>=3.0.0",
        "Pillow>=10.0.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0",
            "pytest-asyncio>=0.21.0",
            "pytest-cov>=4.0",
            "hypothesis>=6.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "spiralsafe-atom=atom.atom_trail:main",
            "spiralsafe-hologram=hologram.hologram_device:main",
            "spiralsafe-tartarus=tartarus.tartarus_device:main",
            "spiralsafe-validate=validate_implementation:main",
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Software Development :: Libraries",
        "Topic :: System :: Hardware",
    ],
    keywords="spiralsafe atom hologram tartarus hardware bridge async",
    include_package_data=True,
    zip_safe=False,
)
