// v1 spaceship - exhaust diffuser (translucent PLA/PETG)
// Units: mm. z=0 is the table, z=24 is the top (flush with the plate's top face).
// Print: as modeled (wide base on the bed, rim up), no supports (the ledge underside is chamfered), 3 perimeters.

// ---- main parameters ----
H        = 24;     // total height
Rtop     = 58;     // top outer radius (O116)
Rbot     = 62;     // bottom outer radius (O124)
wall     = 1.2;    // sloped wall thickness
pocketD  = 110.4;  // plate pocket diameter -> test print 110.25 / 110.40 / 110.55
pocketH  = 3;      // pocket depth (plate thickness)
ledgeR   = 50;     // support ledge inner radius (O100) - electronics stay inside
ledgeT   = 2;      // support ledge thickness
chamferDz = 10;    // height of the 45-degree underside of the ledge (lets it print without supports)

// ---- switch / battery access window (adjust when holder sample arrives) ----
winOn    = true;
winAng   = 180;    // window direction (deg). Point it at the holder's switch side.
winW     = 14;     // window width
winZ0    = 8;      // window bottom edge (from table)
winZ1    = 18;     // window top edge (must stay below the ledge: < H-pocketH-ledgeT = 19)

$fn = 180;

rp = pocketD/2;
zl = H - pocketH;          // height where the plate sits (21)
zb = zl - ledgeT;          // underside of the ledge (19)
function rout(z) = Rbot + (Rtop-Rbot)*z/H;   // outer wall radius
zc    = zb - chamferDz;     // where the chamfer starts on the inner wall
rin_c = rout(zc) - wall;

// The ledge underside is a ~45 degree slope instead of a flat shelf: no supports needed.
profile = [
  [rp, H], [Rtop, H], [Rbot, 0], [Rbot-wall, 0],
  [rin_c, zc], [ledgeR, zb], [ledgeR, zl], [rp, zl]
];

difference() {
  rotate_extrude() polygon(profile);
  if (winOn)
    rotate([0,0,winAng])
      translate([ledgeR-6, -winW/2, winZ0]) cube([Rbot-ledgeR+12, winW, winZ1-winZ0]);
}
