from setuptools import setup, find_packages
import os

# Read the contents of your README file
with open(os.path.join(os.path.dirname(__file__), 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name="bagpipes-spacy",
    version="0.1.4",
    description="A collection of spaCy components for rules-based detection and extraction.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="WJB Mattingly",
    url="https://github.com/wjbmattingly/bagpipes-spacy",
    packages=find_packages(),
    install_requires=[
        "spacy>=3.0",
    ],
    entry_points={
        "spacy_factories": [
            "normalizer = bagpipes_spacy.normalizers:Normalizer",
            "triple_detector = bagpipes_spacy.knowledge:TripleDetector",
            "entity_similarity = bagpipes_spacy.knowledge:EntitySimilarity",
            "entity_cluster = bagpipes_spacy.knowledge:EntityCluster",
            "sentence_cluster = bagpipes_spacy.knowledge:SentenceCluster",
            "token_cluster = bagpipes_spacy.knowledge:TokenCluster",
            "keyword_extractor = bagpipes_spacy.knowledge:KeywordExtractor",
            "quote_detector = bagpipes_spacy.phrases:QuoteDetector",
            "phrases_extractor = bagpipes_spacy.phrases:PhrasesExtractor",
        ]
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
    python_requires='>=3.7',
)