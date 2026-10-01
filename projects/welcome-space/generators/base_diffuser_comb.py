import math
import os
OUT=os.environ.get('OUT','./out/')
CUT='#FF0000'; ENG='#000000'
C=55.0
SLOT_L=28.0; SLOT_W=3.1; SLOT_RC=38.0
ANG=[90,210,330]
def pol(r,a,cx=C,cy=C):
    t=math.radians(a); return cx+r*math.cos(t), cy-r*math.sin(t)

WANG=[30,150,270]; WSLOT_L=20.0; WSLOT_RC=40.0
def slots(cx,cy,stroke,sw=0.1):
    s=''
    for angs,L,rc in ((ANG,SLOT_L,SLOT_RC),(WANG,WSLOT_L,WSLOT_RC)):
        for a in angs:
            x,y=pol(rc,a,cx,cy)
            s+=f'<rect x="{-L/2}" y="{-SLOT_W/2}" width="{L}" height="{SLOT_W}" fill="none" stroke="{stroke}" stroke-width="{sw}" transform="translate({x:.3f},{y:.3f}) rotate({-a})"/>\n'
    return s

def electronics(cx,cy,stroke,sw=0.1,labels=True):
    s=''
    # rail guides (+ top, - bottom), 5 mm wide, 8 mm gap, x -10..44
    s+=f'<rect x="{cx-10}" y="{cy-9}" width="54" height="5" fill="none" stroke="{stroke}" stroke-width="{sw}"/>\n'
    s+=f'<rect x="{cx-10}" y="{cy+4}" width="54" height="5" fill="none" stroke="{stroke}" stroke-width="{sw}"/>\n'
    for x in (2,19,36):
        s+=f'<circle cx="{cx+x}" cy="{cy}" r="2.75" fill="none" stroke="{stroke}" stroke-width="{sw}"/>\n'
    # holder footprint 34x24
    s+=f'<rect x="{cx-46}" y="{cy-12}" width="34" height="24" fill="none" stroke="{stroke}" stroke-width="{sw}"/>\n'
    # electronics limit r=50
    s+=f'<circle cx="{cx}" cy="{cy}" r="50" fill="none" stroke="{stroke}" stroke-width="{sw}" stroke-dasharray="1.5 1.5"/>\n'
    if labels:
        s+=f'<text x="{cx+48}" y="{cy-5}" font-size="5" text-anchor="middle" font-family="Arial" fill="{stroke}">+</text>\n'
        s+=f'<text x="{cx+48}" y="{cy+8}" font-size="5" text-anchor="middle" font-family="Arial" fill="{stroke}">-</text>\n'
        for i,a in enumerate(ANG):
            x,y=pol(46,a+12,cx,cy)
            s+=f'<text x="{x:.2f}" y="{y+1.5:.2f}" font-size="5" text-anchor="middle" font-family="Arial" fill="{stroke}">{i+1}</text>\n'
    return s

# 1) laser base
svg=f'<svg xmlns="http://www.w3.org/2000/svg" width="110mm" height="110mm" viewBox="0 0 110 110">\n'
svg+=f'<g id="CUT-red-hairline"><circle cx="{C}" cy="{C}" r="55" fill="none" stroke="{CUT}" stroke-width="0.1"/>\n'+slots(C,C,CUT)+'</g>\n'
svg+=f'<g id="ENGRAVE-black">\n'+electronics(C,C,ENG)+'</g>\n</svg>\n'
open(OUT+'v1_base_plate_laser.svg','w').write(svg)

# 2) comb test
widths=[3.00,3.05,3.10,3.15,3.20,3.25,3.30]
svg='<svg xmlns="http://www.w3.org/2000/svg" width="130mm" height="70mm" viewBox="0 0 130 70">\n<g id="CUT-red-hairline">\n'
svg+=f'<rect x="5" y="5" width="120" height="30" fill="none" stroke="{CUT}" stroke-width="0.1"/>\n'
for i,w in enumerate(widths):
    x=12+i*16
    svg+=f'<rect x="{x}" y="9" width="{w}" height="18" fill="none" stroke="{CUT}" stroke-width="0.1"/>\n'
for j in range(3):
    svg+=f'<rect x="{5+j*30}" y="42" width="24" height="18" fill="none" stroke="{CUT}" stroke-width="0.1"/>\n'
svg+='</g>\n<g id="ENGRAVE-black">\n'
for i,w in enumerate(widths):
    svg+=f'<text x="{12+i*16+w/2:.2f}" y="32" font-size="3" text-anchor="middle" font-family="Arial">{w:.2f}</text>\n'
svg+='</g>\n</svg>\n'
open(OUT+'v1_comb_test_laser.svg','w').write(svg)

# 3) annotated drawing
def dim(x1,y1,x2,y2,txt,tdx=0,tdy=-1.5,anchor='middle'):
    s=f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="#185FA5" stroke-width="0.25"/>'
    for (x,y) in ((x1,y1),(x2,y2)):
        s+=f'<circle cx="{x}" cy="{y}" r="0.6" fill="#185FA5"/>'
    mx,my=(x1+x2)/2+tdx,(y1+y2)/2+tdy
    s+=f'<text x="{mx}" y="{my}" font-size="3.2" text-anchor="{anchor}" font-family="Arial" fill="#185FA5">{txt}</text>\n'
    return s
W,H=280,175
svg=f'<?xml version="1.0" encoding="UTF-8"?>\n<svg xmlns="http://www.w3.org/2000/svg" width="{W}mm" height="{H}mm" viewBox="0 0 {W} {H}">\n<rect width="{W}" height="{H}" fill="#ffffff"/>\n'
svg+='<text x="8" y="9" font-size="5" font-family="Arial" font-weight="bold" fill="#222">v1 spaceship - base plate and exhaust diffuser (dimensions in mm)</text>\n'
px,py=65,70
svg+=f'<circle cx="{px}" cy="{py}" r="55" fill="#E8CFA3" stroke="#8A6A3C" stroke-width="0.4"/>\n'
svg+=slots(px,py,'#8A6A3C',0.4).replace('fill="none"','fill="#ffffff"')
svg+=f'<rect x="{px-10}" y="{py-9}" width="54" height="5" fill="#D85A30"/><rect x="{px-10}" y="{py+4}" width="54" height="5" fill="#D85A30"/>\n'
for x,col in ((2,'#ffffff'),(19,'#ffffff'),(36,'#378ADD')):
    svg+=f'<circle cx="{px+x}" cy="{py}" r="2.75" fill="{col}" stroke="#555" stroke-width="0.3"/>\n'
svg+=f'<rect x="{px-46}" y="{py-12}" width="34" height="24" fill="#D3D1C7" stroke="#555" stroke-width="0.3"/><text x="{px-29}" y="{py+1}" font-size="3" text-anchor="middle" font-family="Arial">battery holder 34x24</text>\n'
svg+=f'<circle cx="{px}" cy="{py}" r="50" fill="none" stroke="#185FA5" stroke-width="0.3" stroke-dasharray="1.5 1.5"/>\n'
svg+=f'<text x="{px+48}" y="{py-5}" font-size="5" text-anchor="middle" font-family="Arial">+</text><text x="{px+48}" y="{py+8}" font-size="5" text-anchor="middle" font-family="Arial">-</text>\n'
svg+=dim(px-55,py+60,px+55,py+60,'&#216;110',0,-1.5)
svg+=dim(px+2-2.75,py-13,px+36+2.75,py-13,'LED 17',-8,-1.5)
svg+=dim(px-10,py-22,px+44,py-22,'rail 54 x 5, gap 8',0,-1.5)
# slot dims
x,y=pol(SLOT_RC,90,px,py)
svg+=dim(px-8,py-24,px-8,py-52,'slot 28 x 3.1',-2,0,'end')
svg+=f'<text x="{px-55}" y="{py+66}" font-size="3" font-family="Arial" fill="#555">bottom view. panel slot 28 (r24..52) at 90/210/330; wing slot 20 (r30..50) at 30/150/270. width 3.1 = 3.0 + T.</text>\n'
# section
sx,sy=205,60
def P(r,y,sgn=1): return (sx+sgn*r, sy+y)
prof=[(55.2,0),(58,0),(62,24),(60.8,24),(59.3,15),(50,5),(50,3),(55.2,3)]
for sgn in (1,-1):
    pts=' '.join(f'{sx+sgn*r:.2f},{sy+y:.2f}' for r,y in prof)
    svg+=f'<polygon points="{pts}" fill="#B5D4F4" fill-opacity="0.75" stroke="#185FA5" stroke-width="0.4"/>\n'
svg+=f'<rect x="{sx-55}" y="{sy}" width="110" height="3" fill="#E8CFA3" stroke="#8A6A3C" stroke-width="0.3"/>\n'
svg+=f'<rect x="{sx-46}" y="{sy+3}" width="34" height="6.2" fill="#D3D1C7" stroke="#555" stroke-width="0.3"/>\n'
for x in (2,19,36):
    svg+=f'<rect x="{sx+x-2.5}" y="{sy+3}" width="5" height="8.5" fill="#ffffff" stroke="#555" stroke-width="0.3"/>\n'
svg+=f'<line x1="{sx-70}" y1="{sy+24}" x2="{sx+70}" y2="{sy+24}" stroke="#888" stroke-width="0.3"/>\n'
svg+='<text x="%d" y="%d" font-size="3.2" text-anchor="middle" font-family="Arial" fill="#222">section: exhaust diffuser (3D print) + base plate</text>\n'%(sx,sy-10)
svg+=dim(sx-62,sy+30,sx+62,sy+30,'&#216;124 (bottom)',0,4.5)
svg+=dim(sx-58,sy-4,sx+58,sy-4,'&#216;116 (top)',0,-1.5)
svg+=dim(sx+66,sy,sx+66,sy+24,'24',2,1,'start')
svg+=dim(sx-50,sy+19,sx+50,sy+19,'&#216;100 support ledge (electronics stay inside this ring)',0,-1.5)
svg+=f'<text x="{sx-62}" y="{sy+42}" font-size="3" font-family="Arial" fill="#555">pocket: &#216;110.4 x 3 deep (plate sits in), ledge underside chamfered 45 deg (prints without supports), wall 1.2, bottom open.</text>\n'
svg+=f'<text x="{sx-62}" y="{sy+47}" font-size="3" font-family="Arial" fill="#555">switch opening: measure when holder sample arrives (TBD).</text>\n'
svg+=f'<text x="{sx-62}" y="{sy+52}" font-size="3" font-family="Arial" fill="#555">fit: print 3 pocket sizes (&#216;110.25 / &#216;110.40 / &#216;110.55), pick the best.</text>\n'
svg+='</svg>\n'
open(OUT+'v1_base_diffuser_drawing.svg','w').write(svg)
print('ok')
