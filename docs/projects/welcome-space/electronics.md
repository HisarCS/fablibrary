# Electronics

**One rule:** if the electronics are solid, everything else is artistic.

## Architecture
CR2032 → holder with cover and switch → 2 straight copper rails (+ on top, − on bottom) → 3 LEDs (2 white + 1 color). Everything sits on the **bottom face** of the base plate, inside the exhaust diffuser. Panels and nose cone carry no electrical connections.

## Rules
- Rails are 54 × 5 mm with an **8 mm** gap; extra tape pieces are 6 mm max (short-circuit prevention).
- LED legs: long (+) on the top rail, short (−) on the bottom rail. The leg lies flat on the rail and a short piece of copper tape goes on top (**sandwich joint**).
- The copper tape adhesive must be **conductive**: check with a multimeter from adhesive side to top side.
- If resistors are needed, assistants pre-solder them, not students. Values are set by testing; white/blue LEDs may be brighter without resistors on a CR2032.
- The internal resistance of a CR2032 limits short-circuit current; if switching to stronger cells (AAA), add a resettable fuse.

## Acceptance test
1. Open-circuit and loaded voltage on a fresh cell
2. Series current for each LED type
3. Cell voltage and brightness after 1 hour
4. All three LEDs visible from 3 m in a dark room
5. Switch cycled 100 times
6. 10 different people build the same circuit: **10/10 must work**

## Troubleshooting order
Battery → Switch → LED direction → Tape contact → Leg contact
