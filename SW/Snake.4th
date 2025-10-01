( keys 8462 on numeric keyboard, or numbers )
: '2' [ 0 CHAR 2 ] LITERAL ;
: '4' [ 0 CHAR 4 ] LITERAL ;
: '6' [ 0 CHAR 6 ] LITERAL ;
: '8' [ 0 CHAR 8 ] LITERAL ;
( item )
: '#' [ 0 CHAR # ] LITERAL ;
( score, max )
0 0 0 0 VALUE score VALUE maxscore VALUE crash VALUE grow
: show_score
	1 2 CUR_yx  ." SCORE: " score .
	score maxscore > IF score TO maxscore 1 MAX_COLS /2 1- CUR_yx '#' EMIT FI
	1 MAX_COLS /2   CUR_yx  ." MAX: " maxscore .
	;
( wall )
: wall CLS
	0 BEGIN 0 OVER '#' VRAM_yx! 2 OVER '#' VRAM_yx! MAX_ROWS 1- OVER '#' VRAM_yx!  1+ DUP MAX_COLS  = UNTIL DROP
	0 BEGIN                     DUP  0 '#' VRAM_yx! DUP MAX_COLS 1-  '#' VRAM_yx!  1+ DUP MAX_ROWS  = UNTIL DROP
	1 2 CUR_yx ." SCORE:" 0 . SPACE
	;
: is_wall ( c -- flag ) '#' = ;
: test_wall ( y x --  )  VRAM_yx@ is_wall IF 1 TO crash THEN ;
( movement )
: do_step ( y x d -- y x )
	CASE
	0 OF SWAP 1+ SWAP ENDOF
	1 OF 1- ENDOF
	2 OF 1+ ENDOF
	3 OF SWAP 1- SWAP ENDOF
	ENDCASE ;
: key_to_dir ( olddir key -- newdir ) CASE
	'2' OF DROP 0 ENDOF
	'4' OF DROP 1 ENDOF
	'6' OF DROP 2 ENDOF
	'8' OF DROP 3 ENDOF
	ENDCASE ;
: body_str S" abc#de#fg#hi#jkl" ; : body_str_addr body_str DROP ;
: head_str S" v<>^" ; : head_str_addr head_str DROP ;
: tail_str S" v<>^" ; : tail_str_addr tail_str DROP ;
: fruit_str S" @$&*" ; : fruit_str_addr fruit_str DROP ;
( body )
: show_body ( y x old new ) body_str_addr SWAP2 SWAP 4 * + +21 C@ VRAM_yx! ;
: is_body ( c -- flag ) body_str ISINSTR ;
: test_body ( y x --  )  VRAM_yx@ is_body IF 2 TO crash THEN ;
( fruit )
: random_fruit fruit_str RANDOM +21 C@ ;
: show_fruit ( -- ) 5 RANDOM IFNOT MAX_ROWS 4 - RANDOM 3 + MAX_COLS 2 - RANDOM 1+ DUP2 VRAM_yx@ BL = IF random_fruit VRAM_yx! ELSE DROP2 FI FI ;
: is_fruit ( c -- flag ) fruit_str ISINSTR ;
: test_fruit ( y x --  ) VRAM_yx@ is_fruit IF 1 TO grow 1 +TO score THEN ;
( tail )
0 0 0 VALUE tx VALUE ty VALUE td
: hide_tail ty tx BL VRAM_yx! ;
: is_tail ( c -- flag ) tail_str ISINSTR ;
: show_tail ty tx tail_str_addr td +21 C@ VRAM_yx! ;
: test_tail ( y x --  )  VRAM_yx@ is_tail IF 2 TO crash THEN ;
: move_tail
	grow crash ||
	IFNOT
		hide_tail
		ty tx td do_step DUP2 TO tx TO ty VRAM_yx@ body_str POS IFNOT 10 TO crash ELSE 4 MOD  TO td FI
		show_tail
	THEN
	;
( head )
0 0 0 0 VALUE hx VALUE hy VALUE hd VALUE hdd
: hide_head hy hx BL VRAM_yx! ;
: show_head hy hx head_str_addr hd +21 C@ VRAM_yx! ;
: move_head
	10 WAIT hide_head
	hy hx hd ( body here )
		hy hx ( new head )
			hd KEYpress key_to_dir ( dir )
			DUP TO hdd
			do_step
		DUP2 test_body
		DUP2 test_tail
		DUP2 test_wall
		DUP2 test_fruit
		crash IF DROP DROP2 DROP2 ELSE
		TO hx TO hy hdd TO hd
		hd ( y x old new ) show_body
		THEN
	show_head ;

: snake wall show_score
	MAX_COLS /2 TO hx
	MAX_ROWS /2 TO hy
	2 TO hd
	0 TO score
	show_head
	hx 1- TO tx hy TO ty hd TO td show_tail
	0 TO crash
	BEGIN
		0 TO grow
		move_head
		move_tail
		show_fruit
		show_score
(		BEGIN KEYpress 0= UNTIL )
	crash UNTIL
	2 0 CUR_yx  crash 1 = IF ." * Avoid Walls ! *" ELSE ." * Avoid yourself *" THEN
	;
snake
