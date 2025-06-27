.. vim: set ft=rst showbreak=»\  noexpandtab fileencoding=utf-8 nomodified   wrap textwidth=0 foldmethod=marker foldmarker={{{,}}} foldcolumn=4 ruler showcmd lcs=tab\:|- list tabstop=8 noexpandtab nosmarttab softtabstop=0 shiftwidth=0 linebreak  

Pin assingments:
==================

By group:
==========

External Memory
---------------

External memory is hardcoded in ATmega2560 this way:

* PA[0..7] is AD0-7 and A0-7 for external memory
* PC[0..7] is A8-15 for external memory
* PG0 is WR (write active low)
* PG1 is RD (read active low)
* PG2 is ALE (address latch enabled)

This enables aditional 54kB of RAM, but each access to this RAM takes one cycle longer than the same access for normal RAM.

Also 6kB from 64kB is hidden by the normal RAM and so unused. While it could be also utilised by more advanced mapping, it would need more ICs and more complicated memory mapping. I decided to NOOT support this.

The RAM chip contains 128kB of RAM, so we can select which half we will use - I did choose PG3 as it is the next pin to WR/RD/ALE (and the PG port is already broken). Maybe add pulldown here too, so if the pin is not output, then the default half is used. (Floating values would mean, that reads and writes may go to different parts and whole memory would be unusable.)

* PG3 is A16 (memory bank select)

Input / output
--------------

I/O (Serial/UART, I2C, SPI, ISCP, ...) - I would like to have the basic interfaces available even in the fully populated variant - so let's preliminarily allocate them for now:

* PB[0..3] ISCP, SPI
* PD[0..1] I2C/TWI
* PE[0..1] RX/TX USART0
* PE[2..3] CTS/RTS for flow control (so copy-paste of text is reliable)


VGA
------

VGA system uses Timer 1 for Hsync signal and interrupt and for jitter, Timer 3 for Vsync signal and interrupt, data output needs full port. For colors is also used full port to enable foreground/background colors (selectable possibly for each horizontal line).

Ports F and J looks like free ports, let's use them for data and colors. PB7 looks like free pin in already used port, let's use it for Latch.

* PE[7] 16MHz ( **fixed** in HW)
* PB[6] Timer 1 B for Hsync (SW+HW)
* PE[4] Timer 3 B for Vsync (SW+HW)
* PB[7] Latch
* PF[0..7] for data out
* PJ[0..7] for colors out
* Timer 1 jitter (prescale x1, SW only part)

RCA
------

RCA needs timer with one pin for both Hsync and Vsync, USART for data out and one more pin for suppressing data, when there is no output at all. 

While there is not enough computing power to run VGA and RCA at the same time, it may be possible to have at least synchronisation pulses running, so VGA would just show black screen instead of losing sync (and then take 3 seconds to sync again). So let's use different Timer and pins.

* PD[2..3] USART1 RX/TX (even when RX is not needed, it is HW used while USART uses TX)
* PH[4] Timer 4 B for both Hsync and Vsync 

PS/2
------
* ?? PB[4..5] PS/2 pins
* ?? PE[3] PS/2 Envelope

* free so far:
	* PB[4..7] TC1
		* ? PB [4..5,7] --
		* ?? ---
	* PD[2..7] USART1
		* ? PD [4..7] --
	* PE[2..6] TC3
		* ?? PE[2-3,5-6]
	* PF full (JTAG, ADC)
		* ?? ---
	* PG[3..5] TC0
	* PH full USART2 TC2,4
	* PJ full USART3 PCINT
		* ?? --
	* PK full ADC, PCINT
	* PL full TC4,5
By port:
=========

* PA[0..7] is AD0-7 and A0-7 for external memory
* PB[0..3] ISCP, SPI
* PC[0..7] is A8-15 for external memory
* PD[0..1] I2C/TWI
* PE[0..1] RX/TX USART0
* PE[2..3] CTS/RTS for flow control (so copy-paste of text is reliable)

* PG0 is WR (write active low)
* PG1 is RD (read active low)
* PG2 is ALE (address latch enabled)
* PG3 is A16 (memory bank select)





		* I/O (Serial/UART, I2C, SPI, ISCP, ...) - I would like to have the basic interfaces available even in the fully populated variant - so let's preliminarily allocate them for now:
			* PB[0..3] ISCP, SPI
			* PE[0..1] RX/TX USART0
			* PD[0..1] I2C/TWI
		* VGA
			* (PE5)PE[7] 16MHz ( **fixed** in HW)
			* ? PB[6] Timer 1 B for Hsync
			* ?? PE[4] Timer 3 B for Vsync
			* ?? PF[0..7] for data out
			* ?? PJ[0..7] for colors out
			* ?? PB[7] Latch
			* ?? PB[4..5] PS/2 pins
			* ?? PE[3] PS/2 Envelope
			* ?? Timer 4 jitter
		* RCA
			* ? PD[2..3] USART1 RX/TX
		* free so far:
			* PB[4..7] TC1
				* ? PB [4..5,7] --
				* ?? ---
			* PD[2..7] USART1
				* ? PD [4..7] --
			* PE[2..6] TC3
				* ?? PE[2-3,5-6]
			* PF full (JTAG, ADC)
				* ?? ---
			* PG[3..5] TC0
			* PH full USART2 TC2,4
			* PJ full USART3 PCINT
				* ?? --
			* PK full ADC, PCINT
			* PL full TC4,5
