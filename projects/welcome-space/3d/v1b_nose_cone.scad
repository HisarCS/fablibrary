// v1b spaceship (Model B) - nose cone, translucent PLA/PETG
// Units: mm. Print base down, no supports needed (pocket ceilings are 3.3 mm bridges).
R      = 33.0;    // base outer radius
H      = 50.0;    // height
wall   = 1.2;   // shell wall
hubH   = 12.0;    // hub height
hubRin = 8.0;     // hub inner radius
// pockets for the 3 panel top tabs (tab 12.0 x 3.0 x 9.5)
pL = 12.4;  // pocket length (tangential)
pW = 3.3;   // pocket width (test 3.2 / 3.3 / 3.4)
pD = 10.0;   // pocket depth
rP = 15.0;    // pocket centre radius
N  = 48;
$fn = 120;

function prof(r, h) = concat([[0,0]], [for (i=[0:N]) let(z=h*i/N) [r*sqrt(max(0,1-pow(z/h,2))), z]]);
module solid(r, h) { rotate_extrude() polygon(prof(r, h)); }
module shell() { difference() { solid(R, H); translate([0,0,-0.01]) solid(R-wall, H-wall); } }
module hub() {
  difference() {
    intersection() { solid(R-wall+0.01, H-wall); cylinder(r=R, h=hubH); }
    translate([0,0,-1]) cylinder(r=hubRin, h=hubH+2);
    for (a=[90,210,330]) rotate([0,0,a])
      translate([rP-pW/2, -pL/2, -1]) cube([pW, pL, pD+1]);
  }
}
union() { shell(); hub(); }
