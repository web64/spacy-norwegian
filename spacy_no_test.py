#!/usr/bin/env python
# coding: utf8

import spacy

# Update model path to the one you want to test
Norwegian = spacy.load("models/no_ud_nowac_md/model-best")

# From: https://no.wikipedia.org/wiki/Erna_Solberg
text = """
Erna Solberg (født 24. februar 1961 i Bergen) er en norsk politiker (H). Hun har vært Norges statsminister siden 16. oktober 2013, partileder i Høyre siden 2004 og innvalgt på Stortinget fra Hordaland siden 1989.
Som kommunal- og regionalminister fra 2001 til 2005 arbeidet hun særlig for et styrket velferdstilbud innenfor rammen av færre og sterkere kommuner, og regionalt samarbeid på tvers av fylkeskommunene. Hun reformerte også den norske asyl-, flyktning- og innvandringspolitikken, og etablerte en fungerende praksis for rask behandling av asylsøknader uten grunnlag.[1] Siden hun tiltrådte som partileder i 2004 og parlamentarisk leder i 2005, har Solberg særlig betonet den sosiale delen av – og det verdimessige grunnlaget for – Høyres politikk. Partiet har også tatt en mer utpreget pragmatisk kurs.
Etter stortingsvalget i 2009 har oppslutningen rundt Høyre som parti og Solberg som statsministerkandidat steget betraktelig på meningsmålingene. Kommunestyre- og fylkestingsvalget i 2011 ble Høyres beste siden 1979. Foran stortingsvalget i 2013 var det et uttalt mål for Høyre å danne en koalisjonsregjering mellom Høyre, Fremskrittspartiet, Kristelig Folkeparti og Venstre med Solberg som statsminister. Valgresultatet gjorde det mulig for Erna Solberg å danne en regjering utgått fra Høyre og Fremskrittspartiet med en bindende avtale med støttepartiene Venstre og Kristelig Folkeparti.
"""

doc = Norwegian( text )

words  = {}
words['VERB']  = set()
words['NOUN']  = set()
verb_counter = 0
for token in doc:
    #print(token.text, token.lemma_, token.pos_, token.tag_, token.dep_, token.shape_, token.is_alpha, token.is_stop)
    if token.tag_ == 'VERB' or token.tag_ == 'NOUN':
        words[token.tag_].add( token.lemma_ )
        
print( "\n VERBs:" )
print( words['VERB'] )
print( "\n\n NOUNs:" )
print( words['NOUN']  )


print( "\n Entities:" )
for ent in doc.ents:
    print(ent.text, ent.start_char, ent.end_char, ent.label_)
