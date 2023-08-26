import spacy
import re
import unicodedata
from spacy.language import Language


@Language.factory("normalizer")
class Normalizer:
    def __init__(self, nlp, name,
                 normalize_whitespace=True,
                 remove_parentheses=True,
                 remove_brackets=True,
                 expand_contractions=True,
                 remove_diacritics=True):
        self.nlp = nlp
        self.normalize_whitespace = normalize_whitespace
        self.remove_parentheses = remove_parentheses
        self.remove_brackets = remove_brackets
        self.expand_contractions = expand_contractions
        self.remove_diacritics = remove_diacritics

    def __call__(self, doc):
        text = doc.text
        if self.expand_contractions:
            text = expand_contractions(text)
        if self.normalize_whitespace:
            text = ' '.join(text.split())
        if self.remove_parentheses:
            text = re.sub(r'\(.*?\)', '', text)
        if self.remove_brackets:
            text = re.sub(r'\[.*?\]', '', text)
        if self.remove_diacritics:
            text = unicodedata.normalize('NFD', text).encode('ascii', 'ignore').decode('utf-8')
        return self.nlp.tokenizer(text)

contractions_dict = {
    "can't": "cannot",
    "won't": "will not",
    "i'm": "i am",
    "i'll": "i will",
    "i'd": "i would",
    "i've": "i have",
    "you're": "you are",
    "you'll": "you will",
    "you'd": "you would",
    "you've": "you have",
    "he's": "he is",
    "he'll": "he will",
    "he'd": "he would",
    "she's": "she is",
    "she'll": "she will",
    "she'd": "she would",
    "it's": "it is",
    "it'll": "it will",
    "it'd": "it would",
    "we're": "we are",
    "we'll": "we will",
    "we'd": "we would",
    "we've": "we have",
    "they're": "they are",
    "they'll": "they will",
    "they'd": "they would",
    "they've": "they have",
    "that's": "that is",
    "that'll": "that will",
    "that'd": "that would",
    "who's": "who is",
    "who'll": "who will",
    "who'd": "who would",
    "what's": "what is",
    "what'll": "what will",
    "what'd": "what would",
    "where's": "where is",
    "where'll": "where will",
    "where'd": "where would",
    "when's": "when is",
    "when'll": "when will",
    "when'd": "when would",
    "why's": "why is",
    "why'll": "why will",
    "why'd": "why would",
    "how's": "how is",
    "how'll": "how will",
    "how'd": "how would",
    "isn't": "is not",
    "aren't": "are not",
    "wasn't": "was not",
    "weren't": "were not",
    "haven't": "have not",
    "hasn't": "has not",
    "hadn't": "had not",
    "doesn't": "does not",
    "don't": "do not",
    "didn't": "did not",
    "won't": "will not",
    "wouldn't": "would not",
    "couldn't": "could not",
    "shouldn't": "should not",
    "mightn't": "might not",
    "mustn't": "must not",
    "shan't": "shall not",
    "let's": "let us",
    "ma'am": "madam",
    "o'clock": "of the clock",
    "y'all": "you all",
    "ne'er": "never",
    "e'er": "ever",
    "o'er": "over",
}


# Update the contractions_dict to include all cases
all_case_contractions_dict = {k: v for k, v in contractions_dict.items()}
all_case_contractions_dict.update({k.upper(): v.upper() for k, v in contractions_dict.items()})
all_case_contractions_dict.update({k.capitalize(): v.capitalize() for k, v in contractions_dict.items()})

# Regular expression for finding contractions
contractions_re = re.compile('(%s)' % '|'.join(all_case_contractions_dict.keys()), re.IGNORECASE)

def expand_contractions(text):
    def replace(match):
        return all_case_contractions_dict[match.group(0)]
    return contractions_re.sub(replace, text)