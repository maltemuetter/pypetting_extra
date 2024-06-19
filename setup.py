from setuptools import setup, find_packages

setup(
    name="pypetting-extra",  # This should match the folder name
    version="0.1.0",
    author="Malte Muetter",
    author_email="malte.muetter@env.ethz.ch",
    description="This package builds on the pypetting package and facilitates convinent handling of the Evo 200 automated liquid handling system (Tecan)",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/your_repo",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.9",
    install_requires=["pypetting>=0.7.0", "pandas>=2.1.4", "numpy>=1.26.4"],
)
