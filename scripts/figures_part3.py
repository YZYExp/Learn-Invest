#!/usr/bin/env python3
"""Rebuild part 3's exact teaching diagrams with the Python standard library."""
from pathlib import Path
from html import escape
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'assets/images';OUT.mkdir(parents=True,exist_ok=True)
INK='#17324d';MUTED='#52697b';BLUE='#2878a0';TEAL='#238b78';RED='#b95d56';GOLD='#e5bd66'
def text(x,y,s,size=22,color=INK,anchor='start',weight='400'):
 return f'<text x="{x}" y="{y}" font-size="{size}" fill="{color}" text-anchor="{anchor}" font-weight="{weight}">{escape(str(s))}</text>'
def rect(x,y,w,h,fill='#edf3f5',r=14):
 return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{fill}"/>'
def arrow(x1,y1,x2,y2,color=BLUE):
 return f'<path d="M{x1},{y1} L{x2},{y2}" stroke="{color}" stroke-width="3" fill="none" marker-end="url(#arrow)"/>'
def start(title,sub,h=760):
 return f'''<svg xmlns="http://www.w3.org/2000/svg" width="720" height="{h}" viewBox="0 0 720 {h}" role="img"><title>{escape(title)}</title><defs><marker id="arrow" markerWidth="8" markerHeight="8" refX="6" refY="3" orient="auto"><path d="M0,0 L6,3 L0,6" fill="{BLUE}"/></marker></defs><rect width="720" height="{h}" fill="#fbfaf6"/><g font-family="Noto Serif CJK SC, sans-serif">'''+text(36,52,title,28,weight='700')+text(36,87,sub,18,MUTED)
def save(n,s):
 (OUT/f'fig-{n:02d}.svg').write_text(s+'</g></svg>',encoding='utf-8')
# 09 Two distinct cash recipients, reciprocal share transfers.
s=start('发行与转手：钱最终到哪里','同一家公司，两个不同的资金接收方')
s+=rect(30,120,660,245)+text(52,156,'① 公司发行新股',24,TEAL,weight='700')
s+=rect(55,187,165,94,'#dceee8')+text(137,226,'投资者甲',23,anchor='middle')+text(137,256,'出资20万元',19,anchor='middle')
s+=rect(496,187,165,94,'#dce9f3')+text(578,226,'青禾面包',23,anchor='middle')+text(578,256,'取得20万元',19,anchor='middle')
s+=arrow(232,209,481,209)+text(356,196,'认购资金',19,BLUE,'middle')+arrow(481,263,232,263)+text(356,295,'新发行2万股',19,BLUE,'middle')+text(54,337,'发行后：总股数由10万股变为12万股',20)
s+=rect(30,388,660,251)+text(52,427,'② 投资者转让已持有股份',24,TEAL,weight='700')
s+=rect(55,461,165,94,'#dceee8')+text(137,499,'投资者乙',23,anchor='middle')+text(137,530,'买入1000股',19,anchor='middle')
s+=rect(496,461,165,94,'#f4e4d7')+text(578,499,'投资者甲',23,anchor='middle')+text(578,530,'取得1.2万元',19,anchor='middle')
s+=arrow(232,483,481,483)+text(356,470,'交易款1.2万元',19,BLUE,'middle')+arrow(481,537,232,537)+text(356,569,'已发行1000股',19,BLUE,'middle')+text(54,613,'转手后：公司总股数仍为12万股',20)
s+=text(36,690,'假设：新股每股10元，转手每股12元，忽略费用。',19,MUTED)+text(36,722,'普通二级市场交易款不会自动进入公司账户。',20)
save(9,s)
# 10 Exact order book and fills.
s=start('一个1000股买单，为什么分档成交','静态订单簿；不计费用与报价更新')
s+=rect(32,118,656,275)+text(58,155,'当前卖盘（由低价到高价）',23,weight='700')
for j,(p,q) in enumerate([(10,300),(10.05,400),(10.2,500)]):
 y=192+j*60
 s+=rect(53,y-23,613,48,'#e1edf2',6)+text(75,y+8,f'{p:.2f}元',24)+text(275,y+8,f'{q}股',23)+rect(438,y-9,q*.37,16,'#7eb7c8',3)
s+=text(58,377,'最优买价9.98元；最优卖价10.00元',19,MUTED)
s+=rect(32,418,656,122,'#dceee8')+text(56,451,'立即买入1000股',24,TEAL,weight='700')+text(56,484,'300×10.00＋400×10.05＋300×10.20',20)+text(56,518,'总价10080元  →  均价10.08元',23,TEAL)
s+=rect(32,560,656,116,'#f4e4d7')+text(56,595,'限价10.05元，买入1000股',24,weight='700')+text(56,631,'先成交300＋400＝700股',22)+text(56,660,'剩余300股等待；并非保证全部成交',19)
s+=text(36,724,'市价侧重及时成交；限价约束价格，可能无法成交。',19,MUTED)
save(10,s)
# 11 Schematic timing, avoid treating account cash availability as settlement.
s=start('成交、回转与交收：分开看三个时钟','普通股票示意；制度核验：2026-10-23',790)
s+=rect(30,117,660,119,'#e1edf2')+text(51,152,'成交',25,BLUE,weight='700')+text(51,190,'买卖已经匹配，形成履约义务。',22)+text(51,220,'不自动等于“款项已交收、可转出”。',19,MUTED)
s+=rect(30,258,660,133,'#dceee8')+text(51,295,'当日回转',25,TEAL,weight='700')+text(51,331,'港股可当日买卖；普通A股新买股份',21)+text(51,364,'通常不能当天卖出，特定品种另有规则。',20)
s+=rect(30,414,660,227)+text(51,453,'交收周期：假设没有相关假日',24,weight='700')
for x,label in [(228,'周一 T'),(410,'周二'),(586,'周三')]:s+=text(x,494,label,21,anchor='middle')
s+=text(52,545,'美股多数',21)+text(52,575,'适用交易',19,MUTED)+arrow(226,550,410,550)+text(410,583,'T+1交收',19,BLUE,'middle')
s+=text(52,615,'港股通常',21)+arrow(226,610,586,610)+text(586,638,'T+2交收',19,BLUE,'middle')
s+=text(36,696,'能否卖出、能否再买、能否转出银行，是不同问题。',19)+text(36,731,'交收按相应营业日计算；互联互通另查渠道规则。',19,MUTED)+text(36,764,'港股T+1尚属改革计划，不按计划提前改写当前制度。',18,MUTED)
save(11,s)
# 12 Equal initial equity, same asset return, exact bar lengths.
s=start('资产跌10%，自己的钱跌多少','两组初始自有资金都为10万元；不计成本',790)
scale=25
s+=text(36,135,'A 全额自有资金',25,TEAL,weight='700')
for y,label,equity,debt in [(175,'买入时',10,0),(232,'下跌后',9,0)]:
 s+=text(37,y+25,label,21)+rect(165,y,equity*scale,38,'#56a58d',4)+text(165+equity*scale+12,y+27,f'权益{equity}万',20)
s+=text(165,319,'权益：10万 → 9万，亏损10%',23,TEAL)
s+=rect(30,346,660,303)+text(48,388,'B 自有10万＋借入10万',25,BLUE,weight='700')
for y,label,equity,debt in [(424,'买入时',10,10),(492,'下跌后',8,10)]:
 s+=text(45,y+26,label,21)+rect(157,y,equity*scale,42,'#56a58d',4)+rect(157+equity*scale,y,debt*scale,42,'#c4cfd8',4)
 s+=text(157+equity*scale/2,y+28,f'权益{equity}万',18,'#10372a','middle')+text(157+equity*scale+debt*scale/2,y+28,f'债务{debt}万',18,INK,'middle')
s+=text(49,580,'资产：20万 → 18万；债务暂按10万不变',20)+text(49,621,'权益：10万 → 8万，亏损20%',24,RED,weight='700')
s+=text(36,697,'权益＝资产市值－债务。借款不会随资产下跌而减少。',19)+text(36,733,'下跌后杠杆：18÷8＝2.25倍，高于初始2倍。',20)+text(36,768,'实际账户还可能产生利息、追加保证金或强制平仓。',18,MUTED)
save(12,s)
# Numerical invariants for exact arithmetic shown in figures.
assert 300*10+400*10.05+300*10.2==10080
assert 200*9.98+300*9.9+500*9.8==9866
assert abs(18/8-2.25)<1e-12
print('Rebuilt figures 09–12; arithmetic verified.')
