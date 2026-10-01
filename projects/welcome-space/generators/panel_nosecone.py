import math
import os
OUT=os.environ.get('OUT','./out/')
CUT='#FF0000'
# panel profile in (u,v): u radial mm from axis, v height above plate top
P=[(8,0),(24.1,0),(24.1,-2.5),(51.9,-2.5),(51.9,0),(54,0),(54,30),(21,130),(19,130),(19,140),(11,140),(11,130),(8,130)]
def tx(pts,ox,oy): return ' '.join(f'{u-8+ox:.2f},{oy-v:.2f}' for u,v in pts)
# window center
wu,wv,wr=21.9,85,10
# --- laser panels
W,H=160,155
s=f'<?xml version="1.0" encoding="UTF-8"?>\n<svg xmlns="http://www.w3.org/2000/svg" width="{W}mm" height="{H}mm" viewBox="0 0 {W} {H}">\n<g id="CUT-red-hairline">\n'
offs=[5,57,109]
for ox in offs:
    s+=f'<polygon points="{tx(P,ox,147)}" fill="none" stroke="{CUT}" stroke-width="0.1"/>\n'
s+='</g>\n<g id="ENGRAVE-black">\n'
for ox in offs:
    s+=f'<circle cx="{wu-8+ox:.2f}" cy="{147-wv}" r="{wr}" fill="none" stroke="#000" stroke-width="0.1"/>\n'
    s+=f'<text x="{wu-8+ox:.2f}" y="{147-8}" font-size="3" text-anchor="middle" font-family="Arial">v1</text>\n'
s+='</g>\n</svg>\n'
open(OUT+'v1_panel_laser.svg','w').write(s)

# --- annotated drawing
def dim(x1,y1,x2,y2,t,dx=0,dy=-1.5,a='middle'):
    r=f'<line x1="{x1:.2f}" y1="{y1:.2f}" x2="{x2:.2f}" y2="{y2:.2f}" stroke="#185FA5" stroke-width="0.25"/>'
    for x,y in ((x1,y1),(x2,y2)): r+=f'<circle cx="{x:.2f}" cy="{y:.2f}" r="0.6" fill="#185FA5"/>'
    r+=f'<text x="{(x1+x2)/2+dx:.2f}" y="{(y1+y2)/2+dy:.2f}" font-size="3.2" text-anchor="{a}" font-family="Arial" fill="#185FA5">{t}</text>\n'
    return r
def note(x,y,t): return f'<text x="{x}" y="{y}" font-size="3" font-family="Arial" fill="#555">{t}</text>\n'
W,H=280,200
s=f'<?xml version="1.0" encoding="UTF-8"?>\n<svg xmlns="http://www.w3.org/2000/svg" width="{W}mm" height="{H}mm" viewBox="0 0 {W} {H}">\n<rect width="{W}" height="{H}" fill="#fff"/>\n'
s+='<text x="8" y="9" font-size="5" font-family="Arial" font-weight="bold" fill="#222">v1 spaceship - body panel and nose cone (dimensions in mm)</text>\n'
# panel drawn with u measured from axis: axis line at x=ax
ax,base=30,165
pts=' '.join(f'{ax+u:.2f},{base-v:.2f}' for u,v in P)
s+=f'<line x1="{ax}" y1="{base+8}" x2="{ax}" y2="{base-150}" stroke="#888" stroke-width="0.25" stroke-dasharray="3 1.5 0.5 1.5"/>\n'
s+=f'<text x="{ax-1}" y="{base-151}" font-size="3" text-anchor="end" font-family="Arial" fill="#888">axis</text>\n'
s+=f'<polygon points="{pts}" fill="#E8CFA3" stroke="#8A6A3C" stroke-width="0.4"/>\n'
s+=f'<circle cx="{ax+wu}" cy="{base-wv}" r="{wr}" fill="#B5D4F4" stroke="#8A6A3C" stroke-width="0.3"/>\n'
s+=f'<line x1="{ax-5}" y1="{base}" x2="{ax+70}" y2="{base}" stroke="#888" stroke-width="0.25"/>'+note(ax+60,base+4,'plate top')
s+=dim(ax+8,base+7,ax+54,base+7,'46 (r 8..54)',0,4)
s+=dim(ax+24.1,base+13,ax+51.9,base+13,'bottom tab 27.8 x 2.5',0,4)
s+=dim(ax+62,base,ax+62,base-130,'130',2,1,'start')
s+=dim(ax+62,base,ax+62,base-30,'30',-2,1,'end').replace('text-anchor="end"','text-anchor="end"')
s+=dim(ax+11,base-145,ax+19,base-145,'top tab 8 x 10',0,-1.5)
s+=dim(ax+8,base-136,ax+21,base-136,'13',-9,1)
s+=note(ax+40,base-112,'window/sticker area O20 (engrave)')
s+=note(ax+70,base-60,'panel x3, identical parts,')
s+=note(ax+70,base-55,'fits any panel slot')
s+=note(ax+70,base-48,'3 mm plywood')
s+=note(ax+70,base-41,'bottom tab 2.5 is shorter')
s+=note(ax+70,base-36,'than the 3 mm plate')
# nose cone section
cx,cb=205,120   # axis x, base y
R,Hc,w=23,45,1.2
def r_at(z,RR,HH): return RR*math.sqrt(max(0,1-(z/HH)**2))
N=40
outer=[(r_at(Hc*i/N,R,Hc),Hc*i/N) for i in range(N+1)]
inner=[(r_at((Hc-w)*i/N,R-w,Hc-w),(Hc-w)*i/N) for i in range(N+1)]
for sg in (1,-1):
    poly=[(sg*r,z) for r,z in outer]+[(sg*r,z) for r,z in reversed(inner)]
    s+='<polygon points="'+' '.join(f'{cx+x:.2f},{cb-z:.2f}' for x,z in poly)+'" fill="#B5D4F4" fill-opacity="0.8" stroke="#185FA5" stroke-width="0.4"/>\n'
# hub section (cut plane through one slot on right side, solid on left)
hubH=12
ri_h=r_at(hubH,R-w,Hc-w)
s+=f'<polygon points="{cx-ri_h:.2f},{cb-hubH} {cx-8},{cb-hubH} {cx-8},{cb} {cx-(R-w):.2f},{cb}" fill="#B5D4F4" stroke="#185FA5" stroke-width="0.3"/>\n'
s+=f'<polygon points="{cx+8},{cb-hubH} {cx+ri_h:.2f},{cb-hubH} {cx+(R-w):.2f},{cb} {cx+19.5},{cb} {cx+19.5},{cb-11} {cx+10.5},{cb-11} {cx+10.5},{cb} {cx+8},{cb}" fill="#B5D4F4" stroke="#185FA5" stroke-width="0.3"/>\n'
# panel top tab inside
s+=f'<rect x="{cx+11}" y="{cb-10}" width="8" height="10" fill="#E8CFA3" stroke="#8A6A3C" stroke-width="0.3"/>\n'
s+=f'<rect x="{cx+8}" y="{cb}" width="13" height="8" fill="#E8CFA3" stroke="#8A6A3C" stroke-width="0.3"/>\n'
s+=dim(cx-R,cb+16,cx+R,cb+16,'O46 base',0,4.5)
s+=dim(cx-R-8,cb,cx-R-8,cb-Hc,'45',-2,1,'end')
s+=dim(cx+10.5,cb-22,cx+19.5,cb-22,'',0,-1.5)+f'<line x1="{cx+19.5}" y1="{cb-22}" x2="{cx+30}" y2="{cb-30}" stroke="#185FA5" stroke-width="0.25"/>'+f'<text x="{cx+31}" y="{cb-30}" font-size="3.2" font-family="Arial" fill="#185FA5">slot 9 x 3.3, 11 deep</text>\n'
s+=f'<line x1="{cx}" y1="{cb+10}" x2="{cx}" y2="{cb-Hc-6}" stroke="#888" stroke-width="0.25" stroke-dasharray="3 1.5 0.5 1.5"/>\n'
s+=note(cx-55,cb+30,'section: right side shows the panel top tab in a slot, left side the solid hub.')
s+=note(cx-55,cb+35,'shell wall 1.2, rounded (not sharp) tip, hub 12 high, center hole O16.')
s+=note(cx-55,cb+40,'3 slots at 90/210/330 deg, open at the bottom: prints without supports.')
s+=note(cx-55,cb+45,'slot width 3.3 is an estimate: test print 3.2 / 3.3 / 3.4.')
s+=note(cx-55,cb+52,'material: translucent PLA or PETG, tip up, no supports.')
s+='</svg>\n'
s=s.replace('O46','&#216;46').replace('O20','&#216;20').replace('O16','&#216;16')
open(OUT+'v1_panel_nosecone_drawing.svg','w').write(s)

# --- OpenSCAD nose cone
scad='''// v1 spaceship - nose cone (translucent PLA/PETG)
// Units: mm. Print base down, no supports needed.
R      = 23;    // base outer radius (O46)
H      = 45;    // height
wall   = 1.2;   // shell wall (0.4 nozzle: 3 perimeters)
hubH   = 12;    // hub height
hubRin = 8;     // hub inner radius (O16 hole)
slotW  = 3.3;   // slot width for panel tab (test 3.2/3.3/3.4)
slotR0 = 10.5;  // slot inner start radius
slotR1 = 19.5;  // slot outer end radius
slotD  = 11;    // slot depth (tab is 10)
N      = 48;    // profile resolution
$fn    = 120;

function prof(r, h) = concat([[0,0]], [for (i=[0:N]) let(z=h*i/N) [r*sqrt(max(0,1-pow(z/h,2))), z]]);

module solid(r, h) { rotate_extrude() polygon(prof(r, h)); }

module shell() { difference() { solid(R, H); translate([0,0,-0.01]) solid(R-wall, H-wall); } }

module hub() {
  difference() {
    intersection() { solid(R-wall+0.01, H-wall); cylinder(r=R, h=hubH); }
    translate([0,0,-1]) cylinder(r=hubRin, h=hubH+2);
    for (a=[90,210,330]) rotate([0,0,a])
      translate([slotR0, -slotW/2, -1]) cube([slotR1-slotR0, slotW, slotD+1]);
  }
}

union() { shell(); hub(); }
'''
open(OUT+'v1_nose_cone.scad','w').write(scad)
print('ok')
