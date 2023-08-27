# Set extensions for doc
import spacy
from spacy.tokens import Doc, Token, Span
from spacy.language import Language
from collections import defaultdict
import numpy as np

Doc.set_extension("triples", default=[], force=True)

@Language.factory("triple_detector")
class TripleDetector:
    def __init__(self, nlp, name):
        pass

    def __call__(self, doc):
        # List to store the triples
        triples = []
        
        # Iterate over each token in the doc
        for token in doc:
            # Check if the token is a verb
            if "VERB" in token.pos_:
                subject = ""
                obj = ""
                predicate = token.lemma_
                # Iterate over the children of the verb
                for child in token.children:
                    # Check if the child is a subject
                    if "subj" in child.dep_:
                        subject = child.text
                    # Check if the child is an object
                    if "obj" in child.dep_:
                        obj = child.text
                    # Check if the child is a prepositional phrase
                    if child.dep_ == "prep":
                        # Modified line: remove the preposition from the object
                        obj = doc[child.i + 1 : child.right_edge.i + 1].text
                        predicate = doc[token.i : child.i + 1].text
                # If both a subject and an object were found, add the triple to the list
                if subject and obj:
                    triples.append((subject, predicate, obj))
        
        # Set the triples attribute of the doc
        doc._.triples = triples
        
        return doc


# Set extensions for doc
Doc.set_extension("ent_similarity", default=[], force=True)
Doc.set_extension("ent_mappings", default={}, force=True)

@Language.factory("entity_similarity")
class EntitySimilarity:
    def __init__(self, nlp, name):
        self.nlp = nlp

    def __call__(self, doc):
        # compute similarity between all pairs of entities with same label
        similarities = []
        mappings = {}
        for ent1 in doc.ents:
            for ent2 in doc.ents:
                if ent1 != ent2 and ent1.label_ == ent2.label_:
                    similarity = self.compute_similarity(ent1, ent2)
                    if similarity >= self.nlp.config["threshold"]:
                        similarities.append((ent1, ent2, similarity))
                        self.update_mappings(mappings, ent1, ent2)
        doc._.ent_similarity = similarities
        doc._.ent_mappings = mappings
        return doc

    def compute_similarity(self, ent1, ent2):
        # customize this method to compute similarity in the way you want
        # for example, you could compute the similarity between the vector
        # representations of the entities' names, or you could compute the
        # similarity between different parts of the entities' names and then
        # take the average
        return ent1.similarity(ent2)

    def update_mappings(self, mappings, ent1, ent2):
        # update the mappings dictionary with the longest form of the entity
        if len(ent1) > len(ent2):
            mappings.setdefault(ent1, [])
            if ent2 not in mappings[ent1]:
                mappings[ent1].append(ent2)
        else:
            mappings.setdefault(ent2, [])
            if ent1 not in mappings[ent2]:
                mappings[ent2].append(ent1)



# Set extensions
Doc.set_extension("ent_cluster", default={}, force=True)
Doc.set_extension("sent_cluster", default={}, force=True)
Doc.set_extension("token_cluster", default={}, force=True)

class BaseCluster:
    def __init__(self, nlp, name, threshold=0.5):
        self.nlp = nlp
        self.threshold = threshold

    def __call__(self, doc):
        raise NotImplementedError

    def compute_clusters(self, items):
        clusters = {}
        for item1 in items:
            for item2 in items:
                if item1 != item2:
                    similarity = self.compute_similarity(item1, item2)
                    if similarity >= self.threshold:
                        self.update_clusters(clusters, item1, item2, similarity)
        return clusters

    def compute_similarity(self, item1, item2):
        return item1.similarity(item2)

    def update_clusters(self, clusters, item1, item2, similarity):
        cluster1 = clusters.get(item1, [item1])
        cluster2 = clusters.get(item2, [item2])
        cluster = list(set(cluster1 + cluster2))
        max_avg_similarity = 0
        central_node = None
        for item in cluster:
            avg_similarity = self.compute_avg_similarity(item, cluster)
            if avg_similarity > max_avg_similarity:
                max_avg_similarity = avg_similarity
                central_node = item
        clusters[central_node] = cluster

    def compute_avg_similarity(self, item, cluster):
        total_similarity = 0
        for other_item in cluster:
            if item != other_item:
                total_similarity += self.compute_similarity(item, other_item)
        return total_similarity / (len(cluster) - 1)


@Language.factory("entity_cluster")
class EntityCluster(BaseCluster):
    def __init__(self, nlp, name, threshold=0.5, same_label_only=True):
        super().__init__(nlp, name, threshold)
        self.same_label_only = same_label_only

    def __call__(self, doc):
        ent_cluster = self.compute_clusters(doc.ents)
        if self.same_label_only:
            ent_cluster = {central_node: cluster for central_node, cluster in ent_cluster.items() if all(central_node.label_ == ent.label_ for ent in cluster)}
        doc._.ent_cluster = ent_cluster
        return doc

    def compute_similarity(self, ent1, ent2):
        return ent1.similarity(ent2)


@Language.factory("sentence_cluster")
class SentenceCluster(BaseCluster):
    def __init__(self, nlp, name, threshold=0.5):
        super().__init__(nlp, name, threshold)
    def __call__(self, doc):
        sent_cluster = self.compute_clusters(list(doc.sents))
        doc._.sent_cluster = sent_cluster
        return doc


@Language.factory("token_cluster")
class TokenCluster(BaseCluster):
    def __init__(self, nlp, name, threshold=0.5, include_pos=["PROPN", "NOUN", "VERB"], same_pos_only=False):
        super().__init__(nlp, name, threshold)
        self.include_pos = include_pos
        self.same_pos_only = same_pos_only

    def __call__(self, doc):
        tokens = [token for token in doc if self.include_token(token)]
        token_cluster = self.compute_clusters(tokens)
        doc._.token_cluster = token_cluster
        return doc

    def include_token(self, token):
        return (not self.include_pos or token.pos_ in self.include_pos)

    def compute_clusters(self, tokens):
        return super().compute_clusters(tokens)


# Set extensions for tokens, doc, and sentence
Token.set_extension("keyword_value", default=0.0, force=True)
Doc.set_extension("keywords", default=[], force=True)
Span.set_extension("sent_keywords", default=[], force=True)

@Language.factory("keyword_extractor")
class KeywordExtractor:
    def __init__(self, nlp, name, top_n=5, top_n_sent=2, min_ngram=1, max_ngram=3, strict=False):
        self.top_n = top_n
        self.top_n_sent = top_n_sent
        self.min_ngram = min_ngram
        self.max_ngram = max_ngram
        self.strict = strict
        self.use_transformer = "transformer" in nlp.pipe_names

    def valid_token(self, token):
        if self.use_transformer:
            return not (token.is_punct or token.is_stop or token.like_num)
        else:
            return not (token.is_punct or token.is_stop or token.like_num or not token.has_vector)

    def cosine_similarity(self, vec1, vec2):
        return np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))

    def token_vector(self, token):
        if self.use_transformer:
            tensor_indices = token.doc._.trf_data.align[token.i].data.flatten()
            tensor_shape = token.doc._.trf_data.tensors[0].shape[-1]
            tensor = token.doc._.trf_data.tensors[0].reshape(-1, tensor_shape)[tensor_indices]
            return tensor.mean(axis=0)
        else:
            return token.vector

    def span_vector(self, span):
        if self.use_transformer:
            tensor_indices = span.doc._.trf_data.align[span.start: span.end].data.flatten()
            tensor_shape = span.doc._.trf_data.tensors[0].shape[-1]
            tensor = span.doc._.trf_data.tensors[0].reshape(-1, tensor_shape)[tensor_indices]
            return tensor.mean(axis=0)
        else:
            return span.vector

    def __call__(self, doc):
        keyword_freqs = defaultdict(int)
        keyword_similarities = defaultdict(float)

        # Process each sentence
        for sent in doc.sents:
            sent_keywords = self.extract_keywords(sent)
            for keyword, similarity in sent_keywords:
                keyword_freqs[keyword] += 1
                keyword_similarities[keyword] = similarity
            sent._.sent_keywords = sent_keywords

        # Sort keywords based on frequency for the entire document
        sorted_keywords = sorted(keyword_freqs.keys(), key=lambda x: keyword_freqs[x], reverse=True)
        
        # Convert the sorted keywords to tuples with their frequency and similarity scores
        doc._.keywords = [(keyword, keyword_freqs[keyword], keyword_similarities[keyword]) for keyword in sorted_keywords[:self.top_n]]
        
        return doc
    def extract_keywords(self, span):
        token_values = set()

        # Calculate the cosine similarity for individual tokens
        span_vec = self.span_vector(span)
        for token in span:
            if self.valid_token(token):
                similarity = self.cosine_similarity(self.token_vector(token), span_vec)
                token._.keyword_value = similarity
                if not self.strict:
                    token_values.add((token.text, token._.keyword_value))

        # If min_ngram and max_ngram are not both 1, perform n-gram extraction
        if not (self.min_ngram == 1 and self.max_ngram == 1):
            for n in range(self.min_ngram, self.max_ngram + 1):
                for i in range(len(span) - n + 1):
                    ngram = span[i:i+n]
                    if all(self.valid_token(token) for token in ngram):
                        ngram_text = " ".join([token.text for token in ngram])
                        similarity = self.cosine_similarity(self.span_vector(ngram), span_vec)
                        token_values.add((ngram_text.strip(), similarity))

        # Sort based on similarity values
        sorted_tokens = sorted(token_values, key=lambda x: x[1], reverse=True)


        # Extract top keywords for the sentence based on `top_n_sent`
        sent_keywords = sorted_tokens[:self.top_n_sent]

        return sent_keywords