# Instructions for training Norwegian models for use in Spacy

NOTE: This is still a work-in-progress!

The method described below was tested on Ubuntu with Spacy 2.1.3. On different systems or different versions of Spacy the steps might be slightly different.
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

Below are two methods for downloading and converting Norwegian vectors for use in Spacy.

## 1 - FastText (Wikipedia + CommonCrawl)
Download FastText Vectors and convert for use in Spacy

See: https://spacy.io/usage/vectors-similarity#converting

You can optionally download the vectors manually from: https://fasttext.cc/docs/en/crawl-vectors.html

```bash
# Download Bokmål vectors & create Spacy model
wget -P fasttext https://dl.fbaipublicfiles.com/fasttext/vectors-crawl/cc.no.300.vec.gz
python3 -m spacy init-model nb models/nb_vectors_ft_lg --vectors-loc fasttext/cc.no.300.vec.gz

# Download Nynorsk vectors & create Spacy model
wget -P fasttext https://dl.fbaipublicfiles.com/fasttext/vectors-crawl/cc.nn.300.vec.gz
python3 -m spacy init-model nb models/nn_vectors_ft_lg --vectors-loc fasttext/cc.nn.300.vec.gz
```

## 2 - NLPL (Norsk Aviskorpus + NoWaC)
You can download this and several other vector model here: http://vectors.nlpl.eu/repository/

```bash
wget -P nowac http://vectors.nlpl.eu/repository/11/120.zip
unzip nowac/120.zip -d nowac/120/
python3 -m spacy init-model nb models/nb_vectors_nowac_md --vectors-loc nowac/120/model.txt


wget -P nowac http://vectors.nlpl.eu/repository/11/100.zip
unzip nowac/120.zip -d nowac/100/
python3 -m spacy init-model nb models/nb_vectors_nowac_nbdigital_md --vectors-loc nowac/100/model.txt
```

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

# Train Model - with FastText vectors
python3 -m spacy train nb --version=0.0.1 --vectors=models/nb_vectors_ft_lg norne-models  json/no_bokmaal-ud-train.json json/no_bokmaal-ud-dev.json

# Train Model - with NoWaC vectors
python3 -m spacy train nb --version=0.0.1 --vectors=models/nb_vectors_nowac_md models/nb_ud_nowac_md  json/no_bokmaal-ud-train.json json/no_bokmaal-ud-dev.json
```

# Train Norwegian Nynorsk NER Model
```bash
# Fix .conllu files - strip 'name=' from files: 'name=I-PER' -> 'I-PER'
sed -i 's/SpaceAfter=No name=//g' norne/ud/nno/no_nynorsk-ud-dev.conllu
sed -i 's/name=//g' norne/ud/nno/no_nynorsk-ud-dev.conllu
sed -i 's/SpaceAfter=No name=//g' norne/ud/nno/no_nynorsk-ud-train.conllu
sed -i 's/name=//g' norne/ud/nno/no_nynorsk-ud-train.conllu

# Convert .conllu files to Spacy JSON format
python3 -m spacy convert --file-type json --morphology norne/ud/nno/no_nynorsk-ud-train.conllu json
python3 -m spacy convert --file-type json --morphology norne/ud/nno/no_nynorsk-ud-dev.conllu json

# Train Model -
python3 -m spacy train nb --version=0.0.1 --vectors=models/nn_vectors_nowac_md models/nb_ud_nowac_md  json/no_bokmaal-ud-train.json json/no_bokmaal-ud-dev.json
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

# Train
# python3 -m spacy train nb --version=0.0.1 --vectors=models/nb_vectors_nowac_nbdigital_md models/no_ud_nowac-nbdigital_md json/no-train.json json/no-dev.json
python3 -m spacy train nb --version=0.0.1 --vectors=models/nb_vectors_nowac_md models/no_ud_nowac_md json/no-train.json json/no-dev.json

# Packages
python3 -m spacy package models/no_ud_nowac_md/model-best packages --force
cd packages/nb_unnamed-0.0.0/
python3 setup.py sdist
```



# See Also

* https://github.com/ltgoslo/norne
* https://github.com/jarib/spacy-nb

## Spacy Resources
* https://spacy.io/usage/vectors-similarity#converting
* https://github.com/explosion/spaCy/issues/3056 - Adding models for new languages 
* https://spacy.io/api/cli#convert - Convert .conllu to .json command
* https://spacy.io/api/cli#train - Train Spacy model command

# License

The code examples in this repository is licensed under MIT.
Models are under the same license as that of their respective training data.