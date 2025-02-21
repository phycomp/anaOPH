create or replace function "打針"(in outcome varchar default 'outcome') RETURNS varchar AS $eyeSght$
#in "tblName" varchar default 'DTLFDEH', , in "dfltSchm" varchar default 'nhird', in "flshSchm" boolean default false
from plpy import cursor, execute, notice
from sys import exc_info
from re import search, findall, DOTALL, IGNORECASE
from json import dumps
def mergeEYE(原, 新):
    for 新針視, 新日期 in 新.items():  # 
        print('新針視, 新日期', 新針視, 新日期)
        原日期=原.get(新針視)
        if 原日期:
            mergeDATE=set()
            #if 新日期:=新視日.get(原左右):
            print(新日期, 原日期)
            [mergeDATE.add(date) for date in 新日期]
            [mergeDATE.add(date) for date in 原日期]
            原.update({新針視:mergeDATE})
        else:
            原.update({新針視:新日期})
    return 原

def rtrvODUS(打針, ODUSinfo):
    odusPttrn=findall('(O[DUS])(.*?)', ODUSinfo, IGNORECASE)
    #print('odusPttrn', odusPttrn)
    odusPttrnLEN=len(odusPttrn)
    odusRTRV={}
    print('odusPttrn', odusPttrn, ODUSinfo)
    for ndx, (x, _) in enumerate(odusPttrn):
        if not ndx:    #第0
            if odusPttrnLEN==1:
                outPttrn=search(f'({x}.*?)', ODUSinfo).group(1)
            else:
                outPttrn=search(f'({x}.*?){odusPttrn[1][0]}', ODUSinfo).group(1)
        elif ndx==odusPttrnLEN-1: #lastNDX 最後
            outPttrn=search(f'({x}.*)', ODUSinfo).group(1)
        else:
            mtchPttrn=f'({x}.*?){odusPttrn[ndx+1][0]}'
            #print(mtchPttrn)
            outPttrn=search(mtchPttrn, ODUSinfo).group(1)
        oriOutcome=ODUSinfo
        ODUSinfo=ODUSinfo.replace(outPttrn, '')
        print('equalPttrn', outPttrn+ODUSinfo==oriOutcome, '|'.join([outPttrn, ODUSinfo, oriOutcome]))
        odusDATE=findall('\d{7,}|\d+/\d+/\d+', outPttrn)
        #odusRTRV[x]='|'.join(odusDATE)
        x=x.upper()
        finalKEY='|'.join([打針,x])
        視日=odusRTRV.get(finalKEY)
        if 視日:
            DATE=set()
            [DATE.add(date) for date in 視日]  #.split('|')
            [DATE.add(date) for date in odusDATE]
            #合併視日=更新視力(視日, ODUSinfo)
            #odusRTRV.update({x:'|'.join(DATE)})
            odusRTRV.update({finalKEY:list(DATE)})
        else:
            odusRTRV.update({finalKEY:odusDATE})
            #odusRTRV.update({x:'|'.join(odusDATE)})
        #print('odusRTRV', odusRTRV)
         #print(ndx, 'outPttrn', outPttrn)
    return odusRTRV

def rtrvIVI(partOutcome):
    #partOutcome='IVIL (c) OU 1070801, (sp-1)1071003, 1071114, 1071212, 1080327, 1080508, IVIE OS on 1071114, 1071212, 1080327, 1080508, 107/06/26 PDT OS+ IVL (SP) OU'
    iviPttrn=findall('(IVI-?[ALEO]|PDT)(.*?)', partOutcome, DOTALL|IGNORECASE)
    #print('iviPttrn', iviPttrn)
    iviPttrnLEN, iviRTRV, ODUSinfo=len(iviPttrn), {}, {}
    for ndx, (x, _) in enumerate(iviPttrn):
        if not ndx:
            if iviPttrnLEN==1:
                outPttrn=search(f'({x}.*)', partOutcome).group(1)
            else:
                outPttrn=search(f'({x}.*){iviPttrn[1][0]}', partOutcome).group(1)
        elif ndx==iviPttrnLEN-1: #lastNDX 最後
            outPttrn=search(f'({x}.*)', partOutcome).group(1)
        else:
            mtchPttrn=f'({x}.*){iviPttrn[ndx+1][0]}'
            #print(mtchPttrn)
            outPttrn=search(mtchPttrn, partOutcome).group(1)
        #iviRTRV=rtrvODUS(x, outPttrn.replace(x, ''))
        #iviRTRV=ODUSinfo
        if not iviRTRV: iviRTRV=rtrvODUS(x, outPttrn.replace(x, ''))
        else: iviRTRV=mergeEYE(iviRTRV, rtrvODUS(x, outPttrn.replace(x, '')))
        #else: iviRTRV=mergeIVI(iviRTRV, {x:ODUSinfo})
        #print('ODUSinfo', ODUSinfo)
        #oriOutcome=partOutcome
        partOutcome=partOutcome.replace(outPttrn, '')
        #print('equalPttrn==>', outPttrn+partOutcome==oriOutcome, '|'.join([outPttrn, partOutcome, oriOutcome]))
        #print('partOutcome', partOutcome)
    return iviRTRV

def parseEYE(outcome):
  from sys import argv
  #outcome=open(argv[1]).read()
  #print('outcome', outcome)
  eyeFULL={}
  for infoEYE in findall('S:主觀資料(.*?)\n\n', outcome, DOTALL):
      for eyeIVI in map(lambda x:x.replace('\n', ' '), infoEYE.split('s/p')):
          if eyeIVI.find('IVI')!=-1:
              print('rtrvIVI',  eyeIVI, rtrvIVI(eyeIVI))
              #eyeFULL=rtrvIVI(eyeIVI)
              if not eyeFULL: eyeFULL=rtrvIVI(eyeIVI)
              else:
                  eyeFULL=mergeEYE(eyeFULL, rtrvIVI(eyeIVI))
              #    #eyeFULL.update(newEYE)
  return dumps(eyeFULL)
$eyeSght$ LANGUAGE plpython3u
