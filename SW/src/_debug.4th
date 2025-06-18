: p? PINE C@ 0FC AND . ; ( what is on Port E? )
: p! PORTE C! p? ; ( set port E to value on Top Of Stack (TOS) )
: pp ff PINE C! p? ; ( change all output pins on port E to other values )
: x DUP 0 PORTE C! DDRE C! PORTE C! PINE C@ FC AND . ;  ( clear output on PE, open another pin for output and set it, read the port, ignore bits 0 and 1 (RX TX) )
