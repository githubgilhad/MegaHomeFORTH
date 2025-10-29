.. vim: set ft=rst noexpandtab fileencoding=utf-8 nomodified   wrap textwidth=0 foldmethod=marker foldmarker={{{,}}} foldcolumn=4 ruler showcmd lcs=tab\:|- list tabstop=8 noexpandtab nosmarttab softtabstop=0 shiftwidth=0 linebreak showbreak=»\

.. |Ohm| raw:: html

	Ω

.. |kOhm| raw:: html

	kΩ


.. image:: ../../MemxFORTHChipandColorfulStack.png
	:width: 250
	:target: ../../MemxFORTHChipandColorfulStack.png


MegaHomeFORTH - MHF-001
========================

Mega Home Computer with FORTH on ATmega2560 - step to graphic card for HD6309 - VGA, RCA, PS/2 - see `Larger Picture`_

This project is more about the HW part of solution (but with enought SW to be fully tested and expanded (will be build on the way)).

See `<../../HW/KiCad/MHF-002/>`_

Changes from MHF-001
================================================================================


* switched to SMD logical gates for more space avaiable
* switched from 2 to 4 layers (internal are POWER exclusively) for better distribution of power and reducing noise
* added more **Cx** capacitors, but cannont fit them exactly at each power pin for place restrictions - at least they are near and many
* swaped **PORTL -- PORTF** ( VGA Data - Shared Data) for OUT instruction
* moved **SYNC_RCA** to **PE4** (SYNC_VGA) for OC3B
* moved **SUPPRESS** to **PF3** (with VGA Data) just follow suit
* swaped **RTS/CTS -- X16/PS2_OE** (PE2,3 -- PPB4,5) for PCINT4,5
* **74HC165 -> 74HC166** for synchronous load
* added resistors to PS2_Clock and PS2_Data path to prevent conflict
* CP2102 board interface + rewire pins
* isolate USB by solder-jumpers
* SDCard added
* **74AHC373 -> 74AHC573** for better routing
* The transistor is `S8050`, not BC107
* the Inside capacitor is `10 nF`, not 100pF
* the resistor is 20 |kOhm|, no 3k3/22k
* breakout VGA, PS/2 and RCA conectors to pinheader
* LED on `PB7` aka `SYSTEM_LED` for bootloader may be usefull (even when it is `VGA_latch` so it will shine with VGA attached - like 10 |kOhm| green LED?)
* LED on `Reset` may help to debug serial communication (`DTR` pin via capacitor)
* Reset button changed to cheap common Arduino switch
* breakout all USB pins to its own pinheader (and USB A can be attached with just piece of stripboard)
* included CP2102 module
* switched `X16` and `RTS` lines, so `RTS` could use interrupt on low. (RTS can be also ignored, or checked on regular schedule, like 50/sec in SW)
	* `CTS` and `RTS` on atmega and on CH340G should be crossed the same way as RX/TX - **RTS** on **CH340G** is **OUTPUT**
* RX0,TX0 RTS0,CTS0 are **Arduino** pins/points of view, should go to crossed ports on chips Arduino.RX0=CH340G.TX, Arduino.RTS0=CH340G.CTS
* enabled isolation of  **CH340G** via closed solderpads (to freely use Serial headers)
* breakout `DTR` to Serial headers
* for `ISCP` it is needed to set `hfuse` to 0xD9 (run program) instead of 0xD8 (run bootloader) as ICSP destroy bootloader (or what)
* make my own footprints with longer pads for SMD ICs to make soldering easier
* PROBLEM - 74HC165 doubles the first bit (as it is shifted out and latched again before level latch returns inactive) and so ONECHAR have to be 9 clocks long (or lose the last bit) - 74HC166 should be better (as it is edge latched) but now I cannot feed it each 8 clocks, so last bit will be errornerous
	* I should use some port A..F for VGA data **OUT** instead of **STS** too, to fit in 8 clocks
* SD card reader needed little edge filing to not collide with ISCP connector and 3V3 connector - make little more place for it next time and add mounting holes in corner. Sitting just on Koptan tape looks good. (Alternatively unsolder all components and move them on PCB directly. Qualify MISO and MOSI (and maybe clock too) by CS, let CS go inside all the time. Use another pin than ISCP)
* `blink_all <https://github.com/githubgilhad/memxFORTH-asm/tree/master/SW/progs/demo/blink_all>`__  from `memxFORTH-asm <https://github.com/githubgilhad/memxFORTH-asm>`__  may be usefull
* each port connector should have at least `GND`, and ideally `+5V` too - for LEDS and other use (just GND, the +5V are not so needed and there are some free standing around)
* possibly enable to enable SBC use Shared RAM via open solderpads for signals X-A-B interconnected
* the label **"+ 5V -"** was wrong rotated (probabelly some autocorrect on schema -> PCB), fixed and repeatadly checked to be right (no problems found)
* mark areas on SysBus, separate blocks as Data, Address, A, B, Power, MasterReset  with lines
* added MasterReset with diode from Reset to SysBus
* added emitor follower to I2C LED
* added 8 TestPointProbes pads between D-Latch and RAM
* reordered internal pin assignement for RAMs for better routing
* moved PS/2 PsDat to port with IN instructon
* moved RCA Sync and Suppress to share pins with VGA
* switch for using 74HC166 for RCA (marked **40** for old method and **80** for new one after max number of characters per line) - not tested, but Grant Searle uses something similar
* marked PS/2, VGA, RCA, USB areas of PCB on both sides
* better marking of parts and jumpers
* 6 **WS2812B** LEDs for status signalling as "debug diodes" on **X_SHARE_GRANTED** as leds use specific output signal, while X_SHARE_GRANTED is input, which will not pulse on the right frequency. Separated both by 1k resistors.
* **SBC** jumpers for easier (and more consistent) configuration as SBC
* **/VGA_Enabled** active **LOW** enables VGA output. If disabled, VGA gets only black color, regardless of **VGA_Data[0..7]** and **VGA Colors [0..7]** so **PORT F** and **PORT H** may be used for anything else

Some numbers
================================================================================

10x10cm, 4 layers, around 153 parts, 338 vias, 11.4m of tracks, 1174 pads, 378 nets, 4069 segments, 164 solder points, bridges, pinholes, probes and similar copper pieces :)
3x AND, 1x NOT gates was unused and are breaked out for user, 8x9 pinholes as universal expansion area (under SD Card)

ToDo changes
================================================================================



License
-------
GPL 2 or GPL 3 - choose the one that suits your needs.

Author
------
Gilhad - 2025



