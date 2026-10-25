#!/usr/bin/env python3
"""Rebuild chapters 17—20's numerical teaching diagrams (standard library)."""
from pathlib import Path
from html import escape
import json
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'assets/images'
INK='#173c49'; TEAL='#127d84'; MUTED='#526a73'; ORANGE='#b85e32'; BG='#f7f8f3'; PALE='#e5f2ee'; LINE='#c6d6d2'
FONT='Noto Serif CJK SC, Source Han Sans SC, Microsoft YaHei, sans-serif'

def text(x,y,s,size=23,fill=INK,anchor='start',weight='normal'):
 return f'<text x="{x}" y="{y}" font-size="{size}" fill="{fill}" text-anchor="{anchor}" font-weight="{weight}">{escape(str(s))}</text>'
def box(x,y,w,h,fill=PALE):
 return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="14" fill="{fill}"/>'
def line(x1,y1,x2,y2,color=LINE,width=2):
 return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color}" stroke-width="{width}"/>'
def svg(num,title,sub,body,h=720):
 s=f'''<svg xmlns="http://www.w3.org/2000/svg" width="720" height="{h}" viewBox="0 0 720 {h}" role="img" aria-labelledby="title desc"><title id="title">{escape(title)}</title><desc id="desc">{escape(sub)}</desc><rect width="720" height="{h}" fill="{BG}"/><g font-family="{FONT}">{text(36,52,title,29,weight='bold')}{text(36,88,sub,19,fill=MUTED)}{body}{line(36,h-60,684,h-60)}{text(36,h-27,f'图{num} · 原创教学假设；非历史行情与收益预测',18,fill=MUTED)}</g></svg>'''
 (OUT/f'fig-{num}.svg').write_text(s)

p3=sum(c/(1.03**t) for t,c in enumerate([30,30,1030],1))
p5=sum(c/(1.05**t) for t,c in enumerate([30,30,1030],1))
assert round(p3,2)==1000 and round(p5,2)==945.54
b=text(36,134,'合同现金流不变：面值1000元，年票息3%',22)
for i,(year,cash) in enumerate([('第1年末','30元'),('第2年末','30元'),('第3年末','1030元')]):
 x=36+i*222
 b+=box(x,160,204,118)+text(x+102,198,year,21,anchor='middle')+text(x+102,244,cash,31,anchor='middle',weight='bold')
b+=text(36,322,'今天的价格：把三笔款项分别折现后相加',22)
for y,label,value,formula in [(349,'要求收益率3%',p3,'30/1.03 + 30/1.03² + 1030/1.03³'),(478,'要求收益率5%',p5,'30/1.05 + 30/1.05² + 1030/1.05³')]:
 b+=box(36,y,648,111)+text(56,y+36,label,23)+text(660,y+36,f'{value:.2f}元',29,anchor='end',weight='bold')+text(56,y+78,formula,23,fill=MUTED)
b+=text(36,632,'假设：无违约、无税费、年末付息、完整剩余3年。',20,fill=MUTED)
svg(17,'同一张债券，两种今天的价格','折现率提高，固定现金流的现值降低。',b,730)

b=''
clocks=[('经济时钟','产出、消费、就业','记录整体经济活动'),('公司时钟','订单、收入、成本','记录企业经营成果'),('价格时钟','最新成交、估值','反映交易与未来判断')]
for i,(a,c,d) in enumerate(clocks):
 y=122+i*110
 b+=box(36,y,648,94)+text(56,y+37,a,25,weight='bold')+text(250,y+34,c,22)+text(250,y+68,d,20,fill=MUTED)
b+=text(36,493,'盈利增长，不保证价格上涨',25,weight='bold')
for y,a,c in [(527,'原来：每股收益1.00元 × 25倍','价格25.00元'),(590,'后来：每股收益1.20元 × 18倍','价格21.60元')]:
 b+=text(40,y,a,22)+text(675,y,c,22,anchor='end',fill=TEAL,weight='bold')
b+=text(36,644,'盈利增长20%；价格下降13.6%。',23,fill=ORANGE,weight='bold')
svg(18,'经济、公司与价格：三块时钟','它们相互影响，却不保证同向、同时变化。',b,740)

b=box(36,122,648,183)+text(360,161,'实际交换：三笔成交合计',25,anchor='middle',weight='bold')
b+=text(63,208,'买方群体',23)+text(552,208,'卖方群体',23)
b+=line(192,200,524,200,TEAL,3)+text(360,192,'支付2970元 →',22,anchor='middle',fill=TEAL)
b+=line(192,265,524,265,ORANGE,3)+text(360,254,'← 转移300股',22,anchor='middle',fill=ORANGE)
b+=text(36,353,'同一批成交，按主动方向标签再分类',23,weight='bold')
for y,label,value,color in [(390,'主动买入',980,TEAL),(463,'主动卖出',1990,ORANGE)]:
 b+=text(36,y+25,label,22)+f'<rect x="180" y="{y}" width="{value/1990*345:.2f}" height="38" fill="{color}" rx="5"/>'+text(670,y+27,f'{value}元',24,anchor='end',weight='bold')
b+=box(36,541,648,93)+text(360,576,'标签差额：980 − 1990 = −1010元',25,anchor='middle',weight='bold')+text(360,612,'买卖双方金额相等；主动方向金额可以不等。',21,anchor='middle')
b+=text(36,673,'自定义分类示例；不识别机构身份；忽略费用。',20,fill=MUTED)
svg(19,'“净流出”不等于没有买方','先问统计口径，再解释资金方向。',b,770)

rows=[('基准年估价',1.00,20,20.00),('原先预期',1.20,20,24.00),('实际后估价A',1.10,20,22.00),('实际后估价B',1.10,18,19.80)]
b=text(36,128,'同一股数；价格 = 每股收益 × 市盈率',22)
for i,(name,eps,pe,price) in enumerate(rows):
 y=151+i*116
 b+=box(36,y,648,101)+text(54,y+29,name,23,weight='bold')+text(667,y+29,f'{eps:.2f}元 × {pe}倍',22,anchor='end',fill=MUTED)
 b+=f'<rect x="54" y="{y+47}" width="{price/24*475:.1f}" height="31" rx="5" fill="{TEAL if i<2 else ORANGE}"/>'+text(666,y+72,f'{price:.2f}元',26,anchor='end',weight='bold')
b+=text(36,652,'从预期24元到19.80元：价格下降17.5%。',22,fill=ORANGE)
b+=text(36,685,'比基准年赚得更多，也可能低于此前买入预期。',21)
svg(20,'业绩增长，股价为何仍会下跌','比较实际结果，也要比较此前预期和估值。',b,780)
print(json.dumps({'bond_price_3pct':p3,'bond_price_5pct':p5,'figures':[f'fig-{n}.svg' for n in range(17,21)]},ensure_ascii=False))
