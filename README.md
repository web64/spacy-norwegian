# Training Norwegian models for Spacy

The method described below was tested on Ubuntu 16.04 with Spacy 2.1.3. On different systems or different versions of Spacy the steps might be slightly different.
In case of errors, please refer to the Spacy documentation or submit an issue here on this repository.

Suggestions for improvements would be greatly appreciated!

## Setup
Start by cloning this repository and download the NorNE corpus.
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

# Train Norwegian Bokmål NER Model

```bash
# Fix .conllu files - strip 'name=' from files: 'name=I-PER' -> 'I-PER'
sed -i 's/SpaceAfter=No name=//g' norne/ud/nob/no_bokmaal-ud-dev.conllu
sed -i 's/name=//g' norne/ud/nob/no_bokmaal-ud-dev.conllu
sed -i 's/SpaceAfter=No name=//g' norne/ud/nob/no_bokmaal-ud-train.conllu
sed -i 's/name=//g' norne/ud/nob/no_bokmaal-ud-train.conllu

# Convert .conllu files to Spacy JSON format
python3 -m spacy convert --file-type json --morphology norne/ud/nob/no_bokmaal-ud-train.conllu json
python3 -m spacy convert --file-type json --morphology norne/ud/nob/no_bokmaal-ud-dev.conllu json

# Train Model - with Norsk Aviskorpus/NoWaC  vectors
python3 -m spacy train nb --version=0.0.1 --vectors=models/nb_vectors_nowac_md models/nb_ud_nowac_md  json/no_bokmaal-ud-train.json json/no_bokmaal-ud-dev.json
```

# Train Norwegian Nynorsk Model (NER not availavble)
```bash
# Download Nynorsk FastText vectors & create Spacy model
wget -P fasttext https://dl.fbaipublicfiles.com/fasttext/vectors-crawl/cc.nn.300.vec.gz
python3 -m spacy init-model nb models/nn_vectors_ft_lg --vectors-loc fasttext/cc.nn.300.vec.gz

# Fix .conllu files - strip 'name=' from files: 'name=I-PER' -> 'I-PER'
sed -i 's/SpaceAfter=No name=//g' norne/ud/nno/no_nynorsk-ud-dev.conllu
sed -i 's/name=//g' norne/ud/nno/no_nynorsk-ud-dev.conllu
sed -i 's/SpaceAfter=No name=//g' norne/ud/nno/no_nynorsk-ud-train.conllu
sed -i 's/name=//g' norne/ud/nno/no_nynorsk-ud-train.conllu

# Convert .conllu files to Spacy JSON format
python3 -m spacy convert --file-type json --morphology norne/ud/nno/no_nynorsk-ud-train.conllu json
python3 -m spacy convert --file-type json --morphology norne/ud/nno/no_nynorsk-ud-dev.conllu json

# Train Model -
python3 -m spacy train nb --version=0.0.1 --vectors=models/nn_vectors_ft_lg models/nb_ud_nowac_md  json/no_bokmaal-ud-train.json json/no_bokmaal-ud-dev.json
```


# Train Mixed Bokmål/Nynorsk Norwegian NER Model
```bash
# Merge Bokmål and Nynorsk conllu data
cat norne/ud/nob/no_bokmaal-ud-train.conllu norne/ud/nno/no_nynorsk-ud-train.conllu norne/ud/nob/no_bokmaal-ud-test.conllu norne/ud/nno/no_nynorsk-ud-test.conllu > conllu/no-train.conllu 
cat norne/ud/nob/no_bokmaal-ud-dev.conllu norne/ud/nno/no_nynorsk-ud-dev.conllu > conllu/no-dev.conllu 

sed -i 's/SpaceAfter=No name=//g' conllu/no-dev.conllu 
sed -i 's/name=//g' conllu/no-dev.conllu 
sed -i 's/SpaceAfter=No name=//g' conllu/no-train.conllu
sed -i 's/name=//g' conllu/no-train.conllu


# Convert conllu to Spacy JSON format
python3 -m spacy convert --file-type json conllu/no-train.conllu json
python3 -m spacy convert --file-type json conllu/no-dev.conllu json

# Train Spacy model
python3 -m spacy train nb --version=0.0.1 --vectors=models/nb_vectors_nowac_md models/no_ud_nowac_md json/no-train.json json/no-dev.json
```


# Creating packages from models

```bash
python3 -m spacy package models/no_ud_nowac_md/model-best packages --force
cd packages/cd nb_model0-0.0.1/
python3 setup.py sdist
```
In some versions of Spacy, the /packages/[MODEL]/meta.json needs to include these fields in order to run the `python setup.py sdist` command.
```json
{
  "description":"",
  "author":"",
  "email":"",
  "url":"",
  "license":""
}
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