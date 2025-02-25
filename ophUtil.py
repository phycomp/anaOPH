def nsrtOPH(始年, 末年):
  #with open('眼科資料表.sql', 'w') as fout:
  塞入=''
  for ndx in range(始年, 末年):
    #ndx=str(ndx).zfill(2)
    if ndx>=2020:
      塞入+=fr'''insert into 眼科{ndx} (select f."DTPHIST", f."DTPDATE", concat('S:主觀資料'||E'\n'||f."S", E'\n\n'||'O:客觀資料'||E'\n'||f."O", E'\n\n'||'A:診斷'||E'\n'||f."A", E'\n\n'||'P:治療計畫'||E'\n'||f."P"), f."DTPDEPT" from (select o.*,v."O",a."A",p."P" from (select "DTPMONT", "DTPHIST", "DTPDATE", "DTPDEPT", string_agg("DTSOAPTX", E'\n' order by "DTSTMP" asc)"S" from "BDCBSOAP_{ndx}" where "DTPDEPT" in ('010', '110', '0PH', '1PH', '0C1') and "DTSOAPTY"in ('S') group by 1,2,3,4)o inner join (select "DTPMONT", "DTPHIST", "DTPDATE", "DTPDEPT", string_agg("DTSOAPTX", E'\n' order by "DTSTMP" asc)"O" from "BDCBSOAP_{ndx}" where "DTPDEPT" in ('010', '110', '0PH', '1PH', '0C1') and "DTSOAPTY"in ('O')group by 1,2,3,4)v on o."DTPMONT"=v."DTPMONT" and o."DTPHIST"=v."DTPHIST" and o."DTPDATE"=v."DTPDATE" and o."DTPDEPT"=v."DTPDEPT" inner join(select "DTPMONT", "DTPHIST", "DTPDATE", "DTPDEPT", string_agg("DTSOAPTX", E'\n' order by "DTSTMP" asc)"A" from "BDCBSOAP_{ndx}" where "DTPDEPT" in ('010', '110', '0PH', '1PH', '0C1') and "DTSOAPTY"in ('A') group by 1,2,3,4)a on o."DTPMONT"=a."DTPMONT" and o."DTPHIST"=a."DTPHIST" and o."DTPDATE"=a."DTPDATE" and o."DTPDEPT"=a."DTPDEPT" inner join (select "DTPMONT", "DTPHIST", "DTPDATE", "DTPDEPT", string_agg("DTSOAPTX", E'\n' order by "DTSTMP" asc)"P" from "BDCBSOAP_{ndx}" where "DTPDEPT" in ('010', '110', '0PH', '1PH', '0C1') and "DTSOAPTY"in ('P') group by 1,2,3,4)p on o."DTPMONT"=p."DTPMONT" and o."DTPHIST"=p."DTPHIST" and o."DTPDATE"=p."DTPDATE" and o."DTPDEPT"=p."DTPDEPT")f );'''+'\n'
    else:
      塞入+=fr'''insert into 眼科{ndx} (select f."CHARTID", f."RDATE", concat('S:主觀資料'||E'\n'||f."S", E'\n\n'||'O:客觀資料'||E'\n'||f."O", E'\n\n'||'A:診斷'||E'\n'||f."A", E'\n\n'||'P:治療計畫'||E'\n'||f."P"), f."DTPDEPT" from (select o.*,v."O",a."A",p."P" from (select "DTPMONT", "CHARTID", "RDATE", "DTPDEPT", string_agg("DTSOAPTX", E'\n' order by "DTSTMP" asc)"S" from "BDCBSOAP_{ndx}" where "DTPDEPT" in ('010', '110', '0PH', '1PH', '0C1') and "DTSOAPTY"in ('S') group by 1,2,3,4)o inner join (select "DTPMONT", "CHARTID", "RDATE", "DTPDEPT", string_agg("DTSOAPTX", E'\n' order by "DTSTMP" asc)"O" from "BDCBSOAP_{ndx}" where "DTPDEPT" in ('010', '110', '0PH', '1PH', '0C1') and "DTSOAPTY"in ('O')group by 1,2,3,4)v on o."DTPMONT"=v."DTPMONT" and o."CHARTID"=v."CHARTID" and o."RDATE"=v."RDATE" and o."DTPDEPT"=v."DTPDEPT" inner join(select "DTPMONT", "CHARTID", "RDATE", "DTPDEPT", string_agg("DTSOAPTX", E'\n' order by "DTSTMP" asc)"A" from "BDCBSOAP_{ndx}" where "DTPDEPT" in ('010', '110', '0PH', '1PH', '0C1') and "DTSOAPTY"in ('A') group by 1,2,3,4)a on o."DTPMONT"=a."DTPMONT" and o."CHARTID"=a."CHARTID" and o."RDATE"=a."RDATE" and o."DTPDEPT"=a."DTPDEPT" inner join (select "DTPMONT", "CHARTID", "RDATE", "DTPDEPT", string_agg("DTSOAPTX", E'\n' order by "DTSTMP" asc)"P" from "BDCBSOAP_{ndx}" where "DTPDEPT" in ('010', '110', '0PH', '1PH', '0C1') and "DTSOAPTY"in ('P') group by 1,2,3,4)p on o."DTPMONT"=p."DTPMONT" and o."CHARTID"=p."CHARTID" and o."RDATE"=p."RDATE" and o."DTPDEPT"=p."DTPDEPT")f );'''+'\n'
  #fout.write(塞入)
  return 塞入

def 清洗(始年, 末年):
  rinse=''
  for ndx in range(始年, 末年):
    #ndx=str(ndx).zfill(2)
    rinse+=f'truncate 眼科{ndx};\n'
  return rinse

def 刪除資料表(始年, 末年):
  ophTBL=''
  for ndx in range(始年, 末年):
    #ndx=str(ndx).zfill(2)
    ophTBL+=f'''DROP TABLE public.眼科{ndx};\n'''
  return ophTBL

def 創建資料表(始年, 末年):
  ophTBL=''
  for ndx in range(始年, 末年):
    #ndx=str(ndx).zfill(2)
    ophTBL+=f'''CREATE TABLE public.眼科{ndx} (
      病歷號 varchar(10) NULL,
      日期 date NULL,
      眼科文本 text NULL,
      眼科代碼 varchar(3) NULL,
      視力眼壓 text NULL,
      打針 text NULL
  );\n'''
  return ophTBL
def 更新視壓(始年, 末年):
  視壓=''
  for ndx in range(始年, 末年):
    #ndx=str(ndx).zfill(2)
    視壓+=f'''update "眼科{ndx}" set 視力眼壓="視壓"(眼科文本), 打針="ivi打針"(眼科文本);\n'''    #
  return 視壓
