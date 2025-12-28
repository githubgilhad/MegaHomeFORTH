.. vim: ft=rst noexpandtab fileencoding=utf-8 nomodified   wrap textwidth=0 foldmethod=marker foldmarker={{{,}}} foldcolumn=4 ruler showcmd lcs=tab\:|- list tabstop=8 noexpandtab nosmarttab softtabstop=0 shiftwidth=0 linebreak showbreak=--»\ 

.. |Ohm| raw:: html

	Ω

.. |kOhm| raw:: html

	kΩ

|MemxFORTHChipandColorfulStack.png|

MegaHomeFORTH MHF-002
=====================

This is next iteration of `MegaHomeFORTH MHF-001 <https://github.com/githubgilhad/MegaHomeFORTH/tree/MHF-001>`__

MHF-001 was sponsored by PCBway.com, which generously manufactured the PCB for it as sponsorship. The PCB was perfectly done and allowed for testings and rewiring problematic parts to reveal hidden problems in the first iteration design.

MHF-002 have more than 75 improvements over MHF-001 and should be even more testable and more convenient for hand soldering, while using more modern parts.

Global Goals
============

|MHF-002.png|

|MHF-002.a.s.jpg|

|MHF-002.b.s.jpg|

MHF was created as an implementation of a graphical and I/O card design for an 8-bit computer based on the HD6309 processor (hereafter referred to as CPU). The actual design is built around the ATmega2560 microcontroller (used, for example, in the Arduino Mega), which I will refer to as the MCU. The MCU is supplemented with RAM and several simple circuits for input and output. Another RAM chip is used for data transfer in both directions, shared alternately between the CPU and MCU. The advantage of this design is high throughput (at the cost of latency) and easy access from both systems.


During the debugging of the preliminary prototypes, it proved to be a significant advantage to have interactive access to the hardware, which led to the implementation of FORTH. It also became clear that, in addition to VGA/RCA, the PS/2 keyboard and SD card could be read concurrently. With enough memory, the graphics card can even function as a standalone single-board computer (SBC), which is a more convenient mode for debugging.

Since access to the shared RAM requires cooperation with the GLUE, the board also includes jumpers for easy configuration of the SBC mode, where some signals intended for the SysBus are redirected directly to the shared memory.

Detailed configuration and usage options will be described on a separate page, but for a quick start, it is sufficient to solder either the left or right side of the A/B jumpers for the graphics card mode. For SBC mode, it is enough to solder the SBC jumpers. These options are mutually exclusive (either graphics card mode or SBC).

Next, there are previews of MHF-002 and links to the schematic and PCB (only the top and bottom layers, as both middle layers are reserved for power), which were generated from KiCad files.


.. |MHF-002.a.s.jpg| image:: MHF-002.a.s.jpg
	:width: 250
	:align: top
	:target: MHF-002.a.s.jpg

.. |MHF-002.b.s.jpg| image:: MHF-002.b.s.jpg
	:width: 250
	:align: top
	:target: MHF-002.b.s.jpg

.. |MHF-002.png| image:: MHF-002.png
	:width: 250
	:align: top
	:target: MHF-002.png

.. |MemxFORTHChipandColorfulStack.png| image:: MemxFORTHChipandColorfulStack.png
	:width: 250
	:align: top
	:target: MemxFORTHChipandColorfulStack.png

.. |view.bottom.png| image:: view.bottom.png
	:width: 250
	:align: top
	:target: view.bottom.png

.. |view_1.png| image:: view_1.png
	:width: 250
	:align: top
	:target: view_1.png

.. |view_2.png| image:: view_2.png
	:width: 250
	:align: top
	:target: view_2.png

.. |view_top.png| image:: view_top.png
	:width: 250
	:align: top
	:target: view_top.png


|view_top.png|

|view.bottom.png|

|view_1.png|

|view_2.png|

`Schema <schema.pdf>`__

`PCB <pcb.pdf>`__
