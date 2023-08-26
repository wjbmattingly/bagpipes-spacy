# Set extensions for doc
import spacy
from spacy.tokens import Doc, Token, Span
from spacy.language import Language

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
