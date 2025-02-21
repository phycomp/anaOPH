create or replace function "rtrvSght2"(in outcome varchar default 'outcome') RETURNS varchar AS $eyeSght$
#in "tblName" varchar default 'DTLFDEH', , in "dfltSchm" varchar default 'nhird', in "flshSchm" boolean default false
from plpy import cursor, execute, notice
from sys import exc_info
from re import search, findall, DOTALL, IGNORECASE
from json import dumps

iviInfo, sghtInfo=None, None
for IVIeyeInfo in findall('S:主觀資料\n(.*)\n\nO:', outcome, DOTALL):
  eyeInfo=findall('(IVI[ALEO]|PDT)(.*)', IVIeyeInfo, IGNORECASE)
  if eyeInfo:
    ivCtgry, oType={}, {}
    for ivctgry, sdateInfo in eyeInfo:
      for otype, _, infoDate in findall('(O[SDU]) (on )?(.*)', sdateInfo):
        for year, month, day in findall('(\d+)[-/]?(\d+)[-/]?(\d+)', infoDate):#\d{5,8}year, month, day(\d{2,4})[-/]?(\d{1,2})[-/]?(\d{1,2})
          #print(year, month, day)
          dateInfo=f'{year}{month}{day}'
          lenDate=len(dateInfo)
          if lenDate==8: year, month, day=search('(\d{4})[-/]?(\d{2})[-/]?(\d{2})', dateInfo).groups()#.replace('-', '0').replace('/', '0')
          elif lenDate==7: year, month, day=search('(\d{3})[-/]?(\d{2})[-/]?(\d{2})', dateInfo).groups()
          elif lenDate==6: 
            year, month, day=search('(\d{2})[-/]?(\d{2})[-/]?(\d{2})', dateInfo).groups()
            if int(year)<=21:year=f'20{year}'
            if int(month)>12: year, month, day=search('(\d{3})[-/]?(\d{1})[-/]?(\d{2})', dateInfo).groups()
          elif lenDate==5:
            year, month, day=search('(\d{3})[-/]?(\d)[-/]?(\d)', dateInfo).groups()
            if int(year)>110: year, month, day=search('(\d{2})[-/]?(\d)[-/]?(\d\d)', dateInfo).groups()
          elif lenDate==4:
            year, month, day=search('(\d{2})[-/]?(\d)[-/]?(\d)', dateInfo).groups()
            if int(year)<21: year=2010
          
          if len(str(year))<=3: year=int(year)+1911
          if len(str(month))==1: month=month.zfill(2)
          if len(str(day))==1: day=day.zfill(2)
          #print(year, month, day)
          Sdate=f'{year}{month}{day}'
          oriSdate=oType.get(otype)
          if oriSdate:
            #oriSdate='|'.join(findall('\d{4,8}', oriSdate))
            fullSdate='|'.join([oriSdate,Sdate])
            oType[otype]=fullSdate
          else:
            #sdate='|'.join(map(prprDate, sdate))
            #sdate='|'.join(findall('\d{4,8}', sdate))
            if Sdate: oType[otype]=Sdate
        if oType: ivCtgry.update({ivctgry:oType})
    #rint(len(eyeInfo), eyeInfo, hist, ivCtgry)
    if ivCtgry:
      iviInfo=dumps(ivCtgry)#','.join([hist, dumps(ivCtgry)])
      #notice(dumps(ivCtgry))#','.join([hist, dumps(ivCtgry)]))
    #if ivCtgry: fout.write(','.join([hist, dumps(ivCtgry)])+'\n')
hgPttrn='.*(\d\d+/\d+).*(mmHg)'
pttrnLEFT='(\d+\.?\d*/?\d+\.?\d*).*OD,?\s+(\w+\.?\d*/?\d+\.?\d*).*OS,?'
rightPttrn='OD:?.*(\d+\.?\d*/?\d+\.?\d*).*,?\s?OS:?.*(\d+\.?\d*/?\d+\.?\d*).*,?'
dcmlPttrn='(\d+\.?\d*/?\d+\.?\d*)'
for 客觀資料 in findall('O:客觀資料\n(.*?)\n', outcome, DOTALL):
  ntRslt=[]
  for line in 客觀資料.split('\n'):
    rslt=findall('\w+\.?/?\d?\.?\d?', line)#, IGNORECASE) rtrvODOS
    for vl in rslt:
      if search('\d', vl): ntRslt.append(vl)
      elif search('NLP|LP|HM|CF', vl): ntRslt.append(vl)
    lenRSLT=len(ntRslt)
    if lenRSLT>3:
      cmbPttrnRlst=findall(rightPttrn+hgPttrn, outcome)
      if cmbPttrnRlst:
        #print('cmbRIGHT', outcome, cmbPttrnRlst)
        sghtInfo='|'.join(cmbPttrnRlst[0])
      cmbPttrnRlst=findall(pttrnLEFT+hgPttrn, outcome)
      if cmbPttrnRlst:
        sghtInfo='|'.join(cmbPttrnRlst[0])
        #print('cmbLEFT', outcome, cmbPttrnRlst)
      cmbPttrnRlst=findall(pttrnLEFT, outcome)
      if cmbPttrnRlst:
        sghtInfo='|'.join(cmbPttrnRlst[0])
        #print('LEFTcmb', outcome, cmbPttrnRlst)
      else:
        #print('rightPttrn', outcome, 
        pttrnRslt=findall(f'O[DS]:?\s?{dcmlPttrn}', outcome, IGNORECASE)
        if pttrnRslt: sghtInfo='|'.join(pttrnRslt)
    elif lenRSLT==3:
      #print('3rslt od, os, mmHg', ntRslt)
      sghtInfo='|'.join(ntRslt)
      #print(f'{outcome}==>', '|'.join(ntRslt))
    elif lenRSLT==2:
      sghtInfo='|'.join(ntRslt)
      #print('2rslt od, os', ntRslt)
if sghtInfo and search('\d{6,}', sghtInfo): sghtInfo=None
if iviInfo:
  return f'{iviInfo}@{sghtInfo}' if sghtInfo else iviInfo
else: return sghtInfo if sghtInfo else None

$eyeSght$ LANGUAGE plpython3u
