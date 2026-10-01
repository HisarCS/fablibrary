import math
import os
OUT=os.environ.get('OUT','./out/')
CUT='#FF0000'
# wing profile (u radial from axis, v above plate top; plate top is 24 above table)
K=[(26,0),(30.1,0),(30.1,-2.5),(49.9,-2.5),(49.9,0),(63,0),(63,-18),(78,-18),(78,-8),(40,70),(26,70)]
def tx(pts,ox,oy): return ' '.join(f'{u-26+ox:.2f},{oy-v:.2f}' for u,v in pts)
W,H=180,100
s=f'<?xml version="1.0" encoding="UTF-8"?>\n<svg xmlns="http://www.w3.org/2000/svg" width="{W}mm" height="{H}mm" viewBox="0 0 {W} {H}">\n<g id="CUT-red-hairline">\n'
offs=[5,63,121]
for ox in offs: s+=f'<polygon points="{tx(K,ox,75)}" fill="none" stroke="{CUT}" stroke-width="0.1"/>\n'
s+='</g>\n<g id="ENGRAVE-black">\n'
for ox in offs: s+=f'<text x="{ox+10}" y="{75-5}" font-size="3" text-anchor="middle" font-family="Arial">K</text>\n'
s+='</g>\n</svg>\n'
open(OUT+'v1_wing_laser.svg','w').write(s)
# drawing
def dim(x1,y1,x2,y2,t,dx=0,dy=-1.5,a='middle'):
    r=f'<line x1="{x1:.2f}" y1="{y1:.2f}" x2="{x2:.2f}" y2="{y2:.2f}" stroke="#185FA5" stroke-width="0.25"/>'
    for x,y in ((x1,y1),(x2,y2)): r+=f'<circle cx="{x:.2f}" cy="{y:.2f}" r="0.6" fill="#185FA5"/>'
    r+=f'<text x="{(x1+x2)/2+dx:.2f}" y="{(y1+y2)/2+dy:.2f}" font-size="3.2" text-anchor="{a}" font-family="Arial" fill="#185FA5">{t}</text>\n'
    return r
def note(x,y,t): return f'<text x="{x}" y="{y}" font-size="3" font-family="Arial" fill="#555">{t}</text>\n'
W,H=230,150
s=f'<?xml version="1.0" encoding="UTF-8"?>\n<svg xmlns="http://www.w3.org/2000/svg" width="{W}mm" height="{H}mm" viewBox="0 0 {W} {H}">\n<rect width="{W}" height="{H}" fill="#fff"/>\n'
s+='<text x="8" y="9" font-size="5" font-family="Arial" font-weight="bold" fill="#222">v1 spaceship - wing (dimensions in mm)</text>\n'
ax,pt=20,95  # axis x, plate-top y
s+=f'<line x1="{ax}" y1="{pt+30}" x2="{ax}" y2="{pt-80}" stroke="#888" stroke-width="0.25" stroke-dasharray="3 1.5 0.5 1.5"/>'+note(ax+1,pt-81,'axis')
# plate + diffuser silhouette for context
s+=f'<rect x="{ax}" y="{pt}" width="55" height="3" fill="#E8CFA3" stroke="#8A6A3C" stroke-width="0.3"/>'
s+=f'<polygon points="{ax+50},{pt+5} {ax+57.6},{pt+5} {ax+60.8},{pt+24} {ax+62},{pt+24} {ax+58},{pt} {ax+55.2},{pt} {ax+55.2},{pt+3} {ax+50},{pt+3}" fill="#B5D4F4" stroke="#185FA5" stroke-width="0.3"/>'
s+=f'<line x1="{ax-5}" y1="{pt+24}" x2="{ax+95}" y2="{pt+24}" stroke="#888" stroke-width="0.3"/>'+note(ax+85,pt+28,'table')
s+='<polygon points="'+' '.join(f'{ax+u:.2f},{pt-v:.2f}' for u,v in K)+'" fill="#378ADD" fill-opacity="0.85" stroke="#0C447C" stroke-width="0.4"/>\n'
s+=dim(ax+26,pt-76,ax+78,pt-76,'52 (r 26..78)',0,-1.5)
s+=dim(ax+86,pt-70,ax+86,pt+18,'88',2,1,'start')
s+=dim(ax+30.1,pt+33,ax+49.9,pt+33,'tab 19.8 x 2.5',0,4)
s+=dim(ax+63,pt+40,ax+78,pt+40,'15',0,4)
s+=note(115,40,'- wing x3, identical parts, 3 mm plywood.')
s+=note(115,46,'- fits the 20 mm wing slot in the base (30/150/270 deg).')
s+=note(115,52,'- poka-yoke: the 27.8 panel tab does not fit a wing slot;')
s+=note(115,57,'  a wing tab is loose in a panel slot, easy to notice.')
s+=note(115,63,'- lower part sits outside the diffuser, ends 6 mm above the table.')
s+=note(115,69,'- closest gap to the diffuser ~2 mm (at the bottom).')
s+=note(115,75,'- no clash with panels: wings sit 60 deg between them.')
s+=note(115,83,'TEST: with a single 20 mm tab the wing may lean.')
s+=note(115,88,'if it wobbles: split the tab in two or reduce slot T.')
s+='</svg>\n'
open(OUT+'v1_wing_drawing.svg','w').write(s)
print('ok')
