# Training Norwegian models for Spacy

__UPDATE:__ There is now an official Norwegian model for Spacy available.
```
# Download Norwegian Spacy model
python -m spacy download nb_core_news_sm
```



The method described below was tested on Ubuntu 18.04 with Spacy 2.1.4. On different systems or different versions of Spacy the steps might be slightly different.
In case of errors, please refer to the Spacy documentation or submit an issue here on this repository.

Suggestions for improvements would be greatly appreciated!

## Setup
Start by cloning this repository and download the [NorNE](https://github.com/ltgoslo/norne) corpus.
```bash
git clone https://github.com/web64/spacy-norwegian.git
cd spacy-norwegian

git clone https://github.com/ltgoslo/norne
```

# Vectors 
A vector model is not required for most of Spacy's functionality, but can be used to improve results.
You can train new vector models from your own training texts or use one of the many available pre-trained vector models.
Pre-trained Word2vec, Gensim and FastText vector models needs to be converted before use in Spacy.



```bash
# Norsk Aviskorpus + NoWaC - fastText Skipgram
wget -P nowac http://vectors.nlpl.eu/repository/11/120.zip
unzip nowac/120.zip -d nowac/120/
python3 -m spacy init-model nb models/nb_vectors_nowac_md --vectors-loc nowac/120/model.txt
```

[Instructions for preparing additional Norwegian vector models](https://github.com/web64/spacy-norwegian/blob/master/vectors.md)


# Prepare training data
First convert .conllu files to a format parsable by Spacy.
The 10th MISC column will be converted from `SpaceAfter=No|name=B-GPE_ORG` to only include `B-GPE_ORG`.
```bash
python3 norne/scripts/ud2spacy.py nob --outputdir=conllu
python3 norne/scripts/ud2spacy.py nno --outputdir=conllu
```

Convert .conllu files to  Spacy's JSON format
```bash
python3 -m spacy convert --file-type json --morphology conllu/no_bokmaal-ud-train.conllu json
python3 -m spacy convert --file-type json --morphology conllu/no_bokmaal-ud-dev.conllu json
python3 -m spacy convert --file-type json --morphology conllu/no_bokmaal-ud-test.conllu json

python3 -m spacy convert --file-type json --morphology conllu/no_nynorsk-ud-train.conllu json
python3 -m spacy convert --file-type json --morphology conllu/no_nynorsk-ud-dev.conllu json
python3 -m spacy convert --file-type json --morphology conllu/no_nynorsk-ud-test.conllu json
```

# Train Norwegian Bokmål NER Model
```bash
# Train Model - with Norsk Aviskorpus/NoWaC  vectors
python3 -m spacy train nb --version=0.0.1 --vectors=models/nb_vectors_nowac_md models/nb_ud_nowac_md  json/no_bokmaal-ud-train.json json/no_bokmaal-ud-dev.json
```

# Train Norwegian Nynorsk Model
```bash
# Download Nynorsk FastText vectors & create Spacy model
wget -P fasttext https://dl.fbaipublicfiles.com/fasttext/vectors-crawl/cc.nn.300.vec.gz
python3 -m spacy init-model nb models/nn_vectors_ft_lg --vectors-loc fasttext/cc.nn.300.vec.gz

# Train Model -
python3 -m spacy train nb --version=0.0.1 --vectors=models/nn_vectors_ft_lg models/nb_ud_nowac_md  json/no_bokmaal-ud-train.json json/no_bokmaal-ud-dev.json
```


# Train Mixed Bokmål/Nynorsk Norwegian NER Model
```bash
# Merge Bokmål and Nynorsk conllu data
cat conllu/no_bokmaal-ud-train.conllu conllu/no_nynorsk-ud-train.conllu conllu/no_bokmaal-ud-test.conllu conllu/no_nynorsk-ud-test.conllu > conllu/no-train.conllu 
cat conllu/no_bokmaal-ud-dev.conllu conllu/no_nynorsk-ud-dev.conllu > conllu/no-dev.conllu 

# Convert conllu to Spacy JSON format
python3 -m spacy convert --file-type json conllu/no-train.conllu json
python3 -m spacy convert --file-type json conllu/no-dev.conllu json

# Train Spacy model
python3 -m spacy train nb --version=0.0.1 --vectors=models/nb_vectors_nowac_md models/no_ud_nowac_md json/no-train.json json/no-dev.json
```

```json
"accuracy":{
    "uas":91.7548876959,
    "las":89.2278360343,
    "ents_p":89.3064571233,
    "ents_r":88.8511216859,
    "ents_f":89.0782075311,
    "tags_acc":97.6323222763,
    "token_acc":100.0
  }
```

# Reducing model size
You can reduce the number of word vectors to include in the model by setting the `--prune-vectors=N` flag for the `spacy init-model` [command](https://spacy.io/api/cli#init-model).


# Creating packages from models

```bash
python3 -m spacy package --create-meta models/no_ud_nowac_md/model-best packages --force
cd packages/cd nb_model0-0.0.1/
python3 setup.py sdist

# Install package
pip3 install package-name.tar.gz
```

# Testing the model

First update the path to the model: `Norwegian = spacy.load("/PATH/TO/MODEL")`

Then run:
```bash
python3 spacy_no_test.py
```

# See Also

* https://github.com/ltgoslo/norne - Norwegian Named Entities annotations on top of Norwegian Dependency Treebank
* https://github.com/jarib/spacy-nb - Scripts to build a Norwegian model for spacy 

## Spacy Resources
* https://spacy.io/usage/vectors-similarity#converting
* https://github.com/explosion/spaCy/issues/3056 - Adding models for new languages 
* https://spacy.io/api/cli#convert - Convert .conllu to .json command
* https://spacy.io/api/cli#train - Train Spacy model command

# License

The code examples in this repository is licensed under MIT.
Models are under the same license as that of their respective training data.
