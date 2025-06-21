.. vim: set ft=rst showbreak=»\  noexpandtab fileencoding=utf-8 nomodified   wrap textwidth=0 foldmethod=marker foldmarker={{{,}}} foldcolumn=4 ruler showcmd lcs=tab\:|- list tabstop=8 noexpandtab nosmarttab softtabstop=0 shiftwidth=0 linebreak  

See also `Journal <Journal.rst>`__ and `index <README.rst>`__ ( `top <../README.rst>`__ )

Progress
========

Done:

* get Arduino Mega PRO with ATmega2560 for testing
	* ordered some from AliExpress
	* it will also serve as component source for the PCB
* get 16MHz output
	* there is no connection for this on Arduino boards
	* I connected it to some other pin for tests (NEVER use PE5, PE6 in testing)!!!
* map pins in NanoHomeComputer
	* I need to know (and have written to see it), what is used and for what functions
	* I also need to write all used timers and their connections, as conversion need reassing both pins and timers
* map pins on ATmega2560
	* I need to write down what I already used, what are HW limits and to be able to plan optimal use of the rest
* assign VGA/RCA/PS2 pins to ATmega2560
* test VGA output

Next steps:

* test RCA output
* test PS/2 direct input
* test PS/2 8bit input
* assign rest pins on ATmega2560
* draw schema
* draw PCB
* order PCB
* get PCB manufactured
* solder component
* test each goal
* physical tests
* programming
* enjoy :)



