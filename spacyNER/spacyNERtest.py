import spacy
from spacy.tokens import DocBin
import json


def loadAnnot(path, fileBase):
    nlp = spacy.blank("en") # load a new spacy model
    db = DocBin() # create
    trainX = None
    with open(path, 'r') as f:
        trainX = json.load(f)

    for txt, annot in trainX['annotations']:
        doc = nlp.make_doc (txt)
        ents = []
        for s, e, l in annot['entities']:
            span = doc.char_span(s, e, label=l, alignment_mode='contract')
            if (span is None):
                print("skipping entity")
            else:
                ents.append(span)
        doc.ents = ents
        db.add(doc)

    db.to_disk(fileBase+".spacy")

def main():
    # all_labels = ['GEN', 'OCC', 'TOF', 'COL', 'FAB', 'PRI']
    loadAnnot('./annotations.json', "annotations")
    loadAnnot("./test_annotations.json", "test_annot")

def test():
    prompt = input("Enter prompt")
    nlpner = spacy.load("./model-best")
    doc = nlpner(prompt)
    for ent in doc.ents:
        print(f'ent: {ent.text.strip()}, label: {ent.label_}')

if __name__ == "__main__":
    test()
