
See `Progress <Progress.rst>`__ and `Journal <Journal.rst>`__ ( `top <../README.rst>`__ )

I have some ideas, but it would need lot of work to bring it into life

Two sided PCB with VGA, RCA and PS/2 connectors on front edge, system connector on back edge and I/O connectors along sides

.. image:: Idea_001.png
	:width: 250
	:target: Idea_001.png

I need two sides to fit everything I want to have

.. image:: Idea_002.png
	:width: 250
	:target: Idea_002.png

The schema is evolving just now

.. image:: Idea_003.png
	:width: 250
	:target: Idea_003.png

Some temporary notes:
=====================

* The CPU needs 4 cycles to prepare itself for servicing the interrupt (save the program counter, load the interrupt vector and clear the I bit in SREG). The interrupt vector itself is a jmp instruction that takes 2 cycles. When the ISR is done, it executes the reti instruction (return from interrupt) that takes 4 cycles. 
* `74AHC373 <https://cz.farnell.com/nexperia/74ahc373pw-118/latch-d-type-transp-3-state-tssop/dp/2445110>`__ NEXPERIA  74AHC373PW,118  Latch, AHC Family, 74AHC373, D Type Transparent, Tri State Inverted, 25 mA, TSSOP
* `RAM <https://cz.farnell.com/infineon/cy7c109d-10zxi/sram-asynchronous-1mbit-tsop-i/dp/2115420>`__ INFINEON  CY7C109D-10ZXI  IC, SRAM, 1 Mbit, 128K x 8bit, 10 ns Access Time, Parallel Interface, 4.5 V to 5.5 V supply, TSOP-32

