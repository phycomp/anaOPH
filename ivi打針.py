CREATE OR REPLACE FUNCTION public."ivi打針"(outcome character varying DEFAULT 'outcome'::character varying)
 RETURNS character varying
 LANGUAGE plpython3u
AS $function$
from re import findall, DOTALL, IGNORECASE, split

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
    日期打針=fnlEye.get(eye)
    if 日期打針: 日期打針+=f',{mDT}'
    else: 日期打針=mDT
    neatDT=rinseDT(日期打針)
    fnlEye[eye]=neatDT    #日期打針
  return fnlEye

def 民國to西元(eyeDate):
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
  dateEye=''.join([str(Year), Month, Day])
  return dateEye

def rtrvEYE(outcome): #1. 先用s/p分成 2. 用打針IVI 3. 左右眼 4. 找出日期
  if not outcome: return ''
  eyeFULL=[]
  for 主觀 in findall('S:主觀資料(.*?)\n\n', outcome, DOTALL):
    #if search('IVI', 主觀, IGNORECASE|DOTALL):rndrCode('找到IVI')
    for eyeIVI in split('s/p', 主觀, flags=IGNORECASE):
      打針資訊=split('(IVI[- ]?[EAOL]|PDT|IVAS)', eyeIVI)[1:]
      左右, 日期=打針資訊[::2], 打針資訊[1::2]
      打針日期=dict(zip(左右, 日期))
      if 打針日期:  #=dict(zip(左右, 日期)):
        for 打針, 左右日期 in 打針日期.items():
          打針=''.join(filter(str.isalnum, 打針))
          for 左右, 日期 in findall('(O[DUS])(.*)', 左右日期, IGNORECASE|DOTALL):
            eyeDate=findall(r'(\d{6,7})|((?P<Year>\d{2,4})[/-]?(?P<Month>\d{1,2})[/-]?(?P<Day>\d{1,2}))', 日期)
            if eyeDate: #=findall(r'(\d{6,7})|((?P<Year>\d{2,4})[/-]?(?P<Month>\d{1,2})[/-]?(?P<Day>\d{1,2}))', 日期):
              fullDT=[]
              for eDT in eyeDate:
                dateEye=民國to西元(eDT)
                fullDT.append(dateEye)
              fnlDate=','.join(fullDT)
              eyeFULL.append('|'.join([打針,左右.upper(),fnlDate]))
    #rsltEye=rsltEye
  return mergeEYE(eyeFULL)
  #rndrCode(['rsltEye', eyeFULL, rsltEye])
rsltEye=rtrvEYE(outcome)
return rsltEye

$function$
