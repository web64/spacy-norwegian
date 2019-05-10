# Instructions for training Norwegian Spacy models

## Setup
Start by cloning this repository
```bash
git clone https://github.com/web64/spacy-norwegian.git
cd spacy-norwegian
```

# Vectors

Download FastText Vectors and convert for use in Spacy

See: https://spacy.io/usage/vectors-similarity#converting

You can optionally download the vectors manually from: https://fasttext.cc/docs/en/crawl-vectors.html

```bash
# Download Bokmål vectors
wget -P fasttext https://dl.fbaipublicfiles.com/fasttext/vectors-crawl/cc.no.300.vec.gz

# Create Spacy model from Bokmål vectors
python -m spacy init-model nb fasttext/no_vectors_ft_lg --vectors-loc fasttext/cc.no.300.vec.gz

# Download Nynorsk vectors 
wget -P fasttext https://dl.fbaipublicfiles.com/fasttext/vectors-crawl/cc.nn.300.vec.gz
```

# Train Norwegian NER Model
```bash
git clone https://github.com/ltgoslo/norne

# Merge Bokmaal and Nynorsk conllu data
cat norne/ud/nob/no_bokmaal-ud-train.conllu norne/ud/nno/no_nynorsk-ud-train.conllu > conllu/no-train.conllu 
cat norne/ud/nob/no_bokmaal-ud-dev.conllu norne/ud/nno/no_nynorsk-ud-dev.conllu > conllu/no-dev.conllu 
cat norne/ud/nob/no_bokmaal-ud-test.conllu norne/ud/nno/no_nynorsk-ud-test.conllu > conllu/no-test.conllu 

# Convert conllu to Spacy JSON format
python3 -m spacy convert conllu/no-train.conllu norne-json
python3 -m spacy convert conllu/no-dev.conllu norne-json
python3 -m spacy convert conllu/no-test.conllu norne-json

# Convert 
python3 -m spacy convert --file-type=json --morphology norne/ud/nob/no_bokmaal-ud-train.conllu norne-json
python3 -m spacy convert --file-type=json --morphology norne/ud/nob/no_bokmaal-ud-dev.conllu norne-json



python3 -m spacy train nb --version=0.0.1 norne-models  norne-json/no_bokmaal-ud-train.json norne-json/no_bokmaal-ud-dev.json
# Train
python3 -m spacy train nb norne-models norne-json/no-train.json norne-json/no-dev.json


python3 -m spacy package models-ner/model7 packages --force

cd packages/nb_unnamed-0.0.0/
python3 setup.py sdist
```



# License

The code examples in this repository is licensed under MIT.
Models are under the same license as that of their respective training data.