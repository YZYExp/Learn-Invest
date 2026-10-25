"""Rebuild original numeric diagrams for chapters 13–16, standard library only."""
from pathlib import Path
from html import escape

OUT=Path(__file__).resolve().parents[1]/'assets/images'
FONT='Noto Serif CJK SC, Noto Serif CJK SC, sans-serif'
INK='#213c45'; MUTED='#526970'; TEAL='#197a74'; GOLD='#d89b45'; RED='#ba6656'

def text(x,y,s,size=23,color=INK,weight='normal'):
    return f'<text x="{x}" y="{y}" font-size="{size}" fill="{color}" font-weight="{weight}">{escape(s)}</text>'
def box(x,y,w,h,color='#e8f3ef'):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="16" fill="{color}"/>'
def frame(n,title,subtitle,body,height=760):
    svg=f'<svg xmlns="http://www.w3.org/2000/svg" width="720" height="{height}" viewBox="0 0 720 {height}" role="img"><title>{escape(title)}</title><rect width="720" height="{height}" fill="#faf8f2"/><g font-family="{FONT}">'+text(36,48,f'{n:02d} / 理解公司与价格',19,TEAL,'bold')+text(36,94,title,30,INK,'bold')+text(36,131,subtitle,20,MUTED)+body+'</g></svg>'
    (OUT/f'fig-{n:02d}.svg').write_text(svg,encoding='utf-8')

body=''
items=[('收入',100,'#197a74'),('变动支出',50,'#78a59b'),('固定支出',35,'#b5c7b9'),('其他费用及税收',5,GOLD),('净利润',10,'#197a74')]
for i,(label,val,color) in enumerate(items):
 y=171+i*70
 body+=text(36,y+21,label,22)+f'<rect x="257" y="{y}" width="{val*3.35}" height="30" rx="6" fill="{color}"/>'+text(610,y+23,str(val),23,INK,'bold')
body+=box(36,545,648,156)+text(57,580,'收入少10%，利润可能少50%',25,TEAL,'bold')+text(57,620,'原来：100 − 50 − 35 − 5 = 10',23)+text(57,661,'下降后：90 − 45 − 35 − 5 = 5',23)+text(36,737,'单位：万元；其他支出暂固定，税费现实可能变化。',18,MUTED)
frame(13,'收入不等于利润','同一门生意：先看收入如何被支出分走',body)

body=''
for y,title,lines in [(165,'利润表｜全年赚多少',['收入100 − 现金性质费用85 − 折旧5','净利润 = 10万元']), (330,'现金流量表｜钱怎么移动',['经营：10 + 5 − 应收增加3 − 存货增加4 = 8','投资：买设备 −6；筹资：0；现金净增加 = 2']), (515,'资产负债表｜年末留下什么',['资产55 = 负债15 + 权益40','现金：年初18 + 净增加2 = 年末20'])]:
 body+=box(36,y,648,145)+text(57,y+37,title,25,TEAL,'bold')+text(57,y+80,lines[0],20)+text(57,y+116,lines[1],22)
body+=text(354,319,'↓',28,TEAL)+text(354,504,'↓',28,TEAL)+text(36,711,'权益：年初30 + 净利润10 = 年末40',22)+text(36,748,'单位：万元；无分红、新增借款、增资及其他权益变化。',18,MUTED)
frame(14,'同一家公司，三种观察角度','青禾面包的简化账：利润、现金与资产相互勾稽',body,780)

body=box(36,167,648,145)+text(58,205,'起点：每股收益1元 × 市盈率20倍',25,TEAL,'bold')+text(58,252,'每股价格 = 20元',30,INK,'bold')+text(58,288,'10万股 × 20元 = 股权市值200万元',21,MUTED)
body+=text(36,361,'利润相同，市场给予的倍数不同',25,INK,'bold')
for y,mult,price in [(385,12,12),(455,25,25)]:
 body+=text(50,y+30,f'{mult}倍',24)+f'<rect x="155" y="{y}" width="{price*15}" height="39" rx="7" fill="{TEAL if mult==12 else GOLD}"/>'+text(560,y+30,f'{price}元',25)
body+=box(36,555,648,163,'#f4e8df')+text(57,594,'盈利增长，也可能遇到股价下跌',25,RED,'bold')+text(57,635,'1.2元 × 12倍 = 14.4元',28)+text(57,679,'盈利 +20%　　价格相对20元 −28%',23)
body+=text(36,752,'教学假设：倍数不代表推荐值；未来利润并不确定。',18,MUTED)
frame(15,'把价格拆成两部分','每股价格 = 每股收益 × 市盈率（同口径正利润）',body,780)

body=''
scenes=[(166,'分红｜发出现金5万元',['公司现金 −5万元；总股数仍10万股','每股收到0.5元；理论除息价格20→19.5元'],'#e8f3ef'),(340,'回购并注销｜花20万元买1万股',['公司现金 −20万元；股数10万→9万股','利润仍10万元时，每股收益1→约1.1111元'],'#eee9d9'),(514,'增发｜20元发行2万股',['公司现金 +40万元；股数10万→12万股','利润暂不变时，每股收益1→约0.8333元'],'#e4eef0')]
for y,title,lines,color in scenes:
 body+=box(36,y,648,151,color)+text(56,y+39,title,25,TEAL,'bold')+text(56,y+84,lines[0],21)+text(56,y+123,lines[1],21)
body+=text(36,714,'三种独立场景，均从10万股、每股20元起算。',21)+text(36,750,'忽略税费与市场变化；机械变化不能代替价值判断。',18,MUTED)
frame(16,'股东动作：现金与股数一起看','公司资金流向不同，每股背后的权益也会变化',body,780)

# Check arithmetic used by the drawings and prose.
assert 100-50-35-5==10 and 90-45-35-5==5
assert 10+5-3-4==8 and 18+8-6==20 and 55==15+40
assert abs((1.2*12/20-1)*100+28)<1e-10
assert abs(sum([10/1.12,10/1.12**2,110/1.12**3])-95.1963374636)<1e-8
print('Built fig-13 through fig-16; numeric checks passed.')
