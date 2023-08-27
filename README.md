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
    - [Sentence Cluster](#sentence-cluster)
    - [Token Cluster](#token-cluster)
    - [Entity Cluster](#entity-cluster)
    - [Keyword Extractor](#keyword-extractor)
      - [Configuration](#configuration)

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

### Sentence Cluster

The `sentence_cluster` component groups sentences in the text into clusters based on similarity.

```python
import spacy
from bagpipes_spacy import SentenceCluster

nlp = spacy.load("en_core_web_lg")
nlp.add_pipe("sentence_cluster", config={"threshold": 0.8})

text = "Microsoft is a company. Twitter is another company. Tiger Woods is an athlete. Michael Jordan is an athlete."
doc = nlp(text)
print(doc._.sent_cluster)
```

Output:

```
{Twitter is another company.: [Twitter is another company., Microsoft is a company.], Tiger Woods is an athlete.: [Tiger Woods is an athlete., Michael Jordan is an athlete.]}
```

### Token Cluster

The `token_cluster` component groups tokens in the text into clusters based on similarity.

```python
import spacy
from bagpipes_spacy import TokenCluster

nlp = spacy.load("en_core_web_lg")
nlp.add_pipe("token_cluster", config={"threshold": 0.4})

doc = nlp(text)
print(doc._.token_cluster)
```

Output:

```
{Microsoft: [Microsoft, company], company: [Microsoft, company, company], Tiger: [Tiger, Woods], Jordan: [Jordan, Michael, Woods], athlete: [athlete, athlete]}
```

### Entity Cluster

The `entity_cluster` component groups entities in the text into clusters based on similarity.

```python
import spacy
from bagpipes_spacy import EntityCluster

nlp = spacy.load("en_core_web_lg")
nlp.add_pipe("entity_cluster", config={"threshold": 0.3})

doc = nlp(text)
print(doc._.ent_cluster)
```

Output:

```
{Twitter: [Twitter, Microsoft], Michael Jordan: [Michael Jordan, Tiger Woods]}
```

### Keyword Extractor

The `keyword_extractor` component extracts keywords from the text based on cosine similarity with the entire text or sentence.

#### Configuration

The `KeywordExtractor` can be configured using the following parameters:

- `top_n`: The number of top keywords to extract for the entire document.
- `min_ngram`: The minimum size for n-grams.
- `max_ngram`: The maximum size for n-grams.
- `strict`: If set to `True`, only n-grams within the `min_ngram` to `max_ngram` range are considered. If `False`, individual tokens and the specified range of n-grams are considered.
- `top_n_sent`: The number of top keywords to extract for each sentence.


```python
import spacy
from bagpipes_spacy import KeywordExtractor

nlp = spacy.load("en_core_web_lg")
nlp.add_pipe("keyword_extractor", last=True, config={"top_n": 10, "min_ngram": 1, "max_ngram": 3, "strict": True, "top_n_sent": 3})

text = "Natural language processing is a fascinating domain of artificial intelligence. It allows computers to understand and generate human language."
doc = nlp(text)
print("Top Document Keywords:", doc._.keywords)
for sent in doc.sents:
    print(f"Sentence: {sent.text}")
    print("Top Sentence Keywords:", sent._.sent_keywords)
```

Output:

```
Top Document Keywords: [('Natural language processing', 1, 0.7576146), ('language processing', 1, 0.75203013), ('artificial intelligence', 1, 0.74064857), ('generate human language', 1, 0.8099933), ('generate human', 1, 0.766044), ('human language', 1, 0.7234799)]

Sentence: Natural language processing is a fascinating domain of artificial intelligence.
Top Sentence Keywords: [('Natural language processing', 0.7576146), ('language processing', 0.75203013), ('artificial intelligence', 0.74064857)]

Sentence: It allows computers to understand and generate human language.
Top Sentence Keywords: [('generate human language', 0.8099933), ('generate human', 0.766044), ('human language', 0.7234799)]
```