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
	* `A_SHARE_WANTED` nastaví GLUE  **HIGH** = CPU chce Shared RAM
	* `A_SHARE_REQUEST` Arduino nastavi na **HIGH** když chce Shared RAM
	* `A_SHARE_GRANTED` GLUE nastaví na **HIGH**, když Shared RAM patří Arduinu
	* `A_SHARE_BUSY` nastaví GLUE  **HIGH** = Shared RAM patří CPU 
	* `A_SHARE_DIRTY` nastaví GLUE  **HIGH** = Shared RAM byla naposled modifikována CPU 
* C_* komunikace s CPU
	* `C_HALT` pullup
	* `C_READ` CPU chce číst nebo psát
	* `C_CLOCK` hodiny
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
	* `S_READ` read signal - OE, active low
	* `S_WRITE` write signal
	* `S_ENABLE` enable signal
	* `S_A[12..16]` address 

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
			* GLUE nastaví brány pro adresy na Arduino->SYS a otevře je
				* `G_A_DIR` a `G_A_OE`
			* GLUE kopíruje `A_READ` do směru brány `G_D_DIR` pro data a otevře ji
				* `G_D_DIR` a `G_D_OE`
			* GLUE kopíruje `A_READ` do  `R_READ` (AND `C_CLOCK` ?)
			* GLUE kopíruje `A_WRITE` do  `R_WRITE` (AND `C_CLOCK` ?)
			* strike - GLUE udržuje  `R_ENABLE` (podle hodin) - /strike `R_ENABLE` je zapojený pořád
			* GLUE nepřekládá adresy, samo je má na HiZ (a data taky) (zápisy do registrů a tak jdou do podložené RAM)
				* `R_D[0..7]` `R_A[0..16]`
	* LOOP:
		* Arduino nastaví adresu (a data, pokud je `A_READ` = true, dochází ke konfliktu = odpory mezi gate a arduino, budeme držet `A_READ` = false)
		* Arduino nastaví `A_READ` = false (zápis do sys), `A_WRITE` = true 
			* GLUE nastaví `R_READ` a `R_WRITE` a otevře brány pro data -> SYS (může dojít ke konfliktu = odpory mezi gate a SYS)
		* strike - Arduino počká dva cykly SYS (takže aspoň jeden kompletní projde s write) - /strike 
		* Arduino udělá samo cyklus, protože RAM není závislá na hodinách
		* Arduino nastaví `R_WRITE` = false (čtení ze SYS) (není konflikt, čte se co se zapisovalo)
		* Arduino vymyslí další data a jede znovu (klidně v nulovém čase)
	* ROM je zapsána, Arduino odpojí svoje piny pro data a adresy a nastaví `A_BUS` =**LOW**
		* GLUE pro `A_HALT`  **LOW** a `A_BUS`  **LOW** drží brány rozpojené a kopíruje `C_READ` do  `R_READ`
* Arduino předá řízení CPU
	* Arduino nastaví `A_HALT`  = **HIGH**
		* GLUE odpojí/ignoruje `A_BUS` 
		* GLUE nastaví `C_HALT` na HiZ (a vnější pullup ho vytáhne nahoru a CPU se rozběhne)

.. {{{ Registry


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
		* 2 OK - ale protistrana má zájem
		* 4 - protistrana zapsala data (teda, vlastnila zdroj)
	* Pokud Status AND 0001 není OK nelze pracovat ani se starou ani s novou pamětí (lépe řečeno, není definované, co se stane)
		* Pokud se změní source, CPU nečte status, ale zdroj se připojí, je možné ho používat (= čtení Status není povinné, ale připojování může trvat libovolně dlouho, i celé sekundy třeba)
	* Je možno požadovat namapování zdroje (ať stejného či jiného) ještě před dokončením mapování předchozího.
	* Source0 / Source1 jsou pro dolních / horních 8kB mapovatelné oblasti, nezávislé
	* zdroje: rozdělení podle horních a dolních bitů
		* 00xx je systémová paměť
		* 01xx je Arduino 1 paměť
		* 10xx je Arduino 2 paměť
		* zbytek není zatím definován
		* dolní půlka bytu říká, který 8kB blok je namapován (0..15)
		* xx..xxxx bity 4..5 zatím nevyužity, zapisujte 0
	* CPU "vlastní" paměť, pokud ji má namapovanou aspoň v jednom slotu
	* CPU se "vzdá" paměti, jakmile ji namapovanou nemá
	* změna namapování paměti v rámci Arduina není zřeknutí se
	* systémovou paměť CPU vlastní pořád
	* "divná namapování" jako připojení oblasti RAM/ROM, nebo namapování stejného kusu paměti do obou slotů se chovají tak, jak to GLUE logice vyjde. Čili to nejspíš funguje správně a je jedno, kam se zapisuje a odkud čte, ROM není chráněná

`A_` něco, SYS_něco a Arduino_něco jsou signály mezi CPLD a příslušnými častmi počítače, kterým odpovídají stejně nazvané spoje. Jde o žádosti o něco, připojení někam.
Grafické nákresy dodělám časem.
Source-zdroj je to, co se namapuje do 8kB okna - blok paměti z některého z RAM chipů
v registrech je to také pojmenování registru v CPLD
Při novém zápisu CPLD přeruší (a zapomene) předchozí sekvenci a pokusí se namapovat požadovaný zdroj. 
Synchronizaci si musí zařídit CPU, opakovaným čtením Statusu (přičemž může mezitím dělat i cokoli jiného). Mapování musí čekat, dokud požadovanou RAM neuvolní Arduino, což v případě zápisu na SD kartu, nebo jiných operacích může trvat velmi dlouho. Situace je obdobná jako u sériové komunikace, kdy protistrana nevysílá a čekání na další znak může trvat, dokud se obsluha nevrátí z oběda.

.. }}}


.. {{{ Vložka s umělákem



Vložka s umělákem
===================

 
Potrebuju vymyslet (a popsat) rozhrani mezi 8bitovym pocitacem (CPU) a dvema Arduiny (A a B), ktere bude delat CPLD nazvane GLUE (jako lepidlo, ktere spojuje jednotlive casti).
Ze strany CPU pujde o dve dvojice registru - (status_L, addr_L) a (status_H, addr_H) 
A dvojici registru pro chipy - status_A a status_B
Ze strany Arduin půjde o signály privadene na jejich I/O piny

Z pohledu CPU jsou v jeho pameti dve okna o velikosti 8kB (dolni (Low) na adrese 0x8000 a horni(High) na adrese 0xA000) do kterych je neco namapovane

Jsou tri chipy RAM, kazdy ma 128kB (RAM_A sdilena s Arduinem A, RAM_B sdilena s Arduinem B, RAM_C pouze pro CPU)

Kdyz chce CPU pouzit v nejakem okne nejakou pamet, zapise do prislusneho registru (napr. addr_L) pozadovanou adresu jako byte ve tvaru aa00bbbb, kde bity aa udavaji o ktery chip jde (00 RAM_C, 01 RAM_A, 10 RAM_B) a bity bbbb udavaji o kterych 8kB v ramci chipu pujde (4 horni bity adresy). 

Nasledne CPU cte v cyklu odpovidajici stavovy registr (status_L), dokud tento neukaze, ze je mozno dotycne okno pouzivat. Stavovy registr ma nasledujici bity 000wm0b
bit B je busy - 1 znamena pamet neni jeste pridelena, 0 pamet pridelena je
M znamena modified, 1 znamena ze od minuleho prideleni byla pamet modifikovana Arduinem
W je Wanted - 1 znamena, ze Arduino by do te pameti chtelo psat (treba mezitim dosla nejaka nova data zvenku)

CPU take kdykoli muze cist stavovy registr chipu (status_A/status_B), s nasledujicimi bity 00dwmac
bit A je vlastneno Arduinem - 1 znamena ano
bit C je vlastneno CPU - 1 znamena ano
M znamena modified, 1 znamena ze od minuleho prideleni byla pamet modifikovana Arduinem
W je Wanted - 1 znamena, ze Arduino by do te pameti chtelo psat (treba mezitim dosla nejaka nova data zvenku)
D je dirty - CPU tam zapsalo, ale Arduino to jeste necetlo

Pokud CPU namapuje nejakou RAM (jakozto chip), pak mu patri az do chvile, kdy bude v obou oknech namapovano neco jineho (cimz se CPU toho chipu zase vzda)

Obdobne to bude fungovat pro Arduina, Arduino si nemuze pripojit RAM, pokud ji vlastni CPU. Pokud si Arduino pripoji nejakou RAM, tak ji vlastni (a CPU si ji nemuze namapovat), dokud se ji nevzda. Kdyz si Arduino pripoji RAM, tak se predpoklada, ze ji precetlo a zapsalo. Arduino potrebuje vedet, jestli CPU do te pameti zapsalo a jestli ji CPU chce.

A potrebuju pro kazde Arduino vymyslet signaly, aby to mohlo takhle fungovat (potrebuje vedet, jestli je jeho RAM volna, jestli ji CPU chce, jestli ji CPU zapsalo)

A cele to nejak rozumne popsat.


🔸 1. Adresace RAM z pohledu CPU

CPU má dvě 8kB okna:
Název okna	Adresa v paměti CPU	Řídicí registry
Low	0x8000–0x9FFF	addr_L, status_L
High	0xA000–0xBFFF	addr_H, status_H

CPU zapisuje do addr_L / addr_H 1 byte ve tvaru:

aa00bbbb
││   └── bbbb = 4 horní bity adresy v rámci RAM (který 8kB blok z 128kB)
└┴────── aa = výběr RAM čipu:
           00 = RAM_C (pouze pro CPU)
           01 = RAM_A (sdílí s Arduino A)
           10 = RAM_B (sdílí s Arduino B)

GLUE na základě tohoto bajtu:

    Přiřadí do okna odpovídající RAM blok

    Vyhodnotí přístupové právo (jestli CPU smí, nebo ne)

    Připraví status v status_L / status_H

Struktura stavových registrů status_L / status_H:

Bit:    7 6 5 4 3 2 1 0
        0 0 0 W M 0 0 B
                    │ │
                    │ └── B (Busy): 1 = RAM není připravená pro CPU
                    └──── M (Modified): 1 = Arduino ji změnilo od posledního použití
             W (Wanted): 1 = Arduino ji chce pro zápis

🔸 2. Stavové registry Arduin: status_A, status_B

Slouží k tomu, aby CPU mohl sledovat stav každého čipu RAM sdíleného s Arduiny.

Bit:    7 6 5 4 3 2 1 0
        0 0 D W M A 0 C
          │ │ │ │ │   └ CPU own (1 = CPU má RAM)
          │ │ │ │ └── Arduino own (1 = Arduino má RAM)
          │ │ │ └──── M = modified Arduino (od posledního CPU přístupu)
          │ │ └────── W = Arduino chce RAM
          │ └──────── D = Dirty (CPU zapsalo, Arduino ještě nečetlo)

🔸 3. Signály mezi Arduiny a GLUE

Každé Arduino potřebuje rozhraní k GLUE, které mu umožní:

    Požádat o RAM

    Být informováno, jestli je RAM volná

    Být informováno, že CPU zapsalo (Dirty)

    Informovat GLUE, že RAM modifikovalo

    Informovat, že chce RAM

📟 Navržené signály pro každé Arduino (A i B):
Název signálu	Směr	Význam
REQ_RAM	Arduino → GLUE	Požadavek na přístup k RAM (Arduino si ji chce připojit)
RAM_GRANTED	GLUE → Arduino	Arduino dostalo přístup k RAM
CPU_WANTS_RAM	GLUE → Arduino	CPU by rádo mělo RAM (bit W)
CPU_DIRTY	GLUE → Arduino	CPU zapsalo (bit D), Arduino by mělo číst
ARDUINO_MODIFIED	Arduino → GLUE	Arduino zapsalo (bit M)
ARDUINO_RELEASE	Arduino → GLUE	Arduino RAM opouští (vzdává se jí)

Volitelně:

    RAM_SELECT[3:0]: 4 bity určující, který 8kB blok Arduino žádá

    CHIP_SELECT[1:0]: 2 bity pro výběr RAM_A / RAM_B

🔸 4. Pravidla vlastnictví RAM

CPU může používat RAM blok, pokud:

    Není vlastněn Arduinem (bit A = 0)

    GLUE ho připojila a nastavila status_L/H s B = 0

Arduino může používat RAM blok, pokud:

    CPU ho nemá připojený (C = 0)

    Požádá pomocí REQ_RAM, GLUE vrátí RAM_GRANTED

Vlastnictví CPU zaniká, pokud:

    Není RAM připojená ani v Low ani v High okně

Vlastnictví Arduino zaniká, pokud:

    Pošle ARDUINO_RELEASE

🔸 5. Diagram komunikace

Zjednodušeně:

      CPU                           GLUE                        Arduino A / B
       │                              │                                │
       │-- addr_L = 01_00_1010 ------>│                                │
       │                              │                                │
       │<-- status_L = ...0... ------ │ (přiděleno)                   │
       │                              │                                │
       │==> Přístup k RAM_A: blok 0xA000–0xBFFF                        │

      Arduino požaduje RAM_A:
       │                              │<----- REQ_RAM ----------------│
       │                              │----- CPU_WANTS_RAM ------>    │
       │                              │----- CPU_DIRTY --------->     │
       │                              │<---- RAM_GRANTED -----------  │
       │                              │----- A=1, C=0 ----------------│

      Arduino hotovo s RAM_A:
       │                              │<--- ARDUINO_RELEASE ----------│
       │                              │----- A=0 -------------------->│

🔸 Shrnutí komponent rozhraní
🧠 CPU:

    Řídicí registry: addr_L, status_L, addr_H, status_H, status_A, status_B

    Paměťová mapování: 8kB okna na 0x8000 a 0xA000

    Sleduje statusy, reaguje na signály M/W/D

🧱 GLUE (CPLD):

    Koordinuje přidělení RAM

    Sleduje přístupová práva a stavy (M/W/D/A/C)

    Generuje signály pro Arduina

🔧 Arduino A/B:

    I/O signály:

        REQ_RAM, ARDUINO_MODIFIED, ARDUINO_RELEASE

        vstupní: RAM_GRANTED, CPU_WANTS_RAM, CPU_DIRTY

    Sleduje status čipu přes signály, případně může číst stav přes vlastní I/O


.. }}}




Normální stav
=============

* `A_HALT` = **HIGH**
* CPU komunikuje s GLUE přez registry, uvidíme jak. Podstatné stavy:
	* CPU má namapovanou systémovou RAM, GLUE převádí `C_READ` a `C_CLOCK` na `R_READ` `R_WRITE` `R_ENABLE` a `R_A[12..16]`
	* CPU chce Shared RAM (a ta je zrovna obsazená)
		* `A_SHARE_WANTED` nastaví GLUE  **HIGH** = CPU chce Shared RAM
	* CPU chce Shared RAM (a ta je zrovna volná)
		* `A_SHARE_BUSY` nastaví GLUE  **HIGH**
		* `A_SHARE_WANTED` nastaví GLUE  **LOW** 
		* `G_A_DIR` a `G_A_OE` CPU -> Arduino
		* `G_D_DIR` a `G_D_OE` podle `C_READ`
		* `S_READ` read signal - OE, active low
		* `S_WRITE` write signal
		* `S_ENABLE` enable signal
		* `S_A[12..16]` address 
	* Arduino chce Shared RAM
		* `A_SHARE_REQUEST` Arduino nastavi na **HIGH** když chce Shared RAM
	* CPU se vzda Shared RAM
		* `A_SHARE_BUSY` nastaví GLUE  **LOW**
		* `A_SHARE_DIRTY` nastaví GLUE  **HIGH** = Shared RAM byla naposled modifikována CPU 
		* a odpojí co se zapojilo (gates ...)
	* Arduino dostane Shared RAM
		* `A_SHARE_GRANTED` GLUE nastaví na **HIGH**, když Shared RAM patří Arduinu
		* `S_ENABLE` = true
		* `S_READ` `S_WRITE` podle `A_READ` `A_WRITE`
	* Arduino vrací Shared RAM
		* `A_SHARE_REQUEST` Arduino nastavi na **LOW** když vrací Shared RAM
		* GLUE `A_SHARE_GRANTED` low
		* GLUE uvolní zdroje



