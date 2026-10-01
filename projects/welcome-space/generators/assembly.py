import math
import os
OUT=os.environ.get('OUT','./out/')
W,H=250,270
def T(x,y,t,sz=3.4,a='start',col='#222',b=False):
    return f'<text x="{x}" y="{y}" font-size="{sz}" text-anchor="{a}" font-family="Arial" fill="{col}"{" font-weight=\"bold\"" if b else ""}>{t}</text>\n'
def badge(x,y,n): return f'<circle cx="{x}" cy="{y}" r="3.6" fill="#185FA5"/>'+T(x,y+1.3,n,3.4,'middle','#fff',True)
s=f'<?xml version="1.0" encoding="UTF-8"?>\n<svg xmlns="http://www.w3.org/2000/svg" width="{W}mm" height="{H}mm" viewBox="0 0 {W} {H}">\n<rect width="{W}" height="{H}" fill="#fff"/>\n'
s+=T(8,10,'v1 spaceship - exploded assembly and student sequence',5,b=True)
cx=70
s+=f'<line x1="{cx}" y1="18" x2="{cx}" y2="258" stroke="#999" stroke-width="0.3" stroke-dasharray="3 2"/>\n'
# nose cone y 20-60
s+=f'<path d="M{cx-23} 62 Q{cx-22} 30 {cx} 20 Q{cx+22} 30 {cx+23} 62 Z" fill="#B5D4F4" stroke="#185FA5" stroke-width="0.4"/>'+badge(cx+34,40,'6')
# panels y 75-180 : front panel + two side fins hint
s+=f'<polygon points="{cx-8},180 {cx-8},80 {cx+8},80 {cx+30},150 {cx+30},180" fill="#E8CFA3" stroke="#8A6A3C" stroke-width="0.4"/>'
s+=f'<polygon points="{cx-8},180 {cx-8},80 {cx-30},150 {cx-30},180" fill="#D9BC8C" stroke="#8A6A3C" stroke-width="0.4"/>'
s+=f'<circle cx="{cx+12}" cy="128" r="7" fill="#B5D4F4" stroke="#8A6A3C" stroke-width="0.3"/>'+badge(cx+40,120,'4')
# wings y 150-200 left/right offset
s+=f'<polygon points="{cx+45},200 {cx+45},160 {cx+60},160 {cx+80},205 {cx+80},212 {cx+70},212 {cx+70},200" fill="#378ADD" stroke="#0C447C" stroke-width="0.4"/>'+badge(cx+90,185,'7')
# plate y 215
s+=f'<ellipse cx="{cx}" cy="220" rx="55" ry="8" fill="#E8CFA3" stroke="#8A6A3C" stroke-width="0.4"/>'
s+=f'<rect x="{cx-35}" y="228" width="22" height="5" fill="#D3D1C7" stroke="#555" stroke-width="0.3"/>'
for x in (0,12,24): s+=f'<circle cx="{cx+x}" cy="231" r="2.2" fill="#fff" stroke="#555" stroke-width="0.3"/>'
s+=f'<rect x="{cx-5}" y="226" width="34" height="1.5" fill="#D85A30"/>'
s+=badge(cx+64,222,'2')
# diffuser y 240-258
s+=f'<path d="M{cx-58} 240 H{cx+58} L{cx+62} 258 H{cx-62} Z" fill="#B5D4F4" fill-opacity="0.7" stroke="#185FA5" stroke-width="0.4"/>'+badge(cx+70,250,'5')
s+=T(cx,266,'electronics are UNDER the plate, facing into the diffuser',3,'middle','#555')
# steps
x0,y0=150,24
steps=[('1','Stickers: on panels and wings while flat'),
('2','Electronics: plate upside down (bottom face up)'),
('','holder + 2 copper rails + 3 LEDs (sandwich)'),
('3','Test: insert battery, ON. Do all 3 LEDs light?'),
('','if not: battery > switch > LED direction >'),
('','tape contact > LED leg contact'),
('4','Panels x3: into the top face of the plate,'),
('','into the long slots (28 mm)'),
('5','Plate into diffuser: electronics facing down'),
('6','Nose cone: onto the top tabs of the 3 panels'),
('7','Wings x3: into the short slots (20 mm)'),
('8','Dark room: ON and final test')]
y=y0
for i,(n,t) in enumerate(steps):
    if n and i>0: y+=3
    if n: s+=badge(x0,y-1.2,n)
    s+=T(x0+6,y,t,3.2)
    y+=5.5
s+=T(x0,y+6,'Note: order of steps 4-5-6 to be tested in pilot.',3,col='#555')
s+=T(x0,y+11,'Alternative: panels into nose cone first,',3,col='#555')
s+=T(x0,y+16,'then everything into the plate.',3,col='#555')
s+='</svg>\n'
open(OUT+'v1_assembly_drawing.svg','w').write(s)
print('ok')
