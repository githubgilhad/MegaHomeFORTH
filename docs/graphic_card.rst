.. vim: set ft=rst showbreak=»\  noexpandtab fileencoding=utf-8 nomodified   wrap textwidth=0 foldmethod=marker foldmarker={{{,}}} foldcolumn=4 ruler showcmd lcs=tab\:|- list tabstop=8 noexpandtab nosmarttab softtabstop=0 shiftwidth=0 linebreak  

Základní myšlenka
==================

* HW:
	* retropočítač/CPU - HD6309 4MHz
	* Arduino - atmega2560
	* gates - 74HC245 Octal bus tranceiver 3 state - 2 pro adresu, 1 pro data
	* GLUE - ATF1504 - 64 I/O pinů
		* GLUE obecně je v tom počítači to, co převádí jedny signály na druhé (adresu na OE příslušných obvodů a podobně) - vlastně všechno, co není CPU, RAM nebo Arduino, ale zde je to CPLD, které dělá všechno a gates, které zajišťují oddělení sběrnic. Možná časem přibudou podpůrné obvody, ale spíš ne.
	* paměť - CY7C109D-128kx8-SRAM 
		* jedna pro retropočítač se základním mapováním 0..64kB
			* oblast 8000-BFFF je překrývána podle potřeby
			* oblast C000-C??? je použita pro I/O účely
			* zbytek (C???-FFFF) je považován za ROM (a je otázka, zda do něj půjde normálně zapisovat)
		* druhá pro sdílení s CPU a s Arduinem
			* vždy do ní může v danou chvíli přistupovat maximálně jede z nich
			* gates jsou použity pro oddělení této paměti od sběrnice CPU
			* Arduino si nastaví porty do HiZ podle potřeby


* Retropočítač/CPU vidí paměť jako 32kB RAM, 16kB cosi jako EMS s benefity, několik bytů pro I/O mapování a zbytek do 64kB ROM.
* Arduino vidí 128kB externě dostupné RAM a nějaké signály
* Glue logic dělá registry a (některé) příslušné signály

* Arduino dokáže s tou externí RAM komunikovat asi tak na 1-2 MB/s ( nastavit adresu 2, nastavit OE+R/W 1, vlastní přenost 1B 1, shodit OE 1, zvýšit adresu 2, uložit ten byte 1, zvýšit interní adresu 2 ~ 9 instrukcí?)
* Arduino nedokáže dost rychle komunikovat s CPU přímo
* CPU komunikuje s tou RAM nativní rychlostí 4MHz asi tak až 1.3 MB/s ( TFM 6+3n )

Signály
=======

* A_* komunikace s Arduino
	* `A_HALT` pulldown, **LOW**, Arduino ho nastaví nahoru když už nepotřebuje haltovat CPU
	* `A_BUS` nastaví Arduino, když chce přístup na systémový bus
	* `A_READ` používá Arduino pro RAM a Shared RAM
	* `A_WRITE` používá Arduino pro RAM a Shared RAM
* C_* komunikace s CPU
	* `C_HALT` pullup
	* `C_READ` CPU chce číst nebo psát
* R_* signály pro systémovou RAM
	* `R_READ` read signal - OE, active low
	* `R_WRITE` write signal
	* `R_ENABLE` enable signal
	* `R_D[0..7]` data = `C_D[0..7]`
	* `R_A[0..16]` address = `C_A[0..11]` plus GLUE
* G_* GLUE logic
	* `G_A_DIR` a `G_A_OE` address gate dir a OE
	* `G_D_DIR` a `G_D_OE` data gate dir a OE
* S_* signály pro Shared RAM

Boot sekvence
==============

* (Reset má kondenzátor a "vyšší práh citlivosti", spíná jako poslední)
* naběhne napájecí napětí
	* `A_HALT` je pulldownem držený dole
		* GLUE logic tudíž podrží dole `C_HALT`
		* (CPU je v haltu a začne nabíhat jeho reset, všechny signály v HiZ)
		* (Arduino staruje a má všechny piny HiZ)
		* (GLUE po resetu odpojilo brány k Arduinu)
	* `A_BUS`  je pulldownem držený dole
		* GLUE pro `A_HALT`  **LOW** a `A_BUS`  **LOW** drží brány rozpojené
			* GLUE kopíruje `C_READ` do  `R_READ`
	* Clock se rozbíhá na nějakých 4 MHz
* po delší době nastartuje Arduino (věci v setup a tak)
	* `A_HALT` nastaví na **LOW** a aktivně ho tam drží (žádná změna)
	* Arduino načte z SD karty, nebo FLASH, nebo nějak obsah ROM
* Arduino začne plnit ROM
	* Arduino nastaví `A_BUS`  na **HIGH**
		* GLUE pro  `A_HALT`  **LOW** a `A_BUS`  **HIGH**
			* GLUE kopíruje `A_READ` do  `R_READ`
			* GLUE kopíruje `A_WRITE` do  `R_WRITE`
			* GLUE udržuje  `R_ENABLE` (podle hodin)
			* GLUE nepřekládá adresy, samo je má na HiZ (a data taky) (zápisy do registrů a tak jdou do podložené RAM)
				* `R_D[0..7]` `R_A[0..16]`
			* GLUE nastaví brány pro adresy na Arduino->SYS a otevře je
				* `G_A_DIR` a `G_A_OE`
			* GLUE kopíruje `A_READ` do směru brány `G_D_DIR` pro data a otevře ji
				* `G_D_DIR` a `G_D_OE`
	* LOOP:
		* Arduino nastaví adresu (a data, pokud je Arduino_R=true, dochází ke konfliktu = odpory mezi gate a arduino)
		* Arduino nastaví Arduino_R=false (zápis do sys), 
			* GLUE nastaví `R_READ` na write a otevře brány pro data -> SYS (může dojít ke konfliktu = odpory mezi gate a SYS)
		* Arduino počká dva cykly SYS (takže aspoň jeden kompletní projde s write)
		* Arduino nastaví Arduino_R=true (čtení ze SYS) (není konflikt, čte se co se zapisovalo)
		* Arduino vymyslí další data a jede znovu (klidně v nulovém čase)
	* ROM je zapsána, Arduino odpojí svoje piny pro data a adresy a nastaví `A_BUS` =**LOW**
		* GLUE pro `A_HALT`  **LOW** a `A_BUS`  **LOW** drží brány rozpojené a kopíruje `C_READ` do  `R_READ`
* Arduino předá řízení CPU
	* Arduino nastaví `A_HALT`  = **HIGH**
		* GLUE odpojí/ignoruje `A_BUS` 
		* GLUE nastaví `C_HALT` na HiZ (a vnější pullup ho vytáhne nahoru a CPU se rozběhne)

Registry
=========

* GLUE poskytuje tyto registry:
	* Source0/1 R/W
		* Source0/1 W: **zapsání** hodnoty znamená vydání požadavku na namapování daného zdroje
			* Source R je okamžitě nastaven na tuto hodnotu (možná sanitizovanou)
			* Status R je nastaven jako busy
		* Source0/1 R: vrací právě namapovaný zdroj (ať už je, či není dostupný)
	* Status0/1 R
		* 0 OK - znamená vše v pořádku
		* 1 busy - zdroj není dosud k dispozici
	* Pokud Status není OK nelze pracovat ani se starou ani s novou pamětí (lépe řečeno, není definované, co se stane)
		* Pokud se změní source, CPU nečte status, ale zdroj se připojí, je možné ho používat (= čtení Status není povinné, ale připojování může trvat libovolně dlouho, i celé sekundy třeba)
	* Je možno požadovat namapování zdroje (ať stejného či jiného) ještě před dokončením mapování předchozího.
	* Source0 / Source1 jsou pro dolních / horních 8kB mapovatelné oblasti, nezávislé
	* zdroje: rozdělení podle horního a dolního bytu
		* 0x je systémová paměť
		* 1x je Arduino 1 paměť
		* 2x je Arduino 2 paměť
		* zbytek není zatím definován
		* dolní půlka bytu říká, který 8kB blok je namapován (0..15)
	* CPU "vlastní" paměť, pokud ji má namapovanou aspoň v jednom slotu
	* CPU se "vzdá" paměti, jakmile ji namapovanou nemá
	* změna namapování paměti není zřeknutí se
	* systémovou paměť CPU vlastní pořád
	* "divná namapování" jako připojení oblasti RAM/ROM, nebo namapování stejného kusu paměti do obou slotů se chovají tak, jak to GLUE logice vyjde. Čili to nejspíš funguje správně a je jedno, kam se zapisuje a odkud čte, ROM není chráněná

`A_` něco, SYS_něco a Arduino_něco jsou signály mezi CPLD a příslušnými častmi počítače, kterým odpovídají stejně nazvané spoje. Jde o žádosti o něco, připojení někam.
Grafické nákresy dodělám časem.
Source-zdroj je to, co se namapuje do 8kB okna - blok paměti z některého z RAM chipů
v registrech je to také pojmenování registru v CPLD
Při novém zápisu CPLD přeruší (a zapomene) předchozí sekvenci a pokusí se namapovat požadovaný zdroj. 
Synchronizaci si musí zařídit CPU, opakovaným čtením Statusu (přičemž může mezitím dělat i cokoli jiného). Mapování musí čekat, dokud požadovanou RAM neuvolní Arduino, což v případě zápisu na SD kartu, nebo jiných operacích může trvat velmi dlouho. Situace je obdobná jako u sériové komunikace, kdy protistrana nevysílá a čekání na další znak může trvat, dokud se obsluha nevrátí z oběda.

Normální stav
=============

* CPU 

