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
    - [Quote Detector](#quote-detector)
    - [Phrases Extractor](#phrases-extractor)
    - [Normalizer](#normalizer)
    - [Triple Detector](#triple-detector)
    - [Entity Similarity](#entity-similarity)
    - [Sentence Cluster](#sentence-cluster)
    - [Token Cluster](#token-cluster)
    - [Entity Cluster](#entity-cluster)
    - [Keyword Extractor](#keyword-extractor)

## Installation

To install Bagpipes spaCy, execute:

```sh
pip install bagpipes-spacy
```

## Usage

After installation, you can add any of the Bagpipes spaCy components to your spaCy pipeline using the `add_pipe` method. There's no need to import the components individually.

### Quote Detector

```python
import spacy

nlp = spacy.blank("en")
nlp.add_pipe("quote_detector")

text = """
"I... oh ... very well," said the Prime Minister weakly. "Yes, I'll see Fudge."
He hurried back to his desk, straightening his tie as he went. He had barely resumed his seat, and arranged his face into what he hoped was a relaxed and unfazed expression, when bright green flames burst into life in the empty grate beneath his marble mantelpiece.
"""

doc = nlp(text)
for quote in doc._.quotes:
    print(quote)
```

### Phrases Extractor

```python
import spacy

nlp = spacy.load("en_core_web_md")
nlp.add_pipe("phrases_extractor")

text = """Seconds later, he had climbed out onto a rather fine antique rug, brushing ash from the sleeves of his long pin-striped cloak, a lime-green bowler hat in his hand."""

doc = nlp(text)

print("Prepositional Phrases:", doc._.prep_phrases)
print("Noun Phrases:", doc._.noun_phrases)
print("Verb Phrases:", doc._.verb_phrases)
print("Adj Phrases:", doc._.adj_phrases)
```

### Normalizer

```python
nlp.add_pipe('normalizer', first=True)
```

### Triple Detector

```python
nlp.add_pipe('triple_detector')
```

### Entity Similarity

```python
nlp.add_pipe('entity_similarity')
```

### Sentence Cluster

```python
nlp = spacy.load("en_core_web_lg")
nlp.add_pipe("sentence_cluster", config={"threshold": 0.8})

text = "Microsoft is a company. Twitter is another company. Tiger Woods is an athlete. Michael Jordan is an athlete."
doc = nlp(text)
print(doc._.sent_cluster)
```

### Token Cluster

```python
nlp = spacy.load("en_core_web_lg")
nlp.add_pipe("token_cluster", config={"threshold": 0.4})

doc = nlp(text)
print(doc._.token_cluster)
```

### Entity Cluster

```python
nlp = spacy.load("en_core_web_lg")
nlp.add_pipe("entity_cluster", config={"threshold": 0.3})

doc = nlp(text)
print(doc._.ent_cluster)
```

### Keyword Extractor

The `keyword_extractor` component can be configured with the following parameters:
- `top_n`: The number of top keywords to extract for the entire document.
- `min_ngram`: The minimum size for n-grams.
- `max_ngram`: The maximum size for n-grams.
- `strict`: If set to `True`, only n-grams within the `min_ngram` to `max_ngram` range are considered.
- `top_n_sent`: The number of top keywords to extract for each sentence.

```python
import spacy

nlp = spacy.load("en_core_web_lg")
nlp.add_pipe("keyword_extractor", last=True, config={"top_n": 10, "min_ngram": 1, "max_ngram": 3, "strict": True, "top_n_sent": 3})

text = "Natural language processing is a fascinating domain of artificial intelligence. It allows computers to understand and generate human language."
doc = nlp(text)
print("Top Document Keywords:", doc._.keywords)
for sent in doc.sents:
    print(f"Sentence: {sent.text}")
    print("Top Sentence Keywords:", sent._.sent_keywords)
```