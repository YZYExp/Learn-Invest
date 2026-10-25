"""Rebuild original instructional figures 05–08. Python standard library only."""
from pathlib import Path
from html import escape
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'assets/images'
OUT.mkdir(parents=True,exist_ok=True)
BG='#F6F3EC'; INK='#203340'; TEAL='#217C7E'; GOLD='#C68A39'; MUTED='#60737B'
def svg_start(title,subtitle,h=760):
 return [f'<svg xmlns="http://www.w3.org/2000/svg" width="720" height="{h}" viewBox="0 0 720 {h}" role="img" aria-label="{escape(title)}">',f'<rect width="720" height="{h}" fill="{BG}"/>','<style>text{font-family:"Noto Serif CJK SC","Microsoft YaHei",sans-serif;fill:#203340} .small{font-size:18px} .body{font-size:22px} .title{font-size:30px;font-weight:700}</style>',text(40,58,title,'title'),text(40,95,subtitle,'small')]
def text(x,y,s,cls='body',color=None):
 return f'<text x="{x}" y="{y}" class="{cls}"'+(f' style="fill:{color}"' if color else '')+f'>{escape(s)}</text>'
def rect(x,y,w,h,fill='white',stroke='none',r=16):
 return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{fill}" stroke="{stroke}"/>'
def line(x1,y1,x2,y2,color=TEAL,width=3):
 return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color}" stroke-width="{width}"/>'
def end(parts,n):
 parts.append('</svg>');(OUT/f'fig-{n:02}.svg').write_text('\n'.join(parts),encoding='utf-8')
# 05: discrete cash-flow timeline, not a scaled continuous-y graph.
s=svg_start('图5  一张债券的三年现金流','假设面值1000元，年票息3%，每年付息，足额履约')
for i,(label,amt,note) in enumerate([('买入时','付出 1000 元','以面值买入；忽略税费'),('第1年末','收到 30 元','1000 × 3% = 30'),('第2年末','收到 30 元','再次收到一年的票息'),('第3年末','收到 1030 元','30元票息 + 1000元本金')]):
 y=130+i*135
 if i<3:s.append(line(73,y+86,73,y+133,MUTED,2))
 s.extend([rect(40,y,640,112),f'<circle cx="73" cy="{y+38}" r="16" fill="{TEAL}"/>',text(67,y+45,str(i),'small','#FFFFFF'),text(108,y+35,label,'small'),text(108,y+73,amt),text(350,y+72,note,'small')])
s.extend([text(40,710,'合计收款1090元 = 归还本金1000元 + 利息90元','small'),text(40,738,'票息由合同约定；中途出售的价格仍可能变化。','small')]);end(s,5)
# 06: revenue waterfall and proportional ownership.
s=svg_start('图6  利润归属与实际分红','虚构企业：青禾面包；仅有同权普通股',800)
s.extend([rect(40,126,640,170),text(64,165,'收入 100万元'),rect(64,189,552,35,TEAL,r=6),rect(64,189,496.8,35,'#9AB9B4',r=6),text(64,260,'成本、费用与税收 90万','small'),text(458,260,'净利润 10万','small'),text(64,284,'示意条按金额比例绘制','small')])
s.extend([rect(40,325,640,174),text(64,365,'总股数 10万股'),text(64,406,'你持有 1000股 ÷ 10万股 = 1%'),rect(64,435,552,28,'#DCE7E3',r=5),rect(64,435,5.52,28,GOLD,r=1),text(64,485,'金色部分表示持股比例1%','small')])
s.extend([rect(40,528,640,172),text(64,570,'对应当年净利润：10万元 × 1% = 1000元'),text(64,614,'若公司分配一半利润：实际分红 500元'),text(64,659,'其余利润留在公司，不是账户里的现金。','small'),text(40,744,'利润归属、实际分红与股票市值需要分别记录。','small'),text(40,774,'金额为简化教学假设，不代表真实公司回报。','small')]);end(s,6)
# 07: exact weighted portfolio calculation.
s=svg_start('图7  一只基金的组合回报','假设无费用、无负债、份额不变；甲乙均为虚构资产',780)
s.extend([rect(40,128,640,108),text(64,167,'起点：净资产100万元 / 100万份'),text(64,208,'每份净值 1元')])
s.extend([rect(40,264,312,170),rect(368,264,312,170),text(64,302,'甲资产：权重60%'),text(392,302,'乙资产：权重40%'),text(64,343,'60万元 × 1.10'),text(392,343,'40万元 × 0.95'),text(64,391,'变为66万元',color=TEAL),text(392,391,'变为38万元',color=GOLD),text(64,420,'价格上涨10%','small'),text(392,420,'价格下跌5%','small')])
s.extend([rect(40,463,640,168),text(64,507,'新净资产：66 + 38 = 104万元'),text(64,551,'新净值：104万元 / 100万份 = 1.04元'),text(64,596,'组合回报 = 60% × 10% + 40% × (−5%)')])
s.extend([text(40,680,'结果：+4%，不是两种涨跌幅的简单平均。'),text(40,724,'看懂基金要穿透到资产及其权重。','small'),text(40,754,'基金是集合投资方式；底层资产决定主要风险来源。','small')]);end(s,7)
# 08: vertical comparison cards; distinctions not implied performance ranking.
s=svg_start('图8  先辨认收益来源，再比较回报','以下是权利与成本对照，不是预期收益排行榜',810)
rows=[('直接持有出租物业','来源：租金、转售价差','成本与约束：维护、空置、税费、出售时间'),('REITs份额','来源：按产品条款分派、份额价差','还要看：底层经营、债务、费用、市场报价'),('实物黄金','来源：出售价格与买入成本之差','不会自行付息；另有价差、保管与汇率影响'),('外币与加密资产','外币：相对本币的汇率变化影响回报','代币：权利、储备和兑付条件需逐项核实')]
for i,(a,b,c) in enumerate(rows):
 y=130+i*145;s.extend([rect(40,y,640,125),rect(40,y,8,125,TEAL if i%2==0 else GOLD,r=3),text(64,y+33,a),text(64,y+69,b,'small'),text(64,y+104,c,'small')])
s.extend([text(40,748,'同一种底层对象，实物、基金与衍生品仍有不同合同。','small'),text(40,780,'共同问题：谁付款？付多少？何时能退出？','small')]);end(s,8)
print('Wrote figures 05–08')
