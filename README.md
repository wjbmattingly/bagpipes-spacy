[![GitHub Stars](https://img.shields.io/github/stars/wjbmattingly/bagpipes-spacy?style=social)](https://github.com/wjbmattingly/bagpipes-spacy)
[![PyPi Version](https://img.shields.io/pypi/v/bagpipes-spacy)](https://pypi.org/project/bagpipes-spacy/0.0.1/)
[![PyPi Downloads](https://img.shields.io/pypi/dm/bagpipes-spacy)](https://pypi.org/project/bagpipes-spacy/0.0.1/)

# Bagpipes spaCy

![bagpipes spacy logo](https://github.com/wjbmattingly/bagpipes-spacy/blob/main/images/bagpipes-spacy-logo.png?raw=true)


Bagpipes spaCy is a collection of custom spaCy pipeline components designed to enhance text processing capabilities. These components include:

1. **Quote Detector**: Identifies and extracts quotes from the text.
2. **Phrases Extractor**: Extracts various types of phrases such as prepositional, noun, verb, adjective, and adverbial phrases.
3. **Normalizer**: Normalizes the text by expanding contractions, removing special characters, and more.
4. **Triple Detector**: Extracts triples (subject, predicate, object) from the text.
5. **Entity Similarity**: Computes similarity between entities in the text and maps similar entities.
6. **Entity Cluster**: Groups entities in the text into clusters based on similarity.
7. **Sentence Cluster**: Groups sentences in the text into clusters based on similarity.
8. **Token Cluster**: Groups tokens in the text into clusters based on similarity.
9. **Keyword Extractor**: Extracts keywords from the text based on cosine similarity with the entire text or sentence.

## Table of Contents
- [Bagpipes spaCy](#bagpipes-spacy)
  - [Table of Contents](#table-of-contents)
  - [Installation](#installation)
  - [Usage](#usage)
    - [Integrating the Quote Detector](#integrating-the-quote-detector)
    - [Integrating the Phrases Extractor](#integrating-the-phrases-extractor)
    - [Integrating the Normalizer](#integrating-the-normalizer)
    - [Integrating the Triple Detector](#integrating-the-triple-detector)
    - [Integrating the Entity Similarity](#integrating-the-entity-similarity)
    - [Integrating the Entity Cluster](#integrating-the-entity-cluster)
    - [Integrating the Sentence Cluster](#integrating-the-sentence-cluster)
    - [Integrating the Token Cluster](#integrating-the-token-cluster)
    - [Integrating the Keyword Extractor](#integrating-the-keyword-extractor)

## Installation

To install Bagpipes spaCy, execute:

```sh
pip install bagpipes-spacy
```

## Usage

### Integrating the Quote Detector

Import the `QuoteDetector` and integrate it into your spaCy pipeline:

```python
import spacy
from bagpipes_spacy import QuoteDetector

# Initialize your preferred spaCy model
nlp = spacy.load('en_core_web_md')

# Integrate the component into the pipeline
nlp.add_pipe('quote_detector')
```

### Integrating the Phrases Extractor

Import the `PhrasesExtractor` and integrate it into your spaCy pipeline:

```python
from bagpipes_spacy import PhrasesExtractor

# Integrate the component into the pipeline
nlp.add_pipe('phrases_extractor')
```

### Integrating the Normalizer

Import the `Normalizer` and integrate it into your spaCy pipeline:

```python
from bagpipes_spacy import Normalizer

# Integrate the component into the pipeline
nlp.add_pipe('normalizer', first=True)
```

### Integrating the Triple Detector

Import the `TripleDetector` and integrate it into your spaCy pipeline:

```python
from bagpipes_spacy import TripleDetector

# Integrate the component into the pipeline
nlp.add_pipe('triple_detector')
```

### Integrating the Entity Similarity

Import the `EntitySimilarity` and integrate it into your spaCy pipeline:

```python
from bagpipes_spacy import EntitySimilarity

# Integrate the component into the pipeline
nlp.add_pipe('entity_similarity')
```

### Integrating the Entity Cluster

Import the `EntityCluster` and integrate it into your spaCy pipeline:

```python
from bagpipes_spacy import EntityCluster

# Integrate the component into the pipeline
nlp.add_pipe('entity_cluster')
```

### Integrating the Sentence Cluster

Import the `SentenceCluster` and integrate it into your spaCy pipeline:

```python
from bagpipes_spacy import SentenceCluster

# Integrate the component into the pipeline
nlp.add_pipe('sentence_cluster')
```

### Integrating the Token Cluster

Import the `TokenCluster` and integrate it into your spaCy pipeline:

```python
from bagpipes_spacy import TokenCluster

# Integrate the component into the pipeline
nlp.add_pipe('token_cluster')
```

### Integrating the Keyword Extractor

Import the `KeywordExtractor` and integrate it into your spaCy pipeline:

```python
from bagpipes_spacy import KeywordExtractor

# Integrate the component into the pipeline
nlp.add_pipe('keyword_extractor', last=True, config={"top_n": 10, "min_ngram": 1, "max_ngram": 3, "strict": True, "top_n_sent": 3})
```