# Download Vectors

Below are two methods for downloading and converting Norwegian vectors for use in Spacy.
You can try different vector models to see gives the best results when training the Spacy model.

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
# Norsk Aviskorpus + NoWaC - fastText Skipgram
wget -P nowac http://vectors.nlpl.eu/repository/11/120.zip
unzip nowac/120.zip -d nowac/120/
python3 -m spacy init-model nb models/nb_vectors_nowac_md --vectors-loc nowac/120/model.txt

# Norsk Aviskorpus + NoWaC + NBDigital - Gensim Continuous Skipgram
wget -P nowac http://vectors.nlpl.eu/repository/11/100.zip
unzip nowac/100.zip -d nowac/100/
python3 -m spacy init-model nb models/nb_vectors_nowac_nbdigital_md --vectors-loc nowac/100/model.txt


# Norsk Aviskorpus + NoWaC + NBDigital - fastText Skipgram
wget -P nowac http://vectors.nlpl.eu/repository/11/81.zip
unzip nowac/81.zip -d nowac/81/
python3 -m spacy init-model nb models/nb_vectors_nowac_nbdigital_md --vectors-loc nowac/81/model.txt
```