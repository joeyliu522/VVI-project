//Libraries
#include <Servo.h>

//Servo
Servo G1;
Servo G2;

//Gate vars
const int gateInitial = 1200;
int gateOpen = 0; 
int gateClosed = 0;
int gateDiff = 0; // Note: left higher than right is positive

const int steps = 12;
int degreePerStep = (gateOpen-gateClosed)/steps;
int gateCounter = 0;

int G1state = 1;
int G2state = 1;


//IR
#define S1 22 ///Gate 1 safety sensor
#define S2 23 ///Gate 2 safety sensor
#define S3 24 ///Center tube detection sensor


//Antenna relay pins 
#define A1 6
#define A2 7  
#define A3 8


//Sorter number
int sorter = 0;


void setup() {
  
  Serial.begin(9600); //Setup serial port to talk to computer
  Serial1.begin(9600); //Setup serial port to talk to RFID chip
  Serial.setTimeout(100);

  //Pin locations for each servo
  G1.attach(9);
  G2.attach(10);

  //Set gates open initially
  // G1.writeMicroseconds(gateInitial);
  // G2.writeMicroseconds(gateInitial);


  //Setting IR sensor pins as input
  pinMode(S1, INPUT);
  pinMode(S2, INPUT);
  pinMode(S3, INPUT);

  //Setting the pullup resistor for the pins so its initially high 
  digitalWrite(S1,HIGH);
  digitalWrite(S2,HIGH);
  digitalWrite(S3,HIGH);

  //Setting the pins for the relays for the antennas as outputs
  pinMode(A1, OUTPUT);
  pinMode(A2, OUTPUT);
  pinMode(A3, OUTPUT);

  //Setting all the relays for the antennas to be off initially
  digitalWrite(A1,LOW);
  digitalWrite(A2,LOW);
  digitalWrite(A3,LOW);


  Serial.println("What sorter are you checking?");
  while(Serial.available() == 0){}
  sorter = Serial.parseInt();
  
  bool valid = false;

  while (!valid){
    
  if (sorter != 1 && sorter != 2 && sorter != 3 && sorter != 4) {
  Serial.println("Invalid Entry"); 
  Serial.println();
  Serial.println("What sorter are you checking?");
  while(Serial.available() == 0){}
  sorter = Serial.parseInt();
  }

  else {
  valid = true;
  Serial.println(sorter);
  Serial.println();
  }
}

  //Setting the values for gateOpen and gateClosed based on sorter number
  if (sorter == 1){gateOpen = 1400;gateClosed = 1050;}
  else if (sorter ==2){gateOpen = 1300;gateClosed = 1600;}
  else if (sorter ==3){gateOpen = 1225; gateClosed = 1580;}
  else if (sorter ==4){gateOpen = 1350;gateClosed = 1600;}


  degreePerStep = (gateOpen-gateClosed)/steps;

  G1.writeMicroseconds(gateOpen);
  G2.writeMicroseconds(gateOpen);
  


}

void loop() {
 
  Serial.println("What would you like to check?");  //Ask user what they would like to check
  Serial.println("Antennas: A1, A2, A3  IR sensors: S1, S2, S3  Gates: G1, G2");
  Serial.println();
  
  while(Serial.available() == 0){}   //Wait for user input
  String input = Serial.readString(); //Store user input
  Serial.println(input);

  //Antenna input strings
  if (input == "A1"){CheckAntenna(A1);}
  else if (input == "A2") {CheckAntenna(A2);}
  else if (input == "A3") {CheckAntenna(A3);}

  //IR sensor input strings
  else if (input == "S1"){CheckIR(S1);}
  else if (input == "S2") {CheckIR(S2);}
  else if (input == "S3") {CheckIR(S3);}

  //Gate input strings
  else if (input == "G1"){CheckGate(G1,&G1state);}
  else if (input == "G2"){CheckGate(G2,&G2state);}

  else if (input == "T1"){
    digitalWrite(A1, HIGH);
    Serial1.write("MOF\r");
    while(Serial1.available() == 0) {}
    Serial.println(Serial1.readString());
    digitalWrite(A1, LOW);
  }

  
  else {Serial.println();Serial.println("Invalid Entry");} // If user input was not one of the input strings 
  

}



void CheckAntenna(int antenna) {
  
  String tag = "";
  String keyPress = "";
  
  Serial.println("Antenna ready");

  digitalWrite(antenna,HIGH); //Turns on relay x for antenna x

  while(Serial1.available() == 0 && Serial.available() == 0){} //Waiting for an rfid tag to be read by the antenna or a button press from user

  tag = Serial1.readString(); // storing the tag ID if there is something read
  keyPress = Serial.readString(); //storing the button press if user wants to end because nothing read


  digitalWrite(antenna,LOW); //Turns off relay x for antenna x
  
  if (tag != ""){
    Serial.print("Antenna Working! Tag ID:");
    Serial.println(tag);
    }

  Serial.println();
  
  
 }


 void CheckIR(int sensor) {

  Serial.println("Sensor ready");
  
  int currentState = digitalRead(sensor); // read from the IR detector

  if (currentState == 0) {Serial.println("Light Beam Broken");}
  else if (currentState == 1) {Serial.println("Light Beam Unbroken");}
  int previousState = currentState;
  
  while(Serial.available() == 0) {  //loop to continue checking sensor, ends when a button is pressed 
    
    currentState = digitalRead(sensor); // read from the IR detector

  // check if the sensor beam is broken
  // if it is, the currentState is LOW or 0:
  
  if (currentState && !previousState) {
    Serial.println("Light Beam Unbroken");
  } 
  if (!currentState && previousState) {
    Serial.println("Light Beam Broken");
  }
    previousState = currentState;
 }
 Serial.readString();// capture the key press
 Serial.println(); //print blank line
 
}





bool SetGateByValue (Servo G,int state){

  Serial.println("Would you like to set the gate to specific values?  Y for yes  N for no");

  bool valid = false;
  int currPos;

  while(!valid){
  
  while(Serial.available()==0){} //wait for user response
  String input = Serial.readString(); //read in input to variable
  
  if (input != "Y" && input != "N"){
  Serial.println("Invalid Entry");
  Serial.println();
    }

  else if (input == "Y"){
   valid = true; //Exit initial invalid loop
   bool cont = true;

   if (state == 0){currPos = gateClosed;}//Set current position based on the given state of the servo, needed for MoveGate function
   if (state == 1){currPos = gateOpen;} //Set current position based on the given state of the servo, needed for MoveGate function

   while (cont){ //Loop for allowing new values to be entered

   //Ask the user for servo value
   Serial.println("Input the value you want to test. Values should be between 900-2100.");
   Serial.println("You can keep entering new values.Enter any non-numeric key when you want to exit.");
   
   while(Serial.available() == 0); //Wait for user to input value
   int gateValue = Serial.parseInt(); //Store user input in var

   if (gateValue == 0){ //Exit while loop
   cont = false;    
   Serial.println(); //print blank space
   return true;
    }

   else if (gateValue >= 900 && gateValue <= 2100){Serial.println(gateValue);MoveGate(G,currPos,gateValue);currPos = gateValue;} //Write value to servo and set  current position to new gate value 

   else { Serial.println("Invalid Entry");Serial.println();} //Invalid Entry
   }
   }
   
  

  else if (input == "N"){valid = true;Serial.println(); return false; } 
  
  
  }
}


void CheckGate(Servo G,int *state) {

  //Ask user if they want to check specific gate value
  if (!SetGateByValue(G,*state)){

  
  //if gate is closed open it 
  if (*state == 0){
  MoveGate(G, gateClosed,gateOpen);
  Serial.println("open");
  Serial.println();
  *state = 1; //change the state to open
  
  }
  //if gate is open close it
  else if (*state == 1) {
  MoveGate(G, gateOpen,gateClosed);
  Serial.println("closed");
  Serial.println();
  *state = 0; //change the state to open
  }
  }

  
  }


void MoveGate(Servo G,int initPos, int finalPos) {
  
    int numSteps = (finalPos - initPos)/degreePerStep; // calculate the number of steps for a given movement
    if (numSteps == 0) {G.writeMicroseconds(finalPos);}// If the movement is very small


    else{
    if (numSteps > 0) {degreePerStep = abs(degreePerStep);} //Set degree per step as positive since we want to open
    if (numSteps < 0) {degreePerStep = -degreePerStep;numSteps = abs(numSteps);} // Set degree pers step as negative since we want to close
    

      
    while (gateCounter != numSteps){ //Loop moving the servo degree per step for numSteps
      gateCounter ++; 
      G.writeMicroseconds(initPos + gateCounter*degreePerStep);
      delay(150); // pause servo, this is what makes it moves slowly
      }
    }

  gateCounter = 0; // reset gatecounter to zero 
  }




  
  
  


  
 
