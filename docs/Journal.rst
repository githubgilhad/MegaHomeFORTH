
See also `Progress <Progress.rst>`__ and `index <README.rst>`__ ( `top <../README.rst>`__ )

Journal
=======

* 2025.06.19
	* 
* 2025.06.18
	* ATmega2560 sources:
		* Timer0 8bit PWM (pg.115)
		* Timer1,3,4,5 16bit (pg.133)
		* Timer2 8bit PWM+Async mode (pg.169)
		* Timers and pins:
			+--------+--------+--------+---------+
			| Timer  | Cmp    | pin    | Arduino |
			+========+========+========+=========+
			| Timer 0| OC0A   | PB7    | D13     |
			|        +--------+--------+---------+
			|        | OC0B   | PG5    | D4      |
			+--------+--------+--------+---------+
			| Timer 1| OC1A   | PB5    | D11     |
			|        +--------+--------+---------+
			|        | OC1B   | PB6    | D12     |
			|        +--------+--------+---------+
			|        | OC1C   | PB7    | D13     |
			+--------+--------+--------+---------+
			| Timer 2| OC2A   | PB4    | D10     |
			|        +--------+--------+---------+
			|        | OC2B   | PH6    | D9      |
			+--------+--------+--------+---------+
			| Timer 3| OC3A   | PE3    | D5      |
			|        +--------+--------+---------+
			|        | OC3B   | PE4    | D2      |
			|        +--------+--------+---------+
			|        | OC3C   | PE5    | D3      |
			+--------+--------+--------+---------+
			| Timer 4| OC4A   | PH3    | D6      |
			|        +--------+--------+---------+
			|        | OC4B   | PH4    | D7      |
			|        +--------+--------+---------+
			|        | OC4C   | PH5    | D8      |
			+--------+--------+--------+---------+
			| Timer 5| OC5A   | PL3    | D46     |
			|        +--------+--------+---------+
			|        | OC5B   | PL4    | D45     |
			|        +--------+--------+---------+
			|        | OC5C   | PL5    | D44     |
			+--------+--------+--------+---------+


* 2025.06.17
	* check, what NanoHomeComputer SW uses:
		* ATmega328P Timer1 16bits; Timer0 and Timer2 8bits
		* TIMER0_OVF - millis() in Arduino (prescaler x1024), VGA (prescaler x8)
		* TIMER0_COMPA - VGA main asm procedure/line loop
		* TCNT2 - VGA jitter - need prescaler x1 (no prescaling)
		* TIMER1_OVF - frames VGA, lines RCA
		* TIMER1_COMPB - RCAout
		* UCSR0x - RCA USART
* 2025.06.16
	* The next step is to decide, which ports and pins will be used for needed functions
		* external memory (the pins are **fixed** in HW)
			* PA[0..7] is AD0-7 and A0-7 for external memory
			* PC[0..7] is A8-15 for external memory
			* PG0 is WR (write negated)
			* PG1 is RD (read negated)
			* PG2 is ALE (address latch enabled)
		* I/O (Serial/UART, I2C, SPI, ISCP, ...) - I would like to have the basic interfaces available even in the fully populated variant - so let's preliminarily allocate them for now:
			* PB[0..3] ISCP, SPI
			* PE[0..1] RX/TX USART0
			* PD[0..1] I2C/TWI
		* VGA
			* PE[7] 16MHz ( **fixed** in HW)
			* ? PB[6] Timer 1 B
		* RCA
			* ? PD[2..3] USART1 RX/TX
		* free so far:
			* PB[4..7] TC1
				* ? PB [4..6,7] --
			* PD[2..7] USART1
				* ? PD [4..7] --
			* PE[2..6] TC3
			* PF full (JTAG, ADC)
			* PG[3..5] TC0
			* PH full USART2 TC2,4
			* PJ full USART3 PCINT
			* PK full ADC, PCINT
			* PL full TC4,5
	* in `NanoHomeComputer <https://github.com/githubgilhad/NanoHomeComputer>`__ were pins and timers allocated as this:
		* VGA part:
			* PC[2..5] (A2-5) VGA colors = i/O
			* PD[0..7] (D0-7) data out = i/O - 8bits = 1 byte!
			* PB[0] (D8) PL i/O 16MHz - HW
			* PB[2] (D10) Vsync i/O - HW
			* PB[3] (D11) CP    i/O latch data
			* PB[4] (D12) Hsync i/O - SW
		* RCA part
			* PB[1] (D9) Sync - HW
			* PD[0..1] (D0-1) USART (both blocked by HW, used only TX PD1)
			* PD[2] (D2) data Enable (prevents floating pin PD1) - SW
		* PS/2 part
			* PC[0..1] (A0-1) PS/2 = I/o Input
			* PB[5] (D13) PS/2 envelope (change?) - Input

* 2025.06.15
	* I had already installed `memxFORTH-core <https://github.com/githubgilhad/memxFORTH-core>`__ there, so I could test it by setting different pins to output and read what is on the port:
	
	.. code:: FORTH
	
		: x DUP 0 PORTE C! DDRE C! PORTE C! PINE C@ FC AND . ; \ ( clear output on PE,
		\ open another pin for output and set it, read the port, ignore bits 0 and 1 (RX TX) )
		: p? PINE C@ 0FC AND . ; ( what is on Port E? )
		: p! PORTE C! p? ; ( set port E to value on Top Of Stack (TOS) )
		: pp ff PINE C! p? ; ( change all output pins on port E to other values )
		bit3 x ( set PE3 - nice, nothing extra happened )
		0 p! ( just normal function )
		bit7 x ( try the hack )
		p? ( WOW we read 1 on PE5 and PE6 and PE7, also Arduino D3 is ON )
		0 p! ( and now it is OFF again - nice ! )
	
	* well, it was more complicated, but having FORTH there already the testing went smooth - it is really nice to be able interactively send signals on any pin, set it for output/input or let it go ON-OF-ON to see on osciloscope, what happened anywhere
	* and with working connection out, I could set the PE7 to output 16MHz on Arduino D3:

	.. code:: bash
	
		# what fuses are there anyway?
		/usr/bin/avrdude -U hfuse:r:-:h -U lfuse:r:-:h -U efuse:r:-:h -v -V -p atmega2560 -D -c usbasp
		# hfuse: 0xd8 lfuse: 0xff efuse: 0xfd
		# fuse 0x40 enables the clock
		/usr/bin/avrdude -U lfuse:w:0xBF:m -v -V -p atmega2560 -D -c usbasp
		# what fuses are there now?
		/usr/bin/avrdude -U hfuse:r:-:h -U lfuse:r:-:h -U efuse:r:-:h -v -V -p atmega2560 -D -c usbasp
		# hfuse: 0xd8 lfuse: 0xBf efuse: 0xfd
	
	* and osciloscope now see nice 16MHz on D3 :)

* 2025.06.15
	On ATmega2560 the system clock can be ouput on Port E pin 7 (PE7) - which is not connected to any pin on Arduino Mega, nor on Arduino Mega PRO.
	But I/O pins on ATmega2560 are by default in read state, which mean high input rezistance, no output signal.
	Therefore I can connect PE7 to PE5 (which is ~D3 on Arduino), **NEVER** use PE5 for output (or special functions)
	and "use it just for reading input signal from outside = PE7 = 16MHz" which does not bring any new information, but is easy way how have the 16MHz on Arduino D3 and so usable.

	* Here is the trace from Arduino D3 to ATmega2560 PE5 and marked PE7 pin
	
		.. image:: 2025.06.15-PE5_trace_1.jpg
			:width: 250
			:target: 2025.06.15-PE5_trace_1.jpg
		
		.. image:: 2025.06.15-PE5_trace_2.jpg
			:width: 250
			:target: 2025.06.15-PE5_trace_2.jpg
	
	* Here is, how it my microskope shows it on close
	
		.. image:: 2025.06.15-trace_1.jpg
			:width: 250
			:target: 2025.06.15-trace_1.jpg

	* And I took 0.2mm enameled wire
	
		.. image:: 2025.06.15-trace_2_wire.jpg
			:width: 250
			:target: 2025.06.15-trace_2_wire.jpg
	
	* And soldered it there (took me like half a hour)
	
		.. image:: 2025.06.15-trace_3_loop.jpg
			:width: 250
			:target: 2025.06.15-trace_3_loop.jpg
	
	* and tested it with FORTH and it behave wrong way
	* Ops, I connected wrong pins.
	* When fixing it, I shortcuted PE7 and PE6 and instead of fixing it (which was too dificult) I just "sacrificed" the PE6 too and made bridge to PE5 (later I will desolder the chip and clean it and sorder it on the new PCB - so it is just temporary)
	
		.. image:: 2025.06.15-trace_4_hack.jpg
			:width: 250
			:target: 2025.06.15-trace_4_hack.jpg



* 2025.06.14
	I just started this site, now I need to set usable structure, take photo of Arduino Mega Pro and decide on how take out 16MHz for testing purposes without making whole PCB
	
	.. image:: Arduino_mega_2560_PRO_foto_1.png
		:width: 250
		:target: Arduino_mega_2560_PRO_foto_1.png

