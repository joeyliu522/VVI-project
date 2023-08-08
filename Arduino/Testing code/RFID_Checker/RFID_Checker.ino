/*
  LiquidCrystal Library - Hello World



  The circuit:
 * LCD RS pin to digital pin 12
 * LCD Enable pin to digital pin 11
 * LCD D4 pin to digital pin 5
 * LCD D5 pin to digital pin 4
 * LCD D6 pin to digital pin 3
 * LCD D7 pin to digital pin 2
 * LCD R/W pin to ground
 * LCD VSS pin to ground
 * LCD VCC pin to 5V
 * 10K resistor:
 * ends to +5V and ground
 * wiper to LCD VO pin (pin 3)

*/

#include <LiquidCrystal.h>
#include <SoftwareSerial.h>

const byte rxPin = 6; //Tx wire from RFID module inserted here
const byte txPin = 7; //Rx wire from RFID module inserteed here

SoftwareSerial mySerial (rxPin, txPin);

//initialize the library with the numbers of the interface pins
LiquidCrystal lcd(12, 11, 5, 4, 3, 2);
int i = 1;


void setup() {
  pinMode(rxPin, INPUT);
  pinMode(txPin, OUTPUT);
  
  lcd.begin(16, 2);

  Serial.begin(9600);
  mySerial.begin(9600);
  
  mySerial.write("SRA\r");
  lcd.print(mySerial.readString());
  
  //lcd.print("Scan ID");
}




void loop() {
  while(mySerial.available() == 0) {}
  String ID = mySerial.readString().substring(4,16);
  lcd.setCursor(0, 0);
  lcd.print("# Id's Scanned:");
  lcd.print(i);
  lcd.setCursor(0,1);
  lcd.print(ID);
  i++; 
}
