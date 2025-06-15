
See also `Progress <Progress.rst>`__ and `index <README.rst>`__

Journal
=======


* `2025.06.14` I just started this site, now I need to set usable structure, take photo of Arduino Mega Pro and decide on how take out 16MHz for testing purposes without making whole PCB
	
	.. image:: Arduino_mega_2560_PRO_foto_1.png
		:width: 250
		:target: Arduino_mega_2560_PRO_foto_1.png

* `2025.06.15` On ATmega2560 the system clock can be ouput on Port E pin 7 (PE7) - which is not connected to any pin on Arduino Mega, nor on Arduino Mega PRO. But I/O pins on ATmega2560 are by default in read state, which mean high input rezistance, no output signal. Therefore I can connect PE7 to PE5 (which is ~D3 on Arduino), **NEVER** use PE5 for output (or special functions) and "use it just for reading input signal from outside = PE7 = 16MHz" which does not bring any new information, but is easy way how have the 16MHz on Arduino D3 and so usable.
	* Here is the trace from Arduino D3 to ATmega2560 PE5 and marked PE7 pin
		
		.. image:: 2025.06.15-PE5_trace_1.jpg
			:width: 250
			:target: 2025.06.15-PE5_trace_1.jpg
		
		.. image:: 2025.06.15-PE5_trace_2.jpg
			:width: 250
			:target: 2025.06.15-PE5_trace_2.jpg
		
		Here is, how it my microskope shows it on close
		
		.. image:: 2025.06.15-trace_1.jpg
			:width: 250
			:target: 2025.06.15-trace_1.jpg

		And I took 0.2mm enameled wire
		
		.. image:: 2025.06.15-trace_2_wire.jpg
			:width: 250
			:target: 2025.06.15-trace_2_wire.jpg
		
		And soldered it there
		
		.. image:: 2025.06.15-trace_3_loop.jpg
			:width: 250
			:target: 2025.06.15-trace_3_loop.jpg
		
		Ops, I connected wrong pins. When fixing it, I shortcuted PE7 and PE6 and instead of fixing it (which was too dificult) I just "sacrifice" the PE6 too and make bridge to PE5
		
		.. image:: 2025.06.15-trace_4_hack.jpg
			:width: 250
			:target: 2025.06.15-trace_4_hack.jpg
	
	* and I had already installed memxFORTH-core there, so I could test it


