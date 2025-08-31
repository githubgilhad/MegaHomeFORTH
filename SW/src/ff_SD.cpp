#include <SPI.h>
#include <SD.h>
	#include <avr/pgmspace.h>
// #include "debug.h"
#include "../libs/bios/bios.h"
#define ERROR(X) error(F(X))
#define INFO(X) info(F(X))
extern "C" {
void wx(const  char *c); 

char wait_for_char();
void error(const  __FlashStringHelper *c); 
void info(const   __FlashStringHelper *c); 
void write_hex32(uint32_t b);
void printDirectory(File dir, int numTabs) {
  while (true) {

    File entry =  dir.openNextFile();
    if (! entry) {
      // no more files
      break;
    }
    for (uint8_t i = 0; i < numTabs; i++) {
      wx("\t");
    }
    wx(entry.name());
//    wx("entry.name");
    if (entry.isDirectory()) {
      wx("/");
      printDirectory(entry, numTabs + 1);
    } else {
      // files have sizes, directories do not
      wx("\t\t");
      write_hex32(entry.size());
      wx("\r\n");
    }
    entry.close();
  }
}

char file_ver='A';

  File myFile;
void ff_SD() {	// {{{ called by f_SD to get stack right
file_ver++;
/*
wait_for_char();
	wx("In SD ...");
wait_for_char();
	bios.wait(1);
	noInterrupts();
	wx("really In SD ...");
	interrupts();
wait_for_char();

*/
	bios.wait(1);
	noInterrupts();
	if (!SD.begin(53)) { interrupts(); wx("SD ini failed!"); return;};
	interrupts();
/*
	wx("SD ini done.");
wait_for_char();
*/
bios.wait(1);
noInterrupts();
  char * fname="0_test.txt";
  fname[0]=file_ver;
  myFile = SD.open(fname, FILE_WRITE);
  interrupts();

  // if the file opened okay, write to it:
//if (false) {
bios.wait(1);
noInterrupts();
  if (myFile) {
//    wx("Writing to test.txt...");
//    wx(fname);
    myFile.println("testing 1, 2, 3.");
    // close the file:
    myFile.close();
//    wx("done.");
  } else {
    // if the file didn't open, print an error:
    wx("error opening test.txt");
  }
interrupts();
// wait_for_char();
bios.wait(1);
noInterrupts();

wx("\r\n");
	myFile  = SD.open("/");
	printDirectory(myFile, 0);
	interrupts();
//	wx("SD Done");
}	// }}}
void ff_SD_CAT(char * name){	 // {{{
	bios.wait(1);
	noInterrupts();
	if (!SD.begin(53)) { interrupts(); wx("SD ini failed!"); return;};
	interrupts();
	//
	bios.wait(1);
	noInterrupts();
	myFile=SD.open(name, FILE_READ);
	interrupts();
	char c[2]={0,0};
	if (myFile) {
		while (myFile.available()) {
			bios.wait(1);
			noInterrupts();
			c[0]=myFile.read();
			interrupts();
			wx(c);
			};
		bios.wait(1);
		noInterrupts();
		myFile.close();
		interrupts();
	} else {
		wx("error opening file");
		wx(name);
	};
	wx("\r\n");
	
}	// }}}
}
