.. vim: set ft=rst noexpandtab fileencoding=utf-8 nomodified   wrap textwidth=0 foldmethod=marker foldmarker={{{,}}} foldcolumn=4 ruler showcmd lcs=tab\:|- list tabstop=8 noexpandtab nosmarttab softtabstop=0 shiftwidth=0 linebreak showbreak=»\

.. |Ohm| raw:: html

	Ω

.. |kOhm| raw:: html

	kΩ


.. image:: MemxFORTHChipandColorfulStack.png
	:width: 250
	:target: MemxFORTHChipandColorfulStack.png

Many thanks to `PCBway <https://www.pcbway.com/>`__, which sponsored this project by manufacturing the PCB for free. The code for this PCB is **W828834AS5P3** and I will create it as free project after I populate it with all parts and get it to work somehow (= I will write SW for demonstrating at least some functionality).

**MHF-001** results:
====================

The **PCBway** PCB was excelent. Communications with PCBway was easy and straightforward, PCB was made exactly to my specification and it was delivered in good time too. Packaging was standart and the PCB was perfect. It was easy to solder, desolder, resolder parts as the testing went and the PCB was not damaged even with some parts (like USB connector) was resoldered many times.

The PCB was perfect, there is nothing what could be improved on the manufacturing. Bad design decisions are problem on my side, PCBway could not discover or prevent them :)

**I will fully recomend PCBway as PCB manufacturer.**

Also their sponsorship encouraged me to speed progress on this project and to write about it, which is really important part. I thank PCBway for their encouragement.

I did run into lot of problems in this project, many of them was on my part, some not (none on PCBway part)

- I found error in compiler (it is fixed now and was really obscure `<https://gcc.gnu.org/bugzilla/show_bug.cgi?id=119989>`__ )
- CH341G is not fully supported in kernel. There is an unofficial fix, but I may add another option too. And I need way to disable this chip alltogether, to be able use Serial + DTR + line flow over connector (and not fight signalling from chip)
- I underestimated how difficult is to reliably handsolder MCU and memories - I will make better footprints for it, and for USB too
- I had no testing program for the HW
- bad understanding of some technicalities (like that RTS/CTS are crossed between MCU and CH341G in similar way as RX/TX)
- bad planning for port usage 
	- VGA output must be on lower port, which allows **OUT** instruction - **STS** is one tick slower and it matter
	- CTS(in) should be on some Pin Change Interrupt pin
- **74HC165** is level driven so manipulating it "manually" leads to doubled first bit value, I will use **74KC166**, which is edge driven, to prevent this problem
- USB connector is better to be massive (like USB A) and easily repaired (as it is physically manipulated often) - and rather be on small module for repairability
- I need even better testability - more pinheaders, add GND (and maybe +5V) to each connector etc...
- see `<https://github.com/githubgilhad/MegaHomeFORTH/tree/master/docs/MHF-001#errata-and-improvements>`__ for more details

All in all - I will make another PCB. This one is OK, but I have much better design ideas now.

For compatibility current status was set to branch **MHF-001**




MegaHomeFORTH
=============

Mega Home Computer with FORTH on ATmega2560 - step to graphic card for HD6309 - VGA, RCA, PS/2 - see `Larger Picture`_

This project is more about the HW part of solution (but with enought SW to be fully tested and expanded (will be build on the way)).

Look at `MHF-001 <docs/MHF-001/>`__ for actual progress just now

Index
-----

- `MegaHomeFORTH`_
	- `Project Goals`_
	- `Larger Picture`_
	- `Progress`_

Project Goals
==============

Depending on how much components will be soldered to the PCB, it could offer many things (at cost of using some pins):

- full breakout of ATmega2560 - like Arduino Mega, but **all** pins accessible - simply, plain, 86 I/O pins |DSC_8304.s.jpg| |DSC_8305.s.jpg|  `blink_all <https://github.com/githubgilhad/memxFORTH-asm/tree/master/SW/progs/demo/blink_all>`__ 
- USB serial connection - 2 pins
- memory extended to 64 kB RAM - at cost of 16+4 pins
- another 128 kB RAM (somehow) accessible - another 24+3 pins
	- and shared over bus with HD6309/6502/other 8 bit computer - +5pins?
- VGA output (~40x25 characters text screen or 320x200 B/W graphic) - 8+3 pins
	- 4+4 bits forefround+background colors for full text lines (or single graphic lines) - 8 pins
- RCA ("composite") B/W output ( can do this OR VGA, not both at the same time, but may switch it SW way ) - 3 pins
- PS/2 input - 2 or 8+1 pins (much smoother operation)
- SD card reader (may interfere with video interrupts?) - 4pins

In full power it can serve as SBC (Single Board Computer) - or as inteligent Video+Keyboard card for 8 bit computer.



Larger Picture
===============

This project is based on:

- `NanoHomeComputer <https://github.com/githubgilhad/NanoHomeComputer>`__ for HW part
	-  which is based on `Squeezing Water from Stone 3: Arduino Nano + 1(!) Logic IC = Computer with VGA and PS/2 <https://github.com/slu4coder/YouTube>`__ and `Composite video from Arduino UNO <https://www.youtube.com/watch?v=Th18tLP86WQ>`__
- `memxFORTH-core <https://github.com/githubgilhad/memxFORTH-core>`__ for using 24bit pointers on ATmega2560
- `pcFORTH-core <https://github.com/githubgilhad/pcFORTH-core.git>`__ for bigger FORTH implementation
- many different internet sources, discussions and hints

It is another step to retrocomputer based on HD6309 - see `some <http://comp24.gilhad.cz/Comp24-specification.html>`__ `pages <http://comp24.gilhad.cz/documentation/Comp24.html>`__ for basic idea.

Video part was successfully tested on `NanoHomeComputer <https://github.com/githubgilhad/NanoHomeComputer>`__, but ATmega328P with only 2kB RAM and 32kB Flash was too limiting for larger project

|ascii.jpg|

Progress
========

`MHF-001 <docs/MHF-001/>`__

Soldering parts and testing.

Done:

* get Arduino Mega Pro
* get 16MHz to output
* map pins in NanoHomeComputer
* map pins on ATmega2560
* map timers in NanoHomeComputer
* assign VGA/RCA/PS2 pins to ATmega2560
* test VGA output
* test RCA output
* test PS/2 direct input
* test PS/2 8bit input
* assign rest pins on ATmega2560
* draw schema `<HW/KiCad/MHF-001/MHF-001.pdf>`_
* draw PCB
* order PCB
* get PCB manufactured `<HW/KiCad/MHF-001/output.zip>`_

Next steps:

* solder component |DSC_8304.s.jpg| |DSC_8305.s.jpg| ... see `MHF-001 <docs/MHF-001/>`__

* test each goal ... see `MHF-001 <docs/MHF-001/>`__
* physical tests
* programming
* enjoy :)

Something works now: |DSC_8303.s.jpg|

see `Progress <docs/Progress.rst>`__ and `Journal <docs/Journal.rst>`__

I have some ideas, but it would need lot of work to bring it into life

|Idea_001| |Idea_001_a| |Idea_001_b.png|

|Idea_002| |Idea_002_a| |Idea_002_b.png|

|Idea_003| |Idea_003_a| |Idea_003_b.png|

.. |Idea_001| image:: docs/Idea_001.png
	:width: 250
	:target: docs/Idea_001.png

.. |Idea_002| image:: docs/Idea_002.png
	:width: 250
	:target: docs/Idea_002.png

.. |Idea_003| image:: docs/Idea_003.png
	:width: 250
	:target: docs/Idea_003.png


.. |Idea_001_a| image:: docs/Idea_001_a.png
	:width: 250
	:target: docs/Idea_001_a.png

.. |Idea_002_a| image:: docs/Idea_002_a.png
	:width: 250
	:target: docs/Idea_002_a.png

.. |Idea_003_a| image:: docs/Idea_003_a.png
	:width: 250
	:target: docs/Idea_003_a.png



.. |Idea_001_b.png| image:: docs/Idea_001_b.png
	:width: 250
	:align: top
	:target: docs/Idea_001_b.png

.. |Idea_002_b.png| image:: docs/Idea_002_b.png
	:width: 250
	:align: top
	:target: docs/Idea_002_b.png

.. |Idea_003_b.png| image:: docs/Idea_003_b.png
	:width: 250
	:align: top
	:target: docs/Idea_003_b.png

.. |DSC_8303.s.jpg| image:: docs/VGA/DSC_8303.s.jpg
	:width: 250
	:align: top
	:target: docs/VGA/DSC_8303.s.jpg

.. |ascii.jpg| image:: ascii.jpg
	:width: 250
	:align: top
	:target: ascii.jpg


.. |DSC_8304.s.jpg| image:: docs/MHF-001/DSC_8304.s.jpg
	:width: 250
	:align: top
	:target: docs/MHF-001/DSC_8304.s.jpg

.. |DSC_8305.s.jpg| image:: docs/MHF-001/DSC_8305.s.jpg
	:width: 250
	:align: top
	:target: docs/MHF-001/DSC_8305.s.jpg

License
-------
GPL 2 or GPL 3 - choose the one that suits your needs.

Author
------
Gilhad - 2025

