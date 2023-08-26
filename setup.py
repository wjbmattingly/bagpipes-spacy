from setuptools import setup, find_packages

setup(
    name="bagpipes-spacy",
    version="0.1.2",
    description="A collection of spaCy components for rules-based detection.",
    long_description=open("README.md", "r", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    author="WJB Mattingly",
    url="https://github.com/wjbmattingly/keyword-spacy",  # replace with the actual URL of your repository
    packages=find_packages(),
    install_requires=[
        "spacy>=3.0",
    ],
    classifiers=[
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",  # adjust this if you are using a different license
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
)
