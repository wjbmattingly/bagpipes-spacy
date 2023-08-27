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

nlp = spacy.blank("en")

nlp.add_pipe("quote_detector")

text = """
"I... oh ... very well," said the Prime Minister weakly. "Yes, I'll see Fudge."
He hurried back to his desk, straightening his tie as he went. He had barely resumed his seat, and arranged his face into what he hoped was a relaxed and unfazed expression, when bright green flames burst into life in the empty grate beneath his marble mantelpiece. He watched, trying not to betray a flicker of surprise or alarm, as a portly man appeared within the flames, spinning as fast as a top. Seconds later, he had climbed out onto a rather fine antique rug, brushing ash from the sleeves of his long pin-striped cloak, a lime-green bowler hat in his hand.
"Ah... Prime Minister," said Cornelius Fudge, striding forward with his hand outstretched. "Good to see you again."
The Prime Minister could not honestly return this compliment, so said nothing at all. He was not remotely pleased to see Fudge, whose occasional appearances, apart from being downright alarming in themselves, generally meant that he was about to hear some very bad news. Furthermore, Fudge was looking distinctly careworn. He was thinner, balder, and grayer, and his face had a crumpled look. The Prime Minister had seen that kind of look in politicians before, and it never boded well.
"How can I help you?" he said, shaking Fudge's hand very briefly and gesturing toward the hardest of the chairs in front of the desk.
"Difficult to know where to begin," muttered Fudge, pulling up the chair, sitting down, and placing his green bowler upon his knees. "What a week, what a week..."
"Had a bad one too, have you?" asked the Prime Minister stiffly, hoping to convey by this that he had quite enough on his plate already without any extra helpings from Fudge.
"Yes, of course," said Fudge, rubbing his eyes wearily and looking morosely at the Prime Minister. "I've been having the same week you have, Prime Minister. The Brockdale Bridge... the Bones and Vance murders... not to mention the ruckus in the West Country..."
"You--er--your--I mean to say, some of your people were--were involved in those--those things, were they?"
Fudge fixed the Prime Minister with a rather stern look. "Of course they were," he said, "Surely you've realized what's going on?"
"I..." hesitated the Prime Minister.
"""

doc = nlp(text)
for quote in doc._.quotes:
    print(quote)
```

Output:
```
"I... oh ... very well,"
"Yes, I'll see Fudge."
"Ah... Prime Minister,"
"Good to see you again."
"How can I help you?"
"Difficult to know where to begin,"
"What a week, what a week..."
"Had a bad one too, have you?"
"Yes, of course,"
"I've been having the same week you have, Prime Minister. The Brockdale Bridge... the Bones and Vance murders... not to mention the ruckus in the West Country..."
"You--er--your--I mean to say, some of your people were--were involved in those--those things, were they?"
"Of course they were,"
"Surely you've realized what's going on?"
"I..."
```

### Integrating the Phrases Extractor

Import the `PhrasesExtractor` and integrate it into your spaCy pipeline:

```python
from bagpipes_spacy import PhrasesExtractor

# Integrate the component into the pipeline
nlp = spacy.load("en_core_web_md")

nlp.add_pipe("phrases_extractor")

text = """Seconds later, he had climbed out onto a rather fine antique rug, brushing ash from the sleeves of his long pin-striped cloak, a lime-green bowler hat in his hand.
"""

doc = nlp(text)

print("Prepositional Phrases")
print(doc._.prep_phrases)
print()

print("Noun Phrases")
print(doc._.noun_phrases)
print()

print("Verb Phrases")
print(doc._.verb_phrases)
print()

print("Adj Phrases")
print(doc._.adj_phrases)
```

Output:
```
Prepositional Phrases
[out onto, onto a rather fine antique rug, from the sleeves, of his long pin-striped cloak, in his hand]

Noun Phrases
[a rather fine antique rug, the sleeves of his long pin-striped cloak, a lime-green bowler hat in his hand, his long pin-striped cloak, a lime-green bowler hat in his hand, a lime-green bowler hat in his hand, his hand]

Verb Phrases
[Seconds later, he had climbed out onto a rather fine antique rug, brushing ash from the sleeves of his long pin-striped cloak, a lime-green bowler hat in his hand.
, brushing ash from the sleeves of his long pin-striped cloak, a lime-green bowler hat in his hand, pin-striped]

Adj Phrases
[fine antique, long, green]
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