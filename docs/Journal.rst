
See also `Progress <Progress.rst>`__ and `index <README.rst>`__ ( `top <../README.rst>`__ )

Journal
=======

* 2025.06.15
	* I had already installed `memxFORTH-core <https://github.com/githubgilhad/memxFORTH-core>`__ there, so I could test it by setting different pins to output and read what is on the port:
	
	.. code:: FORTH
	
		: x DUP 0 PORTE C! DDRE C! PORTE C! PINE C@ FC AND . ; ( clear output on PE, open another pin for output and set it, read the port, ignore bits 0 and 1 (RX TX) )
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
	On ATmega2560 the system clock can be ouput on Port E pin 7 (PE7) - which is not connected to any pin on Arduino Mega, nor on Arduino Mega PRO. But I/O pins on ATmega2560 are by default in read state, which mean high input rezistance, no output signal. Therefore I can connect PE7 to PE5 (which is ~D3 on Arduino), **NEVER** use PE5 for output (or special functions) and "use it just for reading input signal from outside = PE7 = 16MHz" which does not bring any new information, but is easy way how have the 16MHz on Arduino D3 and so usable.

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

