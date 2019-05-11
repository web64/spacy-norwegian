# All (Experimental)
Build model of all available datasets

UD_Norwegian-Nynorsk LIA + NoReC + NorNE 
```bash
# Download UD_Norwegian-Nynorsk LIA
wget -P conllu https://raw.githubusercontent.com/UniversalDependencies/UD_Norwegian-NynorskLIA/master/no_nynorsklia-ud-dev.conllu
wget -P conllu https://raw.githubusercontent.com/UniversalDependencies/UD_Norwegian-NynorskLIA/master/no_nynorsklia-ud-train.conllu
wget -P conllu https://raw.githubusercontent.com/UniversalDependencies/UD_Norwegian-NynorskLIA/master/no_nynorsklia-ud-test.conllu

# Download NoReC corpus
wget http://folk.uio.no/eivinabe/norec-1.0.1.tar.gz
tar -zxvf norec-1.0.1.tar.gz
tar -zxvf norec/conllu.tar.gz --directory=norec/
cat norec/conllu/dev/* > conllu/norec-dev.conllu
cat norec/conllu/test/* > conllu/norec-test.conllu
cat norec/conllu/train/* > conllu/norec-train.conllu

#cat conllu/no-train.conllu conllu/norec-test.conllu conllu/norec-train.conllu conllu/no_nynorsklia-ud-test.conllu conllu/no_nynorsklia-ud-train.conllu > conllu/no-all-train.conllu 
#cat conllu/no-dev.conllu conllu/norec-dev.conllu conllu/no_nynorsklia-ud-dev.conllu > conllu/no-all-dev.conllu 
cat conllu/no-train.conllu conllu/no_nynorsklia-ud-test.conllu conllu/no_nynorsklia-ud-train.conllu > conllu/no-all-train.conllu 
cat conllu/no-dev.conllu conllu/no_nynorsklia-ud-dev.conllu > conllu/no-all-dev.conllu 

python3 -m spacy convert --file-type json conllu/no-all-train.conllu json
python3 -m spacy convert --file-type json conllu/no-all-dev.conllu json

python3 -m spacy train nb --version=0.0.1 --vectors=models/nb_vectors_nowac_md models/no_ud_all_md json/no-all-train.json json/no-all-dev.json
```