: DROP3 DROP2 DROP ;
: LF D EMIT ; 
: ?n ( pinval PINport -- value ) ( and print )
	C@ AND DUP IF ." SET " ELSE ." nul " THEN ; 
		\ call: pin7 PINJ, returns if PJ[7] is set or no
: !n ( pinval PINport value -- )
	IF DUP3 ?n ." => SET " 
	IF DROP3 ELSE C! THEN 
	ELSE DUP3 ?n ." ZEROED " 
	IF C! ELSE DROP3 THEN THEN ;
	\ call: pin7 PINJ 0 to reset the pin, or call: pin7 PINJ 1 to set it
: nD0 bit0 PINF ; \ data out
: nD1 bit1 PINF ;
: nD2 bit2 PINF ;
: nD3 bit3 PINF ;
: nD4 bit4 PINF ;
: nD5 bit5 PINF ;
: nD6 bit6 PINF ;
: nD7 bit7 PINF ;

: nA0 bit4 PINB ; \ PS/2
: nA1 bit5 PINB ;

: nD11 bit7 PINB ; \ Latch

\ Colors
: nA2 bit0 PINJ ;
: nA3 bit1 PINJ ;
: nA4 bit2 PINJ ;
: nA5 bit3 PINJ ;

\ 
: nD10 bit4 PINE ; \ V sync
: nD12 bit6 PINB ; \ H sync

: nD13 bit3 PINE ; \ Envelope


: status 
	." DATA: " nD0 ?n nD1 ?n 
	nD2 ?n nD3 ?n nD4 ?n nD5 ?n 
	nD6 ?n nD7 ?n . . . . . . . .
	SPACE ." COLORS: " 
	nA2 ?n nA3 ?n nA4 ?n nA5 ?n 
	. . . . SPACE ." Vsync " 
	nD10 ?n DROP ." Latch "
	nD11 ?n DROP ." Hsync "
	nD12 ?n DROP ." Env " 
	nD13 ?n DROP ." PS2 "
	nA0 ?n DROP nA1 ?n DROP
	CR LF ;
