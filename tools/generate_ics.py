import math, datetime as dt, uuid
import sys
LAT, LNG, TZ = float(sys.argv[1]), float(sys.argv[2]), 3
SLUG, CITY = sys.argv[3], sys.argv[4]
d2r=math.radians; r2d=math.degrees
def jd(y,m,d):
    if m<=2: y-=1; m+=12
    A=y//100; B=2-A+A//4
    return int(365.25*(y+4716))+int(30.6001*(m+1))+d+B-1524.5
def sunpos(j):
    D=j-2451545.0
    g=(357.529+0.98560028*D)%360; q=(280.459+0.98564736*D)%360
    L=(q+1.915*math.sin(d2r(g))+0.020*math.sin(d2r(2*g)))%360
    e=23.439-0.00000036*D
    RA=r2d(math.atan2(math.cos(d2r(e))*math.sin(d2r(L)),math.cos(d2r(L))))/15%24
    decl=r2d(math.asin(math.sin(d2r(e))*math.sin(d2r(L))))
    eqt=q/15-RA; eqt-=24*round(eqt/24)
    return decl,eqt
def midday(J,t):
    _,eqt=sunpos(J+t/24); return (12-eqt)%24
def angle_t(J,a,t,ccw):
    decl,_=sunpos(J+t/24)
    c=(-math.sin(d2r(a))-math.sin(d2r(decl))*math.sin(d2r(LAT)))/(math.cos(d2r(decl))*math.cos(d2r(LAT)))
    T=r2d(math.acos(c))/15; z=midday(J,t)
    return z-T if ccw else z+T
def asr_t(J,t):
    decl,_=sunpos(J+t/24)
    a=-r2d(math.atan(1/(1+math.tan(d2r(abs(LAT-decl))))))
    return angle_t(J,a,t,False)
def times(day, ramadan):
    J=jd(day.year,day.month,day.day)-LNG/(15*24)
    t={'f':5/24*24,'d':12,'a':13,'m':18}
    for _ in range(2):
        f=angle_t(J,18.5,t['f']/24*24,True) if False else angle_t(J,18.5,t['f'],True)
        d=midday(J,t['d']); a=asr_t(J,t['a']); m=angle_t(J,0.833,t['m'],False)
        t={'f':f,'d':d,'a':a,'m':m}
    adj=TZ-LNG/15
    out={k:v+adj for k,v in t.items()}
    out['i']=out['m']+(2.0 if ramadan else 1.5)
    return out
def hm(day,h):
    mins=math.ceil(h*60-1e-9) if False else round(h*60)
    return dt.datetime.combine(day,dt.time())+dt.timedelta(minutes=mins)
names={'f':'🌅 الفجر','d':'☀️ الظهر','a':'🌤️ العصر','m':'🌇 المغرب','i':'🌙 العشاء'}
start=dt.date(2026,10,12); end=dt.date(2027,10,11)
ram_s,ram_e=dt.date(2027,2,8),dt.date(2027,3,8)
now=dt.datetime.utcnow().strftime('%Y%m%dT%H%M%SZ')
L=['BEGIN:VCALENDAR','VERSION:2.0','PRODID:-//'+SLUG+' Prayer Times//AR','CALSCALE:GREGORIAN','METHOD:PUBLISH',
   'X-WR-CALNAME:مواقيت الصلاة - '+CITY+'','X-WR-TIMEZONE:Asia/Riyadh',
   'BEGIN:VTIMEZONE','TZID:Asia/Riyadh','BEGIN:STANDARD','DTSTART:19700101T000000','TZOFFSETFROM:+0300','TZOFFSETTO:+0300','TZNAME:+03','END:STANDARD','END:VTIMEZONE']
rows=[]; day=start; n=0
while day<=end:
    T=times(day, ram_s<=day<=ram_e)
    for k in 'fdami':
        s=hm(day,T[k]); e=s+dt.timedelta(minutes=20)
        nm='🕌 الجمعة' if (k=='d' and day.weekday()==4) else names[k]
        L+=['BEGIN:VEVENT',f'UID:{uuid.uuid4()}@{SLUG}-prayer',f'DTSTAMP:{now}',
            f'DTSTART;TZID=Asia/Riyadh:{s:%Y%m%dT%H%M%S}',f'DTEND;TZID=Asia/Riyadh:{e:%Y%m%dT%H%M%S}',
            f'SUMMARY:{nm}','TRANSP:TRANSPARENT',
            'BEGIN:VALARM','ACTION:DISPLAY',f'DESCRIPTION:{nm} بعد ١٠ دقائق','TRIGGER:-PT10M','END:VALARM','END:VEVENT']
        n+=1
    rows.append((day,[hm(day,T[k]).strftime('%H:%M') for k in 'fdami']))
    day+=dt.timedelta(1)
L.append('END:VCALENDAR')
open(f'/home/claude/{SLUG}-prayer-times.ics','w',encoding='utf-8',newline='').write('\r\n'.join(L)+'\r\n')
print(n,'events')
for d,r in rows:
    if d in (dt.date(2026,10,12),dt.date(2026,12,21),dt.date(2027,2,10),dt.date(2027,6,21),dt.date(2027,10,11)): print(d,r)
