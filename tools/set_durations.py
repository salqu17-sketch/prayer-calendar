import sys, re, datetime as dt
DUR={'🌅 الفجر':40,'☀️ الظهر':30,'🕌 الجمعة':50,'🌤️ العصر':30,'🌇 المغرب':20,'🌙 العشاء':30}
src,dst=sys.argv[1],sys.argv[2]
t=open(src,encoding='utf-8',newline='').read()
now=dt.datetime.now(dt.timezone.utc).strftime('%Y%m%dT%H%M%SZ')
def fix(m):
    ev=m.group(0)
    s=re.search(r'DTSTART;TZID=Asia/Riyadh:(\d{8}T\d{6})',ev).group(1)
    nm=re.search(r'SUMMARY:([^\r]+)',ev).group(1)
    e=dt.datetime.strptime(s,'%Y%m%dT%H%M%S')+dt.timedelta(minutes=DUR[nm])
    ev=re.sub(r'DTEND;TZID=Asia/Riyadh:\d{8}T\d{6}',f'DTEND;TZID=Asia/Riyadh:{e:%Y%m%dT%H%M%S}',ev)
    ev=re.sub(r'DTSTAMP:\w+',f'DTSTAMP:{now}\r\nLAST-MODIFIED:{now}\r\nSEQUENCE:1',ev)
    return ev
t2,n=re.subn(r'BEGIN:VEVENT.*?END:VEVENT',fix,t,flags=re.S)
open(dst,'w',encoding='utf-8',newline='').write(t2); print(dst,n)
