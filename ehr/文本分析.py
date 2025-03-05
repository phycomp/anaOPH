import spacy
from stUtil import rndrCode
from streamlit import write as rndrCode, sidebar, session_state, code as stCode, info as stInfo
from spacy.lang.en import English
MENUs=['ENT', 'SENT', 'tokenizer', 'punct', 'fastText', 'csvEye', 'answerQuestion', 'ansQues2', 'fastChat', 'optimizer','BILUO', 'vocab', 'word2vec'] #EMBEDDING
from spacy.lang.en.stop_words import STOP_WORDS

def spcyTknzr(sentence):
    mytokens = parser(sentence)
    mytokens = [ word.lemma_.lower().strip() if word.lemma_ != "-PRON-" else word.lower_ for word in mytokens ]
    mytokens = [ word for word in mytokens if word not in stpWrds and word not in PUNCT ]
    return mytokens

try: stpWrds=session_state['STOP_WORDS']
except: session_state['STOP_WORDS']=stpWrds=list(STOP_WORDS)
try: lngMDL=session_state['lngMDL']
except:
    session_state['lngMDL']=lngMDL=spacy.blank("en")
    #nlp = spacy.load('en')

try: PUNCT=session_state['punct']
except:
    import string
    session_state['punct']=PUNCT=string.punctuation
try:parser=session_state['parser']
except:session_state['parser']=parser=English()
#nlp = spacy.load("en_core_web_sm")
try: pthlgyCntxt=session_state['pthlgyCntxt']
except:
    pthlgyCntxt=session_state['pthlgyCntxt']='''O:客觀資料
VA: 6/15 naked eye, 6/12 with PH, OD, 6/60cc OS, IOP: 17/20 mmHg
'''
    #pthlgyCntxt
try: doc=session_state['DOC']
except:
    session_state['DOC']=doc=lngMDL(pthlgyCntxt)
#doc = nlp("I like spaCy")
#rndrCode('<style>div[role=radiogroup]{flex-direction:row; justify-content:space-between} code{white-space: pre-wrap !important;}</style>', unsafe_allow_html=True)
with sidebar:
  menu = radio('Output', MENUs, index=0)

if menu==MENUs[0]:
    rndrCode(list(doc.ents)) #要得出ents
    trainData=session_state['trainData']
    stInfo([trainData])
elif menu==MENUs[1]:
    rndrCode(list(doc.sents))
#MY_PRODUCT = nlp.vocab.add_flag(is_my_product)
#assert doc[2].check_flag(MY_PRODUCT) == True
elif menu==MENUs[2]:
    tknzRslt=spcyTknzr(pthlgyCntxt)
    rndrCode(['tknzRslt', tknzRslt])
elif menu==MENUs[3]:
    rndrCode(['PUNCT', PUNCT])
elif menu==MENUs[4]:
    #rndrCode(['fastText'])
    from gensim.models import FastText
    from gensim.test.utils import common_texts  # some example sentences
    #print(common_texts[0]) ['human', 'interface', 'computer']
    #print(len(common_texts)) 9
    ftMDL = FastText(vector_size=4, window=3, min_count=1)  # instantiate
    ftMDL.build_vocab(corpus_iterable=pthlgyCntxt)
    ftMDL.train(corpus_iterable=pthlgyCntxt, total_examples=len(pthlgyCntxt), epochs=10)  # train
    #sntncCrps = [ pthlgyCntxt.split() ]
    #fstxtMDL = FastText(min_count=1)
    #fstxtMDL.build_vocab(sntncCrps)
    #fstxtMDL.train(sntncCrps, total_examples=fstxtMDL.corpus_count, epochs=fstxtMDL.epochs)
    stInfo(['naked', ftMDL.wv.vectors])  #wordEmbedding .vectors ['naked']
elif menu==MENUs[5]:
    'csvEye'
elif menu==MENUs[6]:
    'answerQuestion'
    train='''id,package_name,review,date,star,version_id
    7bd227d9-afc9-11e6-aba1-c4b301cdf627,com.mantz_it.rfanalyzer,Great app! The new version now works on my Bravia Android TV which is great as it's right by my rooftop aerial cable. The scan feature would be useful...any ETA on when this will be available? Also the option to import a list of bookmarks e.g. from a simple properties file would be useful.,October 12 2016,4,1487
    7bd22905-afc9-11e6-a5dc-c4b301cdf627,com.mantz_it.rfanalyzer,Great It's not fully optimised and has some issues with crashing but still a nice app  especially considering the price and it's open source.,August 23 2016,4,1487
    7bd2299c-afc9-11e6-85d6-c4b301cdf627,com.mantz_it.rfanalyzer,Works on a Nexus 6p I'm still messing around with my hackrf but it works with my Nexus 6p  Trond usb-c to usb host adapter. Thanks!,August 04 2016,5,1487
    7bd22a26-afc9-11e6-9309-c4b301cdf627,com.mantz_it.rfanalyzer,The bandwidth seemed to be limited to maximum 2 MHz or so. I tried to increase the bandwidth but not possible. I purchased this is because one of the pictures in the advertisement showed the 2.4GHz band with around 10MHz or more bandwidth. Is it not possible to increase the bandwidth? If not  it is just the same performance as other free APPs.,July 25 2016,3,1487
    7bd22aba-afc9-11e6-8293-c4b301cdf627,com.mantz_it.rfanalyzer,Works well with my Hackrf Hopefully new updates will arrive for extra functions,July 22 2016,5,1487'''
    from pandas import DataFrame, read_csv
    from streamlit import dataframe
    from io import StringIO
    trnStng=StringIO(train)
#bIO=ByteIO(train)
    trnCSV=read_csv(trnStng)
    dataframe(trnCSV)
#trainDF=DataFrame.from_dict({'眼科':trnCSV})
#dataframe(trainDF)
elif menu==MENUs[-6]:
    train='''Context: 'Architecturally, the school has a Catholic character. Atop the Main Building\'s gold dome is a golden statue of the Virgin Mary. Immediately in front of the Main Building and facing it, is a copper statue of Christ with arms upraised with the legend "Venite Ad Me Omnes". Next to the Main Building is the Basilica of the Sacred Heart. Immediately behind the basilica is the Grotto, a Marian place of prayer and reflection. It is a replica of the grotto at Lourdes, France where the Virgin Mary reputedly appeared to Saint Bernadette Soubirous in 1858. At the end of the main drive (and in a direct line that connects through 3 statues and the Gold Dome), is a simple, modern stone statue of Mary.'
Question: 'To whom did the Virgin Mary allegedly appear in 1858 in Lourdes France?'
Answer: {'text': ['Saint Bernadette Soubirous'], 'answer_start': [515]}'''
    dset='''#train=id,package_name,review,date,star,version_id
7bd22c54-afc9-11e6-98dc-c4b301cdf627,com.mantz_it.rfanalyzer,Works with RTL and Nextbook Aries 8. Demod stops working if the scan width is changed requiring restart.,May 19 2016,5,1487
7bd22cd9-afc9-11e6-9322-c4b301cdf627,com.mantz_it.rfanalyzer,Works with RTL SDR Works but no audio when demodulating,April 24 2016,3,1487
7bd22d59-afc9-11e6-a7a7-c4b301cdf627,com.mantz_it.rfanalyzer,Awsome App! Easy to use  works great on Notes w / Realtek dongle.,April 16 2016,5,1487
7bd22ddc-afc9-11e6-9a16-c4b301cdf627,com.mantz_it.rfanalyzer,I'll forgo the refund. But no go with Watson dongle... Nexus 9. Yet to try on Nexus 6p. So very disappointed!!! :-(,March 31 2016,1,1487
7bd22e5c-afc9-11e6-8a41-c4b301cdf627,com.mantz_it.rfanalyzer,looks like a great program  1 of its kind I don't have the necessary hardware to utilize it though.,March 30 2016,4,1487'''
    #features: ['id', 'title', 'context', 'question', 'answers'], 'ansQues2'

    rndrCode(train)
    #from pandas import DataFrame, read_csv
    #from streamlit import dataframe
    #from io import StringIO
    #trnStng=StringIO(train)
#bIO=ByteIO(train)
    #trnCSV=read_csv(trnStng)
    #dataframe(trnCSV)
elif menu==MENUs[-5]:
    'fastChat'
elif menu==MENUs[-4]:
    'optimizer'
    session_state['trainData']=trainData=[('6/6.7cc od, 6/10cc os IOP: 18/14mmHg\n', {'entities': [(0, 8, 'OD'), (10, 19, 'OS'), (25, 32, 'IOP')]}),
('OD 6/10cc OS 6/10cc; IOP:11/12mmHg\n', {'entities': [(2, 10, 'OD'), (12, 21, 'OS'), (24, 30, 'IOP')]}),
('6/12cc OD 6/6cc OS IOP:13/13mmHg\n', {'entities': [(0, 7, 'OD'), (9, 16, 'OS'), (22, 28, 'IOP')]}),
('6/10cgl OD, 6/12cgl OS, (1070111)\n IOP: 12/13mmHg', {'entities': [(0, 8, 'OD'), (10, 20, 'OS'), (38, 45, 'IOP')]}),
('1/60cc,OD 6/20cc,OS   IOP: 17/19mmHg\n', {'entities': [(0, 7, 'OD'), (9, 17, 'OS'), (25, 32, 'IOP')]}),
('6/30 ccOD, 6/30cc OS, IOP 11/11 mmHg\n', {'entities': [(0, 7, 'OD'), (9, 18, 'OS'), (25, 32, 'IOP')]}),
('6/7.5cc(-0.2-0.25x6) OD, 6/6cc(-0.25) OS, IOP 21/23mmhg\n', {'entities': [(0, 21, 'OD'), (23, 38, 'OS'), (45, 51, 'IOP')]}),
('OD HM/50cm OS 6/60 cc  IOP 19/12 mmhg  elevated bleb,od>os\n', {'entities': [(2, 11, 'OD'), (13, 23, 'OS'), (26, 33, 'IOP')]}),
('OD:6/7.5cc  OS:6/10cc    IOP:  17/19 mmHg\n', {'entities': [(2, 12, 'OD'), (14, 25, 'OS'), (28, 37, 'IOP')]}),
('6/10ccOD, 6/6 OS; IOP 14/12mmHg\n', {'entities': [(0, 6, 'OD'), (8, 14, 'OS'), (21, 27, 'IOP')]}),
('6/12cgl OD, bulbar atrophy OS, IOP 20mmHg slitlamp: PCIOL OD, mild\n', {'entities': [(0, 8, 'OD'), (10, 27, 'OS'), (34, 37, 'IOP')]}),
('scularized cornea,OD>OS\nVA: LP,OD  2/60,OS  IOP: 10/14 mmHg\n', {'entities': [(0, 31, 'OD'), (33, 40, 'OS'), (47, 55, 'IOP')]}),
('OD CF/20CM, OS 6/20; IOP: 16/14 mmHg;\n', {'entities': [(2, 12, 'OD'), (14, 21, 'OS'), (24, 32, 'IOP')]}),
('6/7.5cc OD, 6/6cc OS, IOP: 17/18 mmHg\n', {'entities': [(0, 8, 'OD'), (10, 18, 'OS'), (25, 33, 'IOP')]}),
('6/10cc OD, 6/6.7cc OS, IOP 19/20mmHg\n', {'entities': [(0, 7, 'OD'), (9, 19, 'OS'), (26, 32, 'IOP')]}),
('6/6.7cc OD, 6/6cc OS, IOP: 19/19 mmHg\n', {'entities': [(0, 8, 'OD'), (10, 18, 'OS'), (25, 33, 'IOP')]}),
('OD HM/50cmOS 6/60cc,IOP16(17)/23(17)mmhg elevated bleb,od>os\n', {'entities': [(2, 10, 'OD'), (12, 20, 'OS'), (23, 36, 'IOP')]}),
('od 6/8.6+2.5-4.0x90, os 6/8.6+2.0-3.0x80  IOP 14/14 mmHg\n', {'entities': [(2, 21, 'OD'), (23, 42, 'OS'), (45, 52, 'IOP')]}),
('6/10cc od,6/6cc os    IOP: 14/16mmHg\n', {'entities': [(0, 7, 'OD'), (9, 16, 'OS'), (25, 32, 'IOP')]}),
(' 2/60cc OD, 4/60cc OS; IOP: 18/16 mmHg\n', {'entities': [(0, 8, 'OD'), (10, 19, 'OS'), (26, 34, 'IOP')]}),
('OD 2/60cc, OS 6/8.6c; IOP: 14/16mmHg; OCT:macular edema OD\n', {'entities': [(2, 11, 'OD'), (13, 22, 'OS'), (25, 32, 'IOP')]}),
('6/10cc OD, 6/8.6cc OS, IOP 15/16mmHg conj mild congested OU\n', {'entities': [(0, 7, 'OD'), (9, 19, 'OS'), (26, 32, 'IOP')]}),
('6/6CC OD   6/6CC OS   IOP 17/16mmHg\nlens: PCIOL with PCO OD>OS\n', {'entities': [(0, 6, 'OD'), (8, 17, 'OS'), (25, 31, 'IOP')]}),
('OD:6/8.6(-0.5-1.75x88),OS:6/7.5(-0.25-2.0x84) IOP:13/13,mmHg,\n', {'entities': [(2, 23, 'OD'), (25, 46, 'OS'), (49, 56, 'IOP')]}),
('6/7.5cc OD, 6/6cc OS, IOP 20/14 mmHg\n', {'entities': [(0, 8, 'OD'), (10, 18, 'OS'), (25, 32, 'IOP')]}),
('OD 6/20+0.75 OS 6/10+1.5-0.75x100 IOP:15/16mmHg\n', {'entities': [(2, 13, 'OD'), (15, 34, 'OS'), (37, 43, 'IOP')]}),
('6/7.5cc od   6/6cc os    iop 11/9mmHg\nlens: NS++ OU  pterygium OD>OS\n', {'entities': [(0, 8, 'OD'), (10, 19, 'OS'), (28, 33, 'IOP')]}),
('OD:6/30,OS:6/8.6cc  IOP:10/9 mmHg\n', {'entities': [(2, 8, 'OD'), (10, 20, 'OS'), (23, 29, 'IOP')]}),
('0.9 cc od, 1.0 cc os\nlens:NS++ od>os\n IOP:16/13 mmHg', {'entities': [(0, 31, 'OD'), (33, 34, 'OS'), (41, 48, 'IOP')]}),
('6/7.5cc OD, OS 6/10cc , IOP 17/18 mmHg\n', {'entities': [(0, 8, 'OD'), (10, 12, 'OS'), (27, 34, 'IOP')]}),
('6/60cc,od 6/20cc,os IOP:12/10mmHg\n', {'entities': [(0, 7, 'OD'), (9, 17, 'OS'), (23, 29, 'IOP')]}),
('OD 6/6cc OS 6/6cc IOP 13/17mmHg\n', {'entities': [(2, 9, 'OD'), (11, 16, 'OS'), (21, 27, 'IOP')]}),
('6/5igl OD, 6/5igl OS, IOP: 19/16mmHg\n', {'entities': [(0, 7, 'OD'), (9, 18, 'OS'), (25, 32, 'IOP')]}),
('OD 6/60cc,OS 6/10cc   IOP: 9/14mmHg\n', {'entities': [(2, 10, 'OD'), (12, 22, 'OS'), (25, 31, 'IOP')]}),
('6/60cc OD 6/6sc OS IOP:12/12mmHgh\n', {'entities': [(0, 7, 'OD'), (9, 16, 'OS'), (22, 28, 'IOP')]}),
('6/7.5sc od, 6/8.6sc os IOP: 17/15 mmHg\n', {'entities': [(0, 8, 'OD'), (10, 20, 'OS'), (26, 34, 'IOP')]}),
('6/7.5,od 6/6.7,os c gl IOP:17/19mmHg\n', {'entities': [(0, 6, 'OD'), (8, 15, 'OS'), (26, 32, 'IOP')]}),
('6/30cc OD, 6/6.7cc OS, IOP: 14/17 mmHg\n', {'entities': [(0, 7, 'OD'), (9, 19, 'OS'), (26, 34, 'IOP')]}),
('5/60nc(error) OD, 6/30cc OS, IOP: 18/17 mmHg\n', {'entities': [(0, 14, 'OD'), (16, 25, 'OS'), (32, 40, 'IOP')]}),
('od 6/15nc os 6/12nc; IOP 13/13 mmHg, mild congested conj OU\n', {'entities': [(2, 10, 'OD'), (12, 21, 'OS'), (24, 31, 'IOP')]}),
('6/12cc OD, 6/12cc OS, IOP: 19/22 mmHg\n', {'entities': [(0, 7, 'OD'), (9, 18, 'OS'), (25, 33, 'IOP')]}),
('od 6/12cc os 6/6cc IOP:11/16mmHg lens:NS++,ou\n', {'entities': [(2, 10, 'OD'), (12, 19, 'OS'), (22, 28, 'IOP')]}),
('6/5sc OD, 6/6sc OS, IOP: 22/(22)mmHg\nConj: congested OD>OS\n', {'entities': [(0, 6, 'OD'), (8, 16, 'OS'), (23, 32, 'IOP')]}),
('6/10cgl od, 6/12cgl os; IOP: 11/10 mmHg\nLens: NS+++PSCO+ od>os\n', {'entities': [(0, 8, 'OD'), (10, 20, 'OS'), (27, 35, 'IOP')]}),
('OD 6/6gl, OS 6/6gl; IOP: 13/14 mmHg  conj.: mild injected,ou\n', {'entities': [(2, 10, 'OD'), (12, 20, 'OS'), (23, 31, 'IOP')]}),
('OD 1/60cgl, OS 6/12cgl, IOP18/20mmhg\n', {'entities': [(2, 12, 'OD'), (14, 24, 'OS'), (27, 32, 'IOP')]}),
('CF/15CM,OD;6/20CC,OS NC,IOP 13/10mmHg, OU\n', {'entities': [(0, 8, 'OD'), (10, 18, 'OS'), (27, 33, 'IOP')]}),
('6/60 OD, 6/6 OS; IOP 15/15mmHg\n', {'entities': [(0, 5, 'OD'), (7, 13, 'OS'), (20, 26, 'IOP')]}),
('6/12cc OD, bulbar atrophy OS, NCTIOP: 25mmHg OD\n', {'entities': [(0, 7, 'OD'), (9, 26, 'OS'), (36, 40, 'IOP')]}),
('OD 6/20 cc, OS 6/12 cc, IOP 12/10 mmhg\nLens: NS++,OU,CO+,OD>OS,OU\n', {'entities': [(2, 12, 'OD'), (14, 24, 'OS'), (27, 34, 'IOP')]}),
('OD 6/6cc, OS 6/6cc, IOP: 15/14mmHg\n', {'entities': [(2, 10, 'OD'), (12, 18, 'OS'), (23, 30, 'IOP')]}),
('6/15cc OD, 6/6cgl OS, IOP 14/14mmHg\n', {'entities': [(0, 7, 'OD'), (9, 18, 'OS'), (25, 31, 'IOP')]}),
('6/6.7cc,od 6/6cc,os IOP:22/24mmHg, CCT 575/583um\n', {'entities': [(0, 8, 'OD'), (10, 17, 'OS'), (23, 29, 'IOP')]}),
('1/60cc OD, 6/30cc OS; IOP: 14/15 mmHg\n', {'entities': [(0, 7, 'OD'), (9, 18, 'OS'), (25, 33, 'IOP')]}),
('6/15cc,OD 6/12cc,OS  IOP:15/16mmHG\nLens: NS+CO+PSCO,OD>OS\n', {'entities': [(0, 7, 'OD'), (9, 17, 'OS'), (24, 30, 'IOP')]}),
('1/60cc OD 6/30cc OS  IOP: 16/15  mmHg\n', {'entities': [(0, 7, 'OD'), (9, 17, 'OS'), (24, 33, 'IOP')]}),
('6/30cgl od 6/5 cc os IOP:16/16 mmHg\n', {'entities': [(0, 8, 'OD'), (10, 18, 'OS'), (24, 31, 'IOP')]}),
(' 6/20 CC OD  6/8.6 CC OS    IOP 15/17 mmHg\n', {'entities': [(0, 9, 'OD'), (11, 22, 'OS'), (31, 38, 'IOP')]}),
('6/60cc OD, 6/30cc OS; IOP: 18/20 mmHg\n', {'entities': [(0, 7, 'OD'), (9, 18, 'OS'), (25, 33, 'IOP')]}),
('6/8.6 OD, 6/7.5nc os,\n ref +1.25-1.75x100/+0.75-0.25x20\nIOP 12/16mmHg', {'entities': [(0, 6, 'OD'), (8, 18, 'OS'), (59, 65, 'IOP')]}),
('OD 6/6cc OD , OS 6/6cc IOP 11/11mmHg\n', {'entities': [(2, 14, 'OD'), (16, 22, 'OS'), (26, 32, 'IOP')]}),
('OD 6/30cc OS 6/12cc IOP: 10/9mmHG\n', {'entities': [(2, 10, 'OD'), (12, 20, 'OS'), (23, 29, 'IOP')]}),
('6/60 cc od 6/6 cc os IOP: 17/14 mmhg\n', {'entities': [(0, 8, 'OD'), (10, 18, 'OS'), (24, 32, 'IOP')]}),
('6/6cc OD, 6/6 OS . NeumoIOP12/13 mmHg\n', {'entities': [(0, 6, 'OD'), (8, 14, 'OS'), (27, 33, 'IOP')]}),
('OD 6/8.6cc OS 6/7.5 CC,  IOP: 10/12mmHg\n', {'entities': [(2, 11, 'OD'), (13, 25, 'OS'), (28, 35, 'IOP')]}),
('OD 3/60cc OS 3/60cc IOP: 19/20 mmHg\n', {'entities': [(2, 10, 'OD'), (12, 20, 'OS'), (23, 31, 'IOP')]}),
('OD 6/10cc OS 6/6cc  IOP:15/15 mmhg\n', {'entities': [(2, 10, 'OD'), (12, 20, 'OS'), (23, 30, 'IOP')]}),
('OD 6/10cgl,OS 5/60cgl  IOP:17/18mmHg\n', {'entities': [(2, 11, 'OD'), (13, 23, 'OS'), (26, 32, 'IOP')]}),
#('OD: OS: IOP 14/14 mmHg\n', {'entities': [(2, 4, 'OD'), (2, 4, 'OS'), (11, 18, 'IOP')]}),
('6/60cc od; 4/60cc os,IOP: 17/14 mmHg\n', {'entities': [(0, 7, 'OD'), (9, 18, 'OS'), (24, 32, 'IOP')]}),
('6/10cc OD,6/12cc OS, IOP 17/18mmHg\n', {'entities': [(0, 7, 'OD'), (9, 17, 'OS'), (24, 30, 'IOP')]}),
('OD 6/30cc, OS 6/12cc, IOP: 16/16mmHg\n', {'entities': [(2, 11, 'OD'), (13, 22, 'OS'), (25, 32, 'IOP')]}),
('OD 6/30cc  OS 6/20cc  IOP 13/11 mmHg\n', {'entities': [(2, 11, 'OD'), (13, 22, 'OS'), (25, 32, 'IOP')]}),
('6/12cc OD, 6/7.5cc OS; IOP: 22/22 mmHg\n', {'entities': [(0, 7, 'OD'), (9, 19, 'OS'), (26, 34, 'IOP')]}),
('6/6cc od 6/6cc os ,IOP:10/12mmhg\n', {'entities': [(0, 6, 'OD'), (8, 15, 'OS'), (22, 28, 'IOP')]}),
('OD 6/6gl,OS 6/6.7gl   IOP: 17/15mmHg\n', {'entities': [(2, 9, 'OD'), (11, 22, 'OS'), (25, 32, 'IOP')]}),
('6/60-1c-3.5-7.0x85 OD, 6/30c-1.25-4.0x90 OS; IOP: 15/14 mmHg\n', {'entities': [(0, 19, 'OD'), (21, 41, 'OS'), (48, 56, 'IOP')]}),
('OD 6/8.6cc, OS 6/10cc, IOP;16/21mmHg\n', {'entities': [(2, 12, 'OD'), (14, 23, 'OS'), (26, 32, 'IOP')]}),
('6/6.7 cgl OD -1.25-2.5x82, 6/6cgl OS , IOP 21/16mmHg\n', {'entities': [(0, 10, 'OD'), (12, 34, 'OS'), (42, 48, 'IOP')]}),
('6/20+2sc 6/10cc OD, 6/20sc 6/12cc OS (1080227)\n IOP: mmHg', {'entities': [(0, 16, 'OD'), (18, 34, 'OS'), (51, 53, 'IOP')]}),
('6/30cc OD, 6/8.6cc OS, IOP:17/16mmHg\n', {'entities': [(0, 7, 'OD'), (9, 19, 'OS'), (26, 32, 'IOP')]}),
('6/7.5cc OD, 6/6cc OS< IOP 16/13mmHg\n', {'entities': [(0, 8, 'OD'), (10, 18, 'OS'), (25, 31, 'IOP')]}),
('OD 2/60cc OS 6/15cc IOP:16/16mmHg\n', {'entities': [(2, 10, 'OD'), (12, 20, 'OS'), (23, 29, 'IOP')]}),
('6/6cc OD 6/7.5cc OS, IOP: 19/18mmHg\n', {'entities': [(0, 6, 'OD'), (8, 17, 'OS'), (24, 31, 'IOP')]}),
('OD 6/15cc, OS 6/10cc; IOP: 16/15mmHg\n', {'entities': [(2, 11, 'OD'), (13, 22, 'OS'), (25, 32, 'IOP')]}),
('6/6.7cc od, 6/6.7cc os, IOP 13/13(N)14/18(G)mmHg\n', {'entities': [(0, 8, 'OD'), (10, 20, 'OS'), (27, 44, 'IOP')]}),
('OD 6/6.7 cc, OS 6/6 cc, IOP: 11/11 mmHg,\n', {'entities': [(2, 13, 'OD'), (15, 24, 'OS'), (27, 35, 'IOP')]}),
('OD 6/60c OS 6/12c  IOP:18/18mmHg  conj:mild injected,ou\n', {'entities': [(2, 9, 'OD'), (11, 19, 'OS'), (22, 28, 'IOP')]}),
('OD 6/12cc,OS 6/10cc,IOP:16/15mmHg\n', {'entities': [(2, 10, 'OD'), (12, 20, 'OS'), (23, 29, 'IOP')]}),
('6/15cc,OD 6/8.6cc,OS IOP: 18/16mmHg\n', {'entities': [(0, 7, 'OD'), (9, 18, 'OS'), (24, 31, 'IOP')]}),
('Mod CONGESTION,od>os, IOP 10/10 mmHg\n', {'entities': [(0, 15, 'OD'), (17, 18, 'OS'), (25, 32, 'IOP')]}),
('OD: 6/30cc (-17.5-1.25x40) OS: 6/20cc(-10.0-1.25x150) IOP: 13/12mmHg\n', {'entities': [(2, 27, 'OD'), (29, 54, 'OS'), (57, 64, 'IOP')]}),
('6/60 OD;  6/60 OS,   IOP:13/13mmHg\n', {'entities': [(0, 5, 'OD'), (7, 15, 'OS'), (24, 30, 'IOP')]}),
('6/12cc OD, bulbar atrophy OS, NCTIOP: 13mmHg OD\n', {'entities': [(0, 7, 'OD'), (9, 26, 'OS'), (36, 40, 'IOP')]}),
('6/12cc OD, 6/12cc OS, IOP: 19/22 mmHg\n', {'entities': [(0, 7, 'OD'), (9, 18, 'OS'), (25, 33, 'IOP')]}),
('6/6cc OD, 6/6cc OS,\n Ref:+0.5/+0.75-0.5x95\nNCTIOP= 14/13mmHg', {'entities': [(0, 6, 'OD'), (8, 16, 'OS'), (49, 56, 'IOP')]}),
('OD 6/5c-1.0-0.75x95 OS 6/6 IOP: 15/17mmHg\n', {'entities': [(2, 20, 'OD'), (22, 27, 'OS'), (30, 37, 'IOP')]}),
('6/12cc OD, 6/60cc OS, IOP 12/23mmHg\n', {'entities': [(0, 7, 'OD'), (9, 18, 'OS'), (25, 31, 'IOP')]}),
('OD 6/20cgl,OS 6/20cgl  IOP 13/13 mmHg\n', {'entities': [(2, 11, 'OD'), (13, 23, 'OS'), (26, 33, 'IOP')]}),
('6/15 cc OD 6/7.5 cc OS  IOP: 13/17mmHg\n', {'entities': [(0, 8, 'OD'), (10, 20, 'OS'), (27, 34, 'IOP')]}),
('6/7.5cc od,6/6.7cc os    IOP: 14/17 mmHg\n', {'entities': [(0, 8, 'OD'), (10, 19, 'OS'), (28, 36, 'IOP')]}),
('6/12cc OD, 6/6.7cc OS,  IOP 10/12mmHg,\n', {'entities': [(0, 7, 'OD'), (9, 19, 'OS'), (27, 33, 'IOP')]}),
('OD 6/10 OS 6/15 IOP 12/12mmHg\n', {'entities': [(2, 8, 'OD'), (10, 16, 'OS'), (19, 25, 'IOP')]}),
('OD 6/5cgl, OS 6/5cgl (1050608)\n IOP: 16/13mmHg', {'entities': [(2, 11, 'OD'), (13, 32, 'OS'), (35, 42, 'IOP')]}),
('6/20cc OD, 6/6cc OS  IOP: 10/9 mmHg\n', {'entities': [(0, 7, 'OD'), (9, 17, 'OS'), (24, 31, 'IOP')]}),
('OD 6/12cc, OS 6/7.5cc IOP: 15/17mmHg\n', {'entities': [(2, 11, 'OD'), (13, 22, 'OS'), (25, 32, 'IOP')]}),
('OD LP, OS 2/60 cc,\n IOP:\n18/19 mmHg', {'entities': [(2, 7, 'OD'), (9, 20, 'OS'), (23, 31, 'IOP')]}),
('OD:6/60 OS: 6/6cc, IOP:13/15mmHg\n', {'entities': [(2, 8, 'OD'), (10, 19, 'OS'), (22, 28, 'IOP')]}),
('6/30cc OD 6/12cc OS IOP 11/11mmHg\n', {'entities': [(0, 7, 'OD'), (9, 17, 'OS'), (23, 29, 'IOP')]}),
('OD 6/30cc, OS 6/7.5cc, IOP:12/11mmHg\n', {'entities': [(2, 11, 'OD'), (13, 23, 'OS'), (26, 32, 'IOP')]}),
('6/60 od, NLP os IOP:23/6mmHg  bulbar atrophy os\n', {'entities': [(0, 5, 'OD'), (7, 13, 'OS'), (19, 24, 'IOP')]}),
('6/6.7cgl OD, 6/6 cgl OS\n IOP: 11/12 mmhg', {'entities': [(0, 9, 'OD'), (11, 21, 'OS'), (28, 36, 'IOP')]}),
('6/7.5 cc OD, 6/6.7 cc OS, IOP: mmHg\n', {'entities': [(0, 9, 'OD'), (11, 22, 'OS'), (29, 31, 'IOP')]}),
('OD 6/10cc OS 6/10cc IOP 12/14 mmHg\n', {'entities': [(2, 10, 'OD'), (12, 19, 'OS'), (23, 30, 'IOP')]}),
('6/5cc OD,6/5cc OS\n IOP:15/16mmHg', {'entities': [(0, 6, 'OD'), (8, 15, 'OS'), (22, 28, 'IOP')]}),
('6/6cc OD, 6/6cc OS, IOP: 16/17 mmHg\n', {'entities': [(0, 6, 'OD'), (8, 16, 'OS'), (23, 31, 'IOP')]}),
('6/10(+3.00-0.75x20) OD, 6/6.7cc (+1.50-1.00x40) OS, IOP: 14/15 mmHg,\n', {'entities': [(0, 20, 'OD'), (22, 48, 'OS'), (55, 63, 'IOP')]}),
('OD 6/10c+2.75/0.5/80.,OS:6/10c+1.25\n IOP 24/14mmHg--27mmHg', {'entities': [(2, 22, 'OD'), (24, 37, 'OS'), (40, 54, 'IOP')]}),
('6/60cc od , 6/15cc os  IOP:14/14 mmHg\n', {'entities': [(0, 7, 'OD'), (9, 19, 'OS'), (26, 33, 'IOP')]}),
('OD 6/5cc OS 6/5cc, IOP: 19/18mmHg\n', {'entities': [(2, 9, 'OD'), (11, 19, 'OS'), (22, 29, 'IOP')]}),
('6/7.5cc OD, 6/7.5cc OS, IOP 14/13mmHg\n', {'entities': [(0, 8, 'OD'), (10, 20, 'OS'), (27, 33, 'IOP')]}),
('6/15cc OD 6/20cc OS, IOP 18/16 mmHg\n', {'entities': [(0, 7, 'OD'), (9, 17, 'OS'), (24, 31, 'IOP')]}),
('6/60 6/15cc,OD 6/30 6/12cc,OS  IOP:15/13 mmhg\nlens:ns(+++),OD>OS\n', {'entities': [(0, 12, 'OD'), (14, 27, 'OS'), (34, 41, 'IOP')]}),
('OD 6/10cc OS 6/6cc\n IOP(pneumo):15/16mmHg', {'entities': [(2, 10, 'OD'), (12, 20, 'OS'), (23, 37, 'IOP')]}),
('6/20cc OD, 6/6.7cc OS,IOP= 18/20 mmHg\n', {'entities': [(0, 7, 'OD'), (9, 19, 'OS'), (25, 33, 'IOP')]}),
('OD 6/15, OS 6/6.7, IOP:21/22 mmHg\n', {'entities': [(2, 9, 'OD'), (11, 19, 'OS'), (22, 29, 'IOP')]}),
('OD 6/7.5cc,OS 6/6cc;IOP 13/13mmHg pseudophakia with clear media OU\n', {'entities': [(2, 11, 'OD'), (13, 20, 'OS'), (23, 29, 'IOP')]}),
('OD 6/8.6cc, OS 6/6.7cc   IOP:10/14mmHg\n', {'entities': [(2, 12, 'OD'), (14, 25, 'OS'), (28, 34, 'IOP')]}),
('6/20cc OD, 6/6.7cc OS; Lens: CO+++ OU  IOP:10/12mmHg\n', {'entities': [(0, 7, 'OD'), (9, 19, 'OS'), (42, 48, 'IOP')]}),
('6/6.7CC OD 6/6.7 CC OS , IOP: 17/17mmHg\n', {'entities': [(0, 8, 'OD'), (10, 20, 'OS'), (28, 35, 'IOP')]}),
('6/6ccOD, 6/6-2ccOS IOP: 21/20 mmHg\n', {'entities': [(0, 5, 'OD'), (7, 16, 'OS'), (22, 30, 'IOP')]})
]
    from random import shuffle as rndmShffle
    from spacy.util import minibatch, compounding
    from spacy.training import Example
    #db = DocBin()
    lngMDL=session_state['lngMDL']
    optimizer = lngMDL.initialize()
    #optimizer = lngMDL.initialize()
    #optimizer = lngMDL.begin_training()
    #optimizer = nlp.initialize()
    losses=1
    while losses<1E2:
      #optimizer = lngMDL.create_optimizer()
      losses += 1   #{}
      rndmShffle(trainData)
      #batches = minibatch(trainData, size=compounding(4., 32., 1.001)) # batch up the examples using spaCy's minibatch
      #sizes = compounding(4., 500., 1.001)
      #batches = minibatch(trainData, size=sizes)
      #for batch in batches:
        #texts, annotations = zip(*batch)
      for text, annotations in trainData:
        #stCode(['text, annotations=', text, annotations])
        doc=lngMDL.make_doc(text)
        example=Example.from_dict(doc, annotations) #.append()
        #lngMDL.update(texts, annotations, drop=.5, losses=losses)
        #stCode(['example=', example])
        lngMDL.update([example], sgd=optimizer) #, drop=.5, losses=losses
        #stCode(['losses=', losses])
        #losses=losses.get('ner')
    stCode(['lngMDL=', lngMDL])
    #try:
    #except:
    #    pass
    #    stCode(['no wvMDL'])
elif menu==MENUs[-3]:
    ##PUNCT
    rndrCode(['PUNCT', PUNCT])
elif menu==MENUs[-2]:
    #tokenizer = AutoTokenizer.from_pretrained(lngMDL)
    #enc = tokenizer.encode_plus(text)
    #enc.keys() #dict_keys(['input_ids', 'attention_mask'])
    #trgtDEST='vghBDC'
    from spacy.vocab import Vocab
    vcbInfo=pthlgyCntxt.split()
    vocab = Vocab(strings=vcbInfo)
    #assert len(nlp.vocab) > 0
    #apple = nlp.vocab.strings["apple"]
    #assert nlp.vocab[apple] == nlp.vocab["apple"]
    #oov = nlp.vocab.strings["dskfodkfos"]
    vocabBytes = vocab.to_bytes()
    #rndrCode([pthlgyCntxt])
    stInfo([[x for x in vocab.strings], vocabBytes.decode('utf-8', errors='ignore')])
    #stopWords = [lex for lex in lngMDL.vocab if lex.is_stop]
    #rndrCode([list(stopWords)])
    #apple = nlp.vocab.strings["apple"]
    #oov = nlp.vocab.strings["dskfodkfos"]
    #assert apple in nlp.vocab
    #assert oov not in nlp.vocab

elif menu==MENUs[-1]:
    #from gensim.models.word2vec import Text8Corpus, Word2Vec
    #embddgng=Word2Vec(pthlgyCntxt)
    #from gensim.test.utils import common_texts
    from gensim.models import Word2Vec
    import multiprocessing
    try:
        wvMDL=session_state['wvMDL']
    except:
        VECTOR_SIZE, MIN_COUNT, WINDOW, SG=100, 5, 3, 1
        wvMDL = Word2Vec(vector_size=VECTOR_SIZE, window=WINDOW, min_count=MIN_COUNT, sg=SG)   #sentences=pthlgyCntxt, 
        #model=Word2Vec(sent, min_count=1, size=50, workers=3, window=3, sg=1)
        #lngMDLwv=Word2Vec(sentences=pthlgyCntxt, vector_size=100, window=5, min_count=1, workers=4)
        #rndrCode('wv', lngMDLwv.corpus_count)  #wv.embedding
        cores = multiprocessing.cpu_count() # Count the number of cores in a computer
        stCode(['build_vocab, progress_per=10000, update=False', pthlgyCntxt])
        #for cntxt in pthlgyCntxt.split():
        #    stCode(['cntxt', cntxt])
        #lngMDLwv = Word2Vec(pthlgyCntxt, min_count=4)
        #lngMDLwv = Word2Vec(min_count=1, window=2, epochs=300, sample=6e-5, alpha=.03, min_alpha=.0007, negative=20, workers=cores-1)
# Building the Vocabulary Table: Word2Vec requires us to build the vocabulary table (simply digesting all the words and filtering out the unique words, and doing some basic counts on them):
        #lngMDLwv.build_vocab(pthlgyCntxt, progress_per=10000, update=False)
        wvMDL.build_vocab(pthlgyCntxt, update=False)
        #sentences=pthlgyCntxt, 
        wvMDL.train(pthlgyCntxt, total_examples=wvMDL.corpus_count, epochs=30, report_delay=1)
        session_state['wvMDL']=wvMDL
    rndrCode([wvMDL.wv.vectors])    #vectors wordEmbedding .__dict__
    #.corpus ', '.join(dir(lngMDLwv)),
    #model.save("word2vec.model")
    #rndrCode(embddgng)
    #from fasttext import FastText
    #fstxtMDL = FastText(pthlgyCntxt,  size=4, window=3, min_count=1, iter=10,min_n = 3 , max_n = 6,word_ngrams = 0)
    #fsEmbddng=fstxtMDL.wv.syn0_vocab  # 單詞的向量組 (5, 4)
    #rndrCode(['fsEmbddng', fsEmbddng])
    #add_lifecycle_event, add_null_word, alpha, batch_words, build_vocab, build_vocab_from_freq, cbow_mean, comment, compute_loss, corpus_count, corpus_total_words, create_binary_tree, cum_table, effective_min_count, epochs, estimate_memory, get_latest_training_loss, hashfxn, hs, init_sims, init_weights, layer1_size, lifecycle_events, load, make_cum_table, max_final_vocab, max_vocab_size, min_alpha, min_alpha_yet_reached, min_count, negative, ns_exponent, null_word, predict_output_word, prepare_vocab, prepare_weights, random, raw_vocab, reset_from, running_training_loss, sample, save, scan_vocab, score, seed, seeded_vector, sg, shrink_windows, sorted_vocab, syn1neg, total_train_time, train, train_count, update_weights, vector_size, window, workers, wv
    #seed = 666 sg = 0 window_size = 10 vector_size = 100 min_count = 1 workers = 8 epochs = 5 batch_words = 10000
    #train_data = word2vec.LineSentence('wiki_text_seg.txt')
    #model = Word2Vec(train_data, min_count=min_count, vector_size=vector_size, workers=workers, epochs=epochs, window=window_size, sg=sg, seed=seed, batch_words=batch_words)
    #from flair.embeddings import WordEmbeddings, DocumentPoolEmbeddings
    #gloveEmbddng = WordEmbeddings('glove')
    #docEmbddngs = DocumentPoolEmbeddings([gloveEmbddng])
    #stckedEmbddngs.embed(pthlgyCntxt)
    #document_embeddings.embed(pthlgyCntxt)
    #rndrCode(pthlgyCntxt.embedding)
    #emddngInfo=[]
    #for token in sentence:
    #  emddngInfo.append([token, token.embedding])
    #rndrCode(['sentence.embedding', emddngInfo, sentence.embedding])
