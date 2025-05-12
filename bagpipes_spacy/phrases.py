import spacy
from spacy.tokens import Doc, Token, Span
from spacy.language import Language

# Set extension for doc
Doc.set_extension("quotes", default=[], force=True)


@Language.factory("quote_detector")
class QuoteDetector:
    def __init__(self, nlp, name):
        pass

    def __call__(self, doc):
        # List to store the quotes
        quotes = []

        # Iterate over each token in the doc
        in_quote = False
        start = 0
        end = 0
        for i, token in enumerate(doc):
            # Check if the token is a starting quote
            if token.text in ['"', "“", "‘", "’", "”", "'"] and not in_quote:
                start = i
                in_quote = True
            # Check if the token is an ending quote
            elif token.text in ['"', "”", "’", "”", "‘", "'"] and in_quote:
                end = i
                in_quote = False
                quotes.append(doc[start : end + 1])

        # Set the quotes attribute of the doc
        doc._.quotes = quotes

        return doc


# Set extensions for doc
Doc.set_extension("prep_phrases", default=[], force=True)
Doc.set_extension("noun_phrases", default=[], force=True)
Doc.set_extension("verb_phrases", default=[], force=True)
Doc.set_extension("adj_phrases", default=[], force=True)
Doc.set_extension("adv_phrases", default=[], force=True)


@Language.factory("phrases_extractor")
class PhrasesExtractor:
    def __init__(self, nlp, name):
        pass

    def __call__(self, doc):
        # List to store the phrases
        prep_phrases = []
        noun_phrases = []
        verb_phrases = []
        adj_phrases = []
        adv_phrases = []

        # Set to store the indices of tokens already included in an adjective phrase
        adj_tokens = set()

        # Iterate over each token in the doc
        for token in doc:
            # Prepositional Phrases
            if token.pos_ == "ADP":
                # Get the adjacent tokens
                next_token = doc[token.i + 1] if token.i < len(doc) - 1 else None
                # Check if the next token is also a preposition
                if next_token and next_token.pos_ == "ADP":
                    prep_phrase = doc[token.i : next_token.i + 1]
                else:
                    children = list(token.children)
                    prep_phrase = doc[token.i : children[-1].i + 1] if children else token
                prep_phrases.append(prep_phrase)

            # Noun Phrases
            elif token.pos_ in ["NOUN", "PRON"]:
                noun_phrase = doc[token.left_edge.i : token.right_edge.i + 1]

                noun_phrases.append(noun_phrase)
            # Verb Phrases
            elif token.pos_ == "VERB":
                verb_phrase = doc[token.left_edge.i : token.right_edge.i + 1]
                verb_phrases.append(verb_phrase)
            # Adjective Phrases
            elif token.pos_ == "ADJ" and token.i not in adj_tokens:
                # Get the adjacent tokens
                left_token = doc[token.i - 1] if token.i > 0 else None
                right_token = doc[token.i + 1] if token.i < len(doc) - 1 else None
                # Check if the adjacent tokens are also adjectives
                if left_token and left_token.pos_ == "ADJ":
                    adj_phrase = doc[left_token.i : token.i + 1]
                    adj_tokens.update(range(left_token.i, token.i + 1))
                elif right_token and right_token.pos_ == "ADJ":
                    adj_phrase = doc[token.i : right_token.i + 1]
                    adj_tokens.update(range(token.i, right_token.i + 1))
                else:
                    adj_phrase = token
                    adj_tokens.add(token.i)
                adj_phrases.append(adj_phrase)
            # Adverbial Phrases
            elif token.pos_ == "ADV":
                adv_phrase = doc[token.left_edge.i : token.right_edge.i + 1]
                adv_phrases.append(adv_phrase)

        # Set the phrases attributes of the doc
        doc._.prep_phrases = prep_phrases
        doc._.noun_phrases = noun_phrases
        doc._.verb_phrases = verb_phrases
        doc._.adj_phrases = adj_phrases
        doc._.adv_phrases = adv_phrases

        return doc
