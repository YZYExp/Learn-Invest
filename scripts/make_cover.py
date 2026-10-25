from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import os, subprocess
root=Path(__file__).resolve().parents[1]
font_path=os.environ.get('BOOK_CJK_FONT') or subprocess.check_output(['fc-match','-f','%{file}','Noto Serif CJK SC'],text=True).strip()
im=Image.new('RGB',(1600,2200),'#102f3b'); d=ImageDraw.Draw(im)
def txt(x,y,s,size,color):
 d.text((x,y),s,font=ImageFont.truetype(font_path,size),fill=color)
d.rectangle((115,160,215,176),fill='#d5b46c')
txt(115,220,'看懂投资',184,'#f7f1e4')
txt(123,500,'从一笔钱到整个市场',68,'#d5b46c')
txt(125,650,'资产 · 公司 · 价格 · 风险 · 方法',38,'#b7ced2')
for j,(label,sub) in enumerate([('钱','用途与期限'),('资产','权利与现金流'),('市场','交易与价格'),('判断','价值与风险')]):
 y=940+j*225
 d.ellipse((128,y,206,y+78),outline='#d5b46c',width=3)
 txt(150,y+12,str(j+1),34,'#d5b46c')
 if j<3:d.line((167,y+78,167,y+225),fill='#557882',width=3)
 txt(260,y-10,label,60,'#f7f1e4');txt(500,y+10,sub,40,'#b7ced2')
txt(125,1950,'面向普通读者的投资基础图解',42,'#d5b46c')
txt(125,2040,'24章 / 6篇 / 从概念到判断',31,'#b7ced2')
im.save(root/'assets/images/cover.png')
