"""Rebuild original teaching figures 01--04; Python standard library only."""
from pathlib import Path
from html import escape
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'assets/images'
INK='#18333B'; TEAL='#187D85'; GOLD='#CB8D37'; RED='#B5544C'; MUTED='#526971'
def text(x,y,s,size=22,color=INK,anchor='start'):
 return f'<text x="{x}" y="{y}" font-size="{size}" fill="{color}" text-anchor="{anchor}">{escape(str(s))}</text>'
def rect(x,y,w,h,fill,rx=12):return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}"/>'
def line(x,y,x2,y2,color=MUTED,width=2):return f'<line x1="{x}" y1="{y}" x2="{x2}" y2="{y2}" stroke="{color}" stroke-width="{width}"/>'
def save(n,title,sub,body,h=650):
 svg=f'<svg xmlns="http://www.w3.org/2000/svg" width="720" height="{h}" viewBox="0 0 720 {h}" role="img" aria-labelledby="title desc"><title id="title">{escape(title)}</title><desc id="desc">{escape(sub)}</desc><rect width="720" height="{h}" fill="#F6F5EF"/><g font-family="Noto Serif CJK SC,Noto Sans SC,Microsoft YaHei,sans-serif">'+text(36,50,title,28)+text(36,84,sub,18,MUTED)+body+'</g></svg>'
 (OUT/f'fig-{n:02}.svg').write_text(svg,encoding='utf-8')
body=''
for y,v,title,detail,col in [(128,3,'应急：3万元','按每月必要开支1万元，演示3个月缓冲',TEAL),(260,2,'半年后支出：2万元','确定要用的钱，先检查何时可取回',GOLD),(392,7,'长期规划：7万元','其余资金再按目标、期限与风险安排',INK)]:
 body+=text(36,y,title,25)+rect(36,y+18,v/7*560,30,col,5)+text(36,y+80,detail,20,MUTED)
body+=text(36,590,'总额12万元｜原创假设，不是推荐比例',20,MUTED)
save(1,'同一笔钱，三种任务','先按使用时间与用途分层，再选择产品',body)
body=''
rows=[('初始实际付出','10000＋20＝10020元',INK),('资产出售所得','10800元',TEAL),('持有期间现金分配','＋300元',TEAL),('卖出费用','−20元',RED),('最终实际收回','11080元',INK)]
for i,(a,b,c) in enumerate(rows):
 y=125+i*77
 body+=rect(32,y,656,64,'#FFFFFF')+text(50,y+26,a,19,MUTED)+text(668,y+48,b,24,c,'end')
body+=text(36,555,'净赚1060元；1060 ÷ 10020 ≈ 10.58%',24,TEAL)+text(36,603,'持有一年；分配不再投资；忽略税收',19,MUTED)
save(2,'从价格变动到个人净收益','资产涨幅8%，不等于全部现金的净收益率',body)
body=rect(36,116,648,74,INK)+text(360,146,'目标：到期有足够、可动用的购买力',23,'#FFFFFF','middle')+text(360,175,'观察点放在需要用钱的那一天',18,'#FFFFFF','middle')
rows=[('价格下跌','市场变化，变现所得不足'),('合同失约','信用受损，约定付款未到'),('退出困难','交易稀少或锁定期，钱取不出'),('购买力变化','通胀或汇率变化，买不到原定数量')]
for i,(a,b) in enumerate(rows):
 y=222+i*89
 body+=line(62,190 if i==0 else y-32,62,y+12,TEAL)+rect(86,y,598,66,'#FFFFFF')+text(104,y+26,a,23,TEAL)+text(104,y+53,b,20,MUTED)
body+=text(36,620,'同一资产可同时暴露于多种风险；并非概率图',19,MUTED)
save(3,'风险：资金任务怎样失灵','价格波动只是其中一种表现',body)
body=''; x0,y0=82,472; w,h=510,310
for val in [10000,15000,20000,25000,30000]:
 y=y0-(val-10000)/20000*h
 body+=line(x0,y,x0+w,y,'#D6DFDE',1)+text(x0-10,y+6,str(val),17,MUTED,'end')
for year in [0,5,10,15,20]:
 x=x0+year/20*w
 body+=text(x,y0+30,str(year),18,MUTED,'middle')
body+=text(620,y0+30,'年',18,MUTED)
for mode,col in [('simple',GOLD),('compound',TEAL)]:
 pts=[]
 for yr in range(21):
  v=10000*(1+.05*yr) if mode=='simple' else 10000*1.05**yr
  pts.append(f'{x0+yr/20*w:.2f},{y0-(v-10000)/20000*h:.2f}')
 body+=f'<polyline points="{" ".join(pts)}" fill="none" stroke="{col}" stroke-width="4"/>'
body+=text(595,217,'26533',20,TEAL)+text(595,323,'20000',20,GOLD)
body+=rect(82,540,24,7,TEAL,0)+text(118,549,'复利：收益留存再增长',20,TEAL)+rect(82,580,24,7,GOLD,0)+text(118,589,'单利：本金＋历年取出收益',20,GOLD)+text(36,645,'假设固定年增长5%；纵轴从10000元起，并非零起点',17,MUTED)
save(4,'同样的起点，收益是否留存','初始10000元；20年；全部为数学情景',body,680)
# Calculation checks used by chapters.
assert round(10000*1.05**20)==26533
assert round(10000*1.058**20)==30883
assert round(10000*1.045**20)==24117
assert abs((11080-10020)/10020-.10578842315369262)<1e-12
print('Rebuilt fig-01 through fig-04; numerical checks passed.')
