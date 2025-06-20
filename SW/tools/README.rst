.. vim:   noexpandtab fileencoding=utf-8 nomodified   wrap textwidth=0 foldmethod=marker foldmarker={{{,}}} foldcolumn=4 ruler showcmd lcs=tab\:|- list tabstop=8 noexpandtab nosmarttab softtabstop=0 shiftwidth=0 linebreak showbreak=»\  ft=rst

How to use 24 bits addresses
===============================

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


