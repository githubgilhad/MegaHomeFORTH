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

Changes agains MHF-001
================================================================================

* swaped **PORTL -- PORTF** ( VGA Data - Shared Data) for OUT instruction
* moved **SYNC_RCA** to **PE4** (SYNC_VGA) for OC3B
* moved **SUPPRESS** to **PF3** (with VGA Data) just follow suit
* swaped **RTS/CTS -- X16/PS2_OE** (PE2,3 -- PPB4,5) for PCINT4,5
* **74HC165 -> 74HC166** for synchronous load
* added resistors to PS2_Clock and PS2_Data path to prevent conflict

ToDo changes
================================================================================

* CP2102 board interface + rewire pins
* isolate USB by solder-jumpers


License
-------
GPL 2 or GPL 3 - choose the one that suits your needs.

Author
------
Gilhad - 2025



