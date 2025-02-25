#!/usr/bin/env python
# coding: utf-8
from stUtil import rndrCode

from re import findall, search, DOTALL, IGNORECASE, split
from sys import argv, stdin

def rtrvIVI(partOutcome):
    #search('IVI-?\(?[EALO]\)?', otucome).group()
    iviPttrn=findall('(IVI\(?-?[EALO]\)?|PDT)(.*?)', partOutcome, DOTALL|IGNORECASE)
    iviPttrnLEN, iviRTRV, ODUSinfo=len(iviPttrn), {}, {}
    for ndx, (x, _) in enumerate(iviPttrn):
        if not ndx:    #第0
          if iviPttrnLEN==1: outPttrn=search(f'({x}.*)', partOutcome).group(1)
          else: outPttrn=search(f'({x}.*){iviPttrn[1][0]}', partOutcome).group(1)
        elif ndx==iviPttrnLEN-1: #lastNDX 最後
          outPttrn=search(f'({x}.*)', partOutcome).group(1)
        else:
          mtchPttrn=f'({x}.*){iviPttrn[ndx+1][0]}'
          if mtch:=search(mtchPttrn, partOutcome):
            outPttrn=mtch.group(1)
        #iviRTRV=rtrvODUS(x, outPttrn.replace(x, ''))
        #iviRTRV=ODUSinfo
        #print(iviRTRV)
        if not iviRTRV:
          rndrCode([outPttrn, x])
          iviRTRV=rtrvODUS(x, outPttrn.replace(x, ''))
        else:
          iviRTRV=mergeEYE(iviRTRV, rtrvODUS(x, outPttrn.replace(x, '')))
        #else: iviRTRV=mergeIVI(iviRTRV, {x:ODUSinfo})
        #print('ODUSinfo', ODUSinfo)
        #oriOutcome=partOutcome
        partOutcome=partOutcome.replace(outPttrn, '')
        #print('equalPttrn', outPttrn+partOutcome==oriOutcome, '|'.join([outPttrn, partOutcome, oriOutcome]))
        #print('partOutcome', partOutcome)
    return iviRTRV

def rtrvODUS(打針, ODUSinfo):
    odusPttrn=findall('(O[DUS])(.*?)', ODUSinfo, IGNORECASE)
    odusPttrnLEN=len(odusPttrn)
    odusRTRV={}
    for ndx, (x, _) in enumerate(odusPttrn):
        if not ndx:    #第0
            if odusPttrnLEN==1:
                outPttrn=search(f'({x}.*)', ODUSinfo).group(1)
            else:
                outPttrn=search(f'({x}.*){odusPttrn[1][0]}', ODUSinfo).group(1)
        elif ndx==odusPttrnLEN-1: #lastNDX 最後
            outPttrn=search(f'({x}.*)', ODUSinfo).group(1)
        else:
            mtchPttrn=f'({x}.*){odusPttrn[ndx+1][0]}'
            outPttrn=search(mtchPttrn, ODUSinfo).group(1)
        odusDATE=findall('\d{7,}|\d+/\d+/\d+', outPttrn)
        #odusRTRV[x]='|'.join(odusDATE)
        x=x.upper()
        finalKEY='|'.join([打針,x])
        if 視日:=odusRTRV.get(finalKEY):
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
        #oriOutcome=ODUSinfo
        ODUSinfo=ODUSinfo.replace(outPttrn, '')
        #print('equalPttrn', outPttrn+ODUSinfo==oriOutcome, '|'.join([outPttrn, ODUSinfo, oriOutcome]))
    return odusRTRV
def rinseDT(日期打針):
    neatDT=日期打針.split(',')
    neatDT=list(set(neatDT))
    #sorted(neatDT)
    neatDT.sort()
    neatDT=','.join(neatDT)
    return neatDT
def mergeEYE(eyeFULL):
  fnlEye={}
  for dt in eyeFULL:
    打針資訊=dt.split('|')
    mDT=打針資訊[-1]
    eye='|'.join(打針資訊[:-1])
    if 日期打針:=fnlEye.get(eye): 日期打針+=f',{mDT}'
    else: 日期打針=mDT
    neatDT=rinseDT(日期打針)
    fnlEye[eye]=neatDT    #日期打針
  return fnlEye
def rinseDT2():
  for k in fnlEye:
    日期打針=fnlEye[k]
    neatDT=日期打針.split(',')
    neatDT=list(set(neatDT))
    #sorted(neatDT)
    neatDT.sort()
    neatDT=','.join(neatDT)
    fnlEye[k]=neatDT    #日期打針
  return fnlEye
def mergeEYEII(原, 新):
    for 新針視, 新日期 in 新.items():  # 
        if 原日期:=原.get(新針視):  #{'IVIL|OU': ['1070801',  '1071003',  '1071114',  '1071212',  '1080327',  '1080508',  '107/6/26']}
            mergeDATE=set()
            #if 新日期:=新視日.get(原左右):
            [mergeDATE.add(date) for date in 新日期]
            [mergeDATE.add(date) for date in 原日期]
            原.update({新針視:mergeDATE})
        else:
            原.update({新針視:新日期})
    return 原
def rtrvEYE(outcome):
  eyeFULL={}
  #for infoEYE in findall('S:主觀資料(.*?)\n\n', eyeSOAP, DOTALL):
  spltOut=outcome.split('s/p')
  #rndrCode([len(spltOut), spltOut])   #outcome.split('s/p')
  for eyeIVI in spltOut:   #outcome.split('s/p')map(lambda x:x.replace('\n', ' '), ):
    rndrCode(['eyeIVI search=', eyeIVI])
    if search('IVI', eyeIVI, IGNORECASE|DOTALL):
      #print('rtrvIVI', rtrvIVI(eyeIVI))
      #eyeFULL=rtrvIVI(eyeIVI)
      if not eyeFULL: eyeFULL=rtrvIVI(eyeIVI)
      else:
        eyeFULL=mergeEYE(eyeFULL, rtrvIVI(eyeIVI))
      #    #eyeFULL.update(newEYE)
      #print('eyeFULL', eyeFULL)
  return eyeFULL
def dtYear():
  from datetime import datetime
  dtNow=datetime.now()
  return dtNow.year
def 民國to西元(eyeDate):    #, curYear
  rndrCode(['eyeDate=', eyeDate])
  #if len(eyeDate)==1: Year, Month, Day=eyeDate[0]
  #else: 
  RAW, raw, Year, Month, Day=eyeDate
  if not RAW:
    if len(Year)<=3: Year=int(Year)+1911
    Month=Month.zfill(2)
    Day=Day.zfill(2)
  elif not Year and not Month and not Day and RAW:
    if len(RAW)==7: Year, Month, Day=RAW[:3], RAW[3:5], RAW[5:]
    if len(RAW)==6: #Year, Month, Day=allDate[:3], allDate[3:5], allDate[5:]
      Year, Month, Day=findall('..', RAW)
    Year=int(Year)+1911
    if Year in [1931, 1932]:
      return ''
      #Year, Month, Day=RAW[:4], RAW[4:5], RAW[-2:]
  #if len(Year)==2: 
  #if (len(Year)==3 and len(Month)==2 and len(Day)==1) or (len(Year)==4 and len(Month)==1 and len(Day)==1): #Year=int(Year)+1911   #.zfill(3)# Year=Year.zfill(3) int(Year)>=100
  #  allDate=''.join([Year, Month, Day])
  #  Year, Month, Day=findall('..', allDate)
  #if len(Year)==4 and len(Month)==2 and len(Day)==1:
  #  allDate=''.join([Year, Month, Day])
  #  Year, Month, Day=allDate[:3], allDate[3:5], allDate[5:]
  #if len(Month)==1: Month=Month.zfill(2)
  #if len(Day)==1: Day=Day.zfill(2)
  #rndrCode([eyeDate])
  #if len(Year)<=3: Year=int(Year)+1911
  #nDay=Day.zfill(2)
  #if int(nYear)>100:
  #  #rndrCode(['allDate', allDate])
  #  elif len(allDate)==7: Year, Month, Day=allDate[:3], allDate[3:5], allDate[5:]
  #Month=Month.zfill(2)
  #Day=Day.zfill(2)
  dateEye=''.join([str(Year), Month, Day])
  return dateEye
def rtrvEYE(outcome):
  eyeFULL, curYear=[], dtYear()
  for 主觀 in findall('S:主觀資料(.*?)\n\n', outcome, DOTALL):
    if search('IVI', 主觀, IGNORECASE|DOTALL):rndrCode('找到IVI')
    for eyeIVI in split('s/p', 主觀, flags=IGNORECASE):   #outcome.split('s/p') 主觀.split('S/P')
      #rndrCode(['eyeIVI search=', eyeIVI])
      #出現錯誤==>s/p IVIE(f) OS on 1080722, IVIL NHI 1# OS on 1080819 NHI 2# 1080916 3#L OS 1081105
      #if search('IVI', eyeIVI, IGNORECASE|DOTALL):
      #if iviPttrn:=findall(r'(IVI\s?-?[EALO]|PDT).*?(O[DUS])?\s?(.*)', eyeIVI, DOTALL|IGNORECASE):
      if iviPttrn:=findall(r'(IVI[ -]?[EALO]|PDT).*?(O[DUS])(.*)', eyeIVI, DOTALL|IGNORECASE):   #正確版本
        rndrCode([iviPttrn, eyeIVI])
        打針, 左右眼, 日期=iviPttrn[0]
        eyeDate=findall(r'(\d{6,7})|((?P<Year>\d{2,4})[/-]?(?P<Month>\d{1,2})[/-]?(?P<Day>\d{1,2}))', 日期)
        #if len(eyeDate)==1: dateEye=民國to西元(eyeDate, curYear)
          #rndrCode(['<=3', 日期, eyeDate])
        #rndrCode(['>3', 日期, eyeDate])
        if not eyeDate: continue
        eyeDate=[民國to西元(dt) for dt in eyeDate] #map(, eyeDate, args=curYear)    , curYear
        dateEye=','.join(eyeDate)
        #針視日期='|'.join([打針, 左右眼, eyeDate])
        打針=''.join(filter(str.isalnum, 打針))
        針視日期='|'.join([打針, 左右眼, dateEye]) #replace(' ', '').replace('-', '').replace('(', '')
        eyeFULL.append(針視日期)
      elif iviPttrn:=findall(r'(IVI\s?-?[EALO]|PDT).*?(O[DUS])?\s?(.*)', eyeIVI, DOTALL|IGNORECASE):
        rndrCode(['group=', iviPttrn.groups()])

        #rndrCode([日期, 針視日期])#[打針, 左右眼, eyeDate]
      #iviPttrn
  eyeFULL=mergeEYE(eyeFULL)
  return eyeFULL
      #eyeFULL=rtrvIVI(eyeIVI)

def rtrvEYE(outcome):
  eyeFULL=[]
  #1. 先用s/p分成 2. 用打針IVI 3. 左右眼 4. 找出日期
  for 主觀 in findall('S:主觀資料(.*?)\n\n', outcome, DOTALL):
    #if search('IVI', 主觀, IGNORECASE|DOTALL):rndrCode('找到IVI')
    for eyeIVI in split('s/p', 主觀, flags=IGNORECASE):
      打針資訊=split('(IVI[- ]?[EAOL]|PDT|IVAS)', eyeIVI)[1:]
      左右, 日期=打針資訊[::2], 打針資訊[1::2]
      if 打針日期:=dict(zip(左右, 日期)):
        rndrCode(['打針日期', 打針日期])
        for 打針, 左右日期 in 打針日期.items():
          打針=''.join(filter(str.isalnum, 打針))
          for 左右, 日期 in findall('(O[DUS])(.*)', 左右日期, IGNORECASE|DOTALL):
            if eyeDate:=findall(r'(\d{6,7})|((?P<Year>\d{2,4})[/-]?(?P<Month>\d{1,2})[/-]?(?P<Day>\d{1,2}))', 日期):
              #rndrCode(eyeDate)
              fullDT=[]
              for eDT in eyeDate:
                dateEye=民國to西元(eDT)
                if dateEye: fullDT.append(dateEye)
              fnlDate=','.join(fullDT)
              eyeFULL.append('|'.join([打針,左右.upper(),fnlDate]))
    rsltEye=mergeEYE(eyeFULL)
    rndrCode(['rsltEye', eyeFULL, rsltEye])
      #for 打針, 左右日期 in split('(IVI[ -]?[EALO])', eyeIVI):  #.*(O[DUS]).*
      #  for 左右, 日期 in findall('(O[DUS])(.*?)', 左右日期):
      #    rndrCode([打針, 左右日期, 左右, 日期])
