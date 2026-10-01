// v1 spaceship - nose cone (translucent PLA/PETG)
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
