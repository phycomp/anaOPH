create or replace function "rtrvSght"(in "nhirdTbl" varchar default outcome, in "dfltSchm" varchar default 'nhird', in "flshSchm" boolean default false) RETURNS void AS $eyeSght$
#in "tblName" varchar default 'DTLFDEH', 
from plpy import cursor, execute, notice
from sys import exc_info
from re import search, findall, DOTALL, IGNORECASE

for IVIeyeInfo in findall('S:主觀資料\n(.*)\n\nO:', outcome, DOTALL):
  if eyeInfo:=findall('(IVI[ALEO]|PDT)(.*)', IVIeyeInfo, IGNORECASE):
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
          if oriSdate:=oType.get(otype):
            #oriSdate='|'.join(findall('\d{4,8}', oriSdate))
            fullSdate='|'.join([oriSdate,Sdate])
            oType[otype]=fullSdate
          else:
            #sdate='|'.join(map(prprDate, sdate))
            #sdate='|'.join(findall('\d{4,8}', sdate))
            if Sdate: oType[otype]=Sdate
        if oType: ivCtgry.update({ivctgry:oType})
    #rint(len(eyeInfo), eyeInfo, hist, ivCtgry)
    if ivCtgry: return (','.join([hist, dumps(ivCtgry)]))
    #if ivCtgry: fout.write(','.join([hist, dumps(ivCtgry)])+'\n')

$eyeSght$ LANGUAGE plpython3u
