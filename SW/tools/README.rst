.. vim:   noexpandtab fileencoding=utf-8 nomodified   wrap textwidth=0 foldmethod=marker foldmarker={{{,}}} foldcolumn=4 ruler showcmd lcs=tab\:|- list tabstop=8 noexpandtab nosmarttab softtabstop=0 shiftwidth=0 linebreak showbreak=»\  ft=rst

How to use 24 bits addresses
===============================

* there are `lo8(symbol)`, `hi8(symbol)` and `hlo8(symbol)` for splitting address
* also `pm(symbol)` and `gs(symbol)` which should divide by 2 to get address in FLASH words
* see `<https://sourceware.org/binutils/docs/as/AVR_002dModifiers.html>`__

9.5.2.3 Relocatable Expression Modifiers
----------------------------------------

The assembler supports several modifiers when using relocatable addresses in AVR instruction operands. The general syntax is the following:

modifier(relocatable-expression)

lo8

	This modifier allows you to use bits 0 through 7 of an address expression as an 8 bit relocatable expression.
hi8

	This modifier allows you to use bits 7 through 15 of an address expression as an 8 bit relocatable expression. This is useful with, for example, the AVR ‘ldi’ instruction and ‘lo8’ modifier.

	For example


.. code::

	ldi r26, lo8(sym+10)
	ldi r27, hi8(sym+10)

hh8

	This modifier allows you to use bits 16 through 23 of an address expression as an 8 bit relocatable expression. Also, can be useful for loading 32 bit constants.
hlo8

	Synonym of ‘hh8’.
hhi8

	This modifier allows you to use bits 24 through 31 of an expression as an 8 bit expression. This is useful with, for example, the AVR ‘ldi’ instruction and ‘lo8’, ‘hi8’, ‘hlo8’, ‘hhi8’, modifier.

	For example


.. code::

	ldi r26, lo8(285774925)
	ldi r27, hi8(285774925)
	ldi r28, hlo8(285774925)
	ldi r29, hhi8(285774925)
	; r29,r28,r27,r26 = 285774925

pm_lo8

	This modifier allows you to use bits 0 through 7 of an address expression as an 8 bit relocatable expression. This modifier is useful for addressing data or code from Flash/Program memory by two-byte words. The use of ‘pm_lo8’ is similar to ‘lo8’.
pm_hi8

	This modifier allows you to use bits 8 through 15 of an address expression as an 8 bit relocatable expression. This modifier is useful for addressing data or code from Flash/Program memory by two-byte words.

	For example, when setting the AVR ‘Z’ register with the ‘ldi’ instruction for subsequent use by the ‘ijmp’ instruction:


.. code::

	ldi r30, pm_lo8(sym)
	ldi r31, pm_hi8(sym)
	ijmp

pm_hh8

	This modifier allows you to use bits 15 through 23 of an address expression as an 8 bit relocatable expression. This modifier is useful for addressing data or code from Flash/Program memory by two-byte words.


old
-----

I did not found simple way in **avr-gcc** or **avr-as** 

* `.long symbol` make 32 bit address, not shorter
* `low(symbol)`, `high(symbol)` or similar are not defined
* `symbol & 0xFF`, `symbol >>8` and similar fails, as symbol is not know in compile time and linker does not expressions
* `.byte 0x12, 0x034, 0x056` works, but any change in program/data probably change also the addresses

so I opted for complicated way: 

* scan compiled file `*.elf` for symbols
* generate definitions of all symbols as macros
	* #define address_of_<symbol> .byte 0x12, 0x34, 0x56
* use such macros as addresses in code
* put placeholder values, if macro not found (if possible)
* compile again
* check, if new definitions are the same as old, if no, repeat




.. code::

	
	$ git diff
	diff --git a/SW/src/Makefile b/SW/src/Makefile
	index 3615eab..a201fe8 100644
	--- a/SW/src/Makefile
	+++ b/SW/src/Makefile
	@@ -19,9 +19,18 @@ ASFLAGS += $(DEFINES)
	 include ../Makefile
	 # include $(ARDMK_DIR)/Arduino.mk
	 
	+.PHONY: 24bit
	 
	 $(TARGET_ELF): $(VERSION_HEADER)
	 
	+$(TARGET_ELF): 24bit
	+
	+
	+24bit:
	+	../tools/elf2def.py $(TARGET_ELF) $(OBJDIR)/24bit.def
	+	if ! cmp -s $(OBJDIR)/24bit.def 24bit.def ; then cp $(OBJDIR)/24bit.def 24bit.def; echo -e "##### REMAKE ####"; fi
	+
	+
	 asm.S: words.inc
	 # words.inc: words.4th
	 #	./forth2inc.py
	diff --git a/SW/src/asm.S b/SW/src/asm.S
	index b8443f7..5736e5d 100644
	--- a/SW/src/asm.S
	+++ b/SW/src/asm.S
	@@ -589,6 +589,27 @@ val_of_f_docol:
	 #	.EQU	top_head,1b-3
		.EQU	top_head,1b-4
	 
	+#include "24bit.def"
	+
	+#define PTR24(symbol) address_of_##symbol
	+#define xPTR24(symbol) .byte 0,0,0 
	+
	+// .macro PTR24 symbol
	+// 	address_of_\symbol
	+// .endm
	+
	+
	+.ascii "@@@>"
	+PTR24(f_docol)
	+PTR24(f_docol)
	+PTR24(f_docol)
	+PTR24(w_lastbuildinword_data)
	+PTR24(w_lastbuildinword_data)
	+PTR24(w_lastbuildinword_data)
	+// xPTR24(qwerrewq)
	+// xPTR24(qwerrewq)
	+// xPTR24(qwerrewq)
	+	.ascii "<@@@"
	 .balign 2
		.ascii "###>"
		.global end


