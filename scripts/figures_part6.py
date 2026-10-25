"""Rebuild original, numerically checkable diagrams for chapters 21–24."""
from pathlib import Path
from html import escape
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'assets/images'
NAVY='#17324d'; TEAL='#147d82'; GOLD='#d99732'; BG='#f7f4ed'; MUTED='#546574'
def text(x,y,s,size=24,color=NAVY,weight='400',anchor='start'):
 return f'<text x="{x}" y="{y}" font-size="{size}" fill="{color}" font-weight="{weight}" text-anchor="{anchor}">{escape(s)}</text>'
def rect(x,y,w,h,fill='#ffffff',stroke='none',r=14):
 return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{fill}" stroke="{stroke}"/>'
def line(x1,y1,x2,y2,col=MUTED,width=2):
 return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{col}" stroke-width="{width}"/>'
def save(n,title,body,h=760):
 svg=f'''<svg xmlns="http://www.w3.org/2000/svg" width="720" height="{h}" viewBox="0 0 720 {h}" role="img" aria-labelledby="title"><title id="title">{escape(title)}</title><rect width="720" height="{h}" fill="{BG}"/><g font-family="Noto Serif CJK SC, Noto Sans SC, Microsoft YaHei, sans-serif">{text(36,54,f'图{n}  '+title,29,weight='700')}{body}</g></svg>'''
 (OUT/f'fig-{n}.svg').write_text(svg)

def main():
 OUT.mkdir(parents=True,exist_ok=True)
 rows=[('日常周转','1.6万元','两个月必要支出',1.6,TEAL),('应急储备','4.0万元','收入中断与意外支出',4.0,TEAL),('已知支出','2.0万元','八个月后付款',2.0,GOLD),('长期余额','4.4万元','进一步讨论投资用途',4.4,NAVY)]
 b=text(36,98,'虚构林家：现金合计12万元；必要支出0.8万元/月',22,color=MUTED)
 for i,(a,m,d,v,c) in enumerate(rows):
  y=126+i*128;b+=rect(36,y,648,112)+text(56,y+33,a,24,weight='700')+text(660,y+33,m,24,c,weight='700',anchor='end')+text(56,y+65,d,21,color=MUTED)+rect(56,y+82,600*v/12,12,c,r=4)
 b+=text(36,680,'1.6 ＋ 4.0 ＋ 2.0 ＋ 4.4 ＝ 12.0万元',24,weight='700')+text(36,724,'同一笔钱不重复承担两项资金任务。',22,color=MUTED)
 save(21,'先给钱分配任务',b)
 b=text(36,100,'教学假设：股票涨20%，债券不变；忽略费用税收',22,color=MUTED)
 stages=[('起始：总额10.0万元',6,4,'股票60.00%'),('价格变化后：总额11.2万元',7.2,4,'股票64.29%'),('转移0.48万元后：总额11.2万元',6.72,4.48,'股票60.00%')]
 for i,(title,s,d,pct) in enumerate(stages):
  y=130+i*174;b+=text(36,y,title,24,weight='700')
  total=s+d;scale=648/11.2
  b+=rect(36,y+24,s*scale,58,TEAL,r=0)+rect(36+s*scale,y+24,d*scale,58,GOLD,r=0)
  b+=text(48,y+62,f'股票{s:g}',23,'white')+text(36+s*scale+12,y+62,f'债券{d:g}',23,NAVY)+text(36,y+120,pct,22,color=MUTED)
 b+=text(36,698,'卖股票4800元 → 买债券4800元',25,TEAL,weight='700')+text(36,738,'只靠新增资金恢复比例，则需向债券加入8000元。',21,color=MUTED)
 save(22,'比例会随价格漂移',b,780)
 b=text(36,98,'每次投入1000元；小数份额不受限制；无费用',22,color=MUTED)
 cases=[('路径A：10 → 5 → 10元',[10,5,10]),('路径B：10 → 15 → 20元',[10,15,20])]
 for i,(title,prices) in enumerate(cases):
  y=124+i*264;shares=[1000/x for x in prices];total=sum(shares);value=total*prices[-1]
  b+=rect(36,y,648,238)+text(56,y+37,title,26,weight='700')
  for j,(p,s) in enumerate(zip(prices,shares)):
   x=56+j*210;b+=text(x,y+82,f'第{j+1}次：{p}元',22,color=MUTED)+rect(x,y+102,s*.50,25,TEAL,r=3)+text(x,y+158,f'{s:.2f}份',23,TEAL,weight='700')
  b+=text(56,y+207,f'共{total:.2f}份；期末约{value:.2f}元',24,weight='700')
 b+=text(36,704,'定投改变投入节奏，不保证盈利或胜过一次投入。',22,color=MUTED)
 save(23,'金额固定，份额变化',b,750)
 b=text(36,98,'把事实、假设、结果和过程分别记录',23,color=MUTED)
 steps=[('交易前','目标／期限／投入金额','写下理由及什么证据会改变判断'),('持有中','披露变化／现金流变化','核对事实，区分价格波动与条件改变'),('复盘时','净回报与合适基准','入金不是收益；费用不能重复扣除'),('修订后','保留、调整或退出','记录依据，更新下次检查时间')]
 for i,(title,a,c) in enumerate(steps):
  y=125+i*139;b+=rect(36,y,648,113)+text(56,y+32,title,24,TEAL,weight='700')+text(56,y+65,a,23,weight='700')+text(56,y+95,c,21,color=MUTED)
  if i<3:b+=line(360,y+115,360,y+136,TEAL,3)
 b+=text(36,726,'结果好 ≠ 每个判断都对；结果差 ≠ 每个判断都错。',21,color=MUTED)
 save(24,'让决策可以被复查',b,770)
 # Auditable arithmetic used by the text and diagrams.
 assert abs(sum([1.6,4,2,4.4])-12)<1e-10
 assert abs(11.2*.6-6.72)<1e-10
 assert abs(7.2/.6-11.2-.8)<1e-10
 assert abs(sum(1000/p for p in [10,5,10])*10-4000)<1e-10
 assert abs(sum(1000/p for p in [10,15,20])*20-4333.333333333333)<1e-9
 assert abs(1.1*.92-1-.012)<1e-10
 print('Rebuilt figures 21–24; arithmetic assertions passed.')
if __name__=='__main__': main()
