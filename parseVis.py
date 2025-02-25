from sys import exc_info
from re import search, findall, DOTALL, IGNORECASE
from json import dumps
from stUtil import rndrCode
#hgPttrn='.*(\d\d+/\d+).*(mmHg)'
#pttrnLEFT='(\d+\.?\d*/?\d+\.?\d*).*OD,?\s+(\w+\.?\d*/?\d+\.?\d*).*OS,?'
#rightPttrn='OD:?.*(\d+\.?\d*/?\d+\.?\d*).*,?\s?OS:?.*(\d+\.?\d*/?\d+\.?\d*).*,?'
#dcmlPttrn='(\d+\.?\d*/?\d+\.?\d*)'

def parseVis(outcome):
  spcfcIOP, sghtInfo=None, None
  #rndrCode([outcome])
  if isinstance(outcome, str) or isinstance(outcome, bytes): 客觀資料=findall('O:客觀資料\n(.*)\n\n', outcome, DOTALL|IGNORECASE)
  else: 客觀資料=findall('O:客觀資料\n(.*)\n\n', outcome[0], DOTALL|IGNORECASE)
  if 客觀資料:
    客觀資料=客觀資料[0]
    mtchODOSIOP=[x+y for x, y in findall('(CF|NLP|LP|HM|\d+\.?)(/?\d?\.?\d?[+-]?.*?)', 客觀資料, DOTALL) if search('/\d', y)]
    #mtchODOSIOP=[x for x in findall('(CF|NLP|LP|HM|\d+\.?)(/?\d?\.?\d?[+-]?.*?)', 客觀資料) if x.find('/')!=-1]
    if len(mtchODOSIOP)>=3:
      sghtInfo='|'.join(mtchODOSIOP[:3])
    else:
      #notice('客觀資料', 客觀資料, outcome)
      try:
        ODOSinfo, IOPinfo=findall('(.*OD.*OS.*?\n).*?\n?(.*IOP.*mmHg)?', 客觀資料, DOTALL|IGNORECASE)[0]  #'O:客觀資料\n(.*OD.*OS.*\n?).*?\n?(.*?IOP.*mmHg)?'    (.*OD.*OS.*?\n?).*?\n?(.*IOP.*mmHg)?
      #notice('IOPinfo', IOPinfo, 'ODOSinfo', ODOSinfo)
        if IOPinfo:
          #OD, OS=findall('\d+/\d+', ODOSinfo)
          notice('ODOSinfo', ODOSinfo)
          OD, OS=findall('(CF|NLP|LP|HM|\d+\.?)(/?\d?\.?\d?[+-]?.*?)', ODOSinfo)
          mtchIOP=findall('\d+/\d+', IOPinfo)[0]
        else:
          #rsltODSIOPinfo=findall('\d+/\d+', ODOSinfo)
          #rsltODSIOPinfo=findall('(CF|NLP|LP|HM|\d+\.?)(/?\d?\.?\d?[+-]?.*?)', ODOSinfo)
          rsltODSIOPinfo=[x+y for x, y in findall('(CF|NLP|LP|HM|\d+\.?)(/?\d?\.?\d?[+-]?.*?)', ODOSinfo, DOTALL) ]
          #notice('rsltODSIOPinfo', rsltODSIOPinfo)
          if len(rsltODSIOPinfo)>=3:
            OD, OS, mtchIOP=rsltODSIOPinfo[:3]
            sghtInfo='|'.join([OD, OS, mtchIOP])
      except: return None
        #else: OD, OS, mtchIOP=rsltODSIOPinfo
      #notice(rsltSght)
#for 客觀資料, IOPinfo in   #'O:客觀資料\n(.*?IOP.*?)\n' 'O:客觀資料\n(.*?)[\n]?(.*IOP.*mmHg)?\n' #O:客觀資料\n(.*)[\n]?(.*IOP.*mmHg)?
#if sghtInfo and search('\d{6,}', sghtInfo): sghtInfo=None
#if spcfcIOP:
  return sghtInfo if sghtInfo else None
