#include <Encoder.h>
#include <MsTimer2.h>

/*
  CAVE Commander - 0.0.1
  
  Getting all the input and outputs working. 
  
  1920 x 1200 px
 */

// constants won't change. They're used here to 
// set pin numbers:
const int buttonPin = 7;     // the number of the pushbutton pin
const int ledPin =  13;      // the number of the LED pin
const int extLEDPin = 8;
const int pot_0 = A1;
const int pot_1 = A0;
const int encoderPin_grn = 2;
const int encoderPin_org = 3;

const int xAxis = pot_0;
const int yAxis = pot_1;


//Setting constants
const int UPDATE_PERIOD = 100;  //(ms) period between each data update

const int X = 0;
const int Y = 1;

const int POT_CENTER = 511;  //Center value for the pot
const int MOUSE_DELAY = 2;   // 2ms delay for mouse.

const int POT_THRESHOLD = 1;     //Change in pot to register change
const int POT_RANGE[] = {1023,1023};

// variables will change:
int i = 0;
int buttonState = 0;         // variadble for reading the pushbutton status
int potVal_0 = 0;
int potVal_1 = 1;
int sentCounter = 0;
boolean mouseControl = false;

int virtualMouse[2];            //How we're tracking current mouse locations.
int oldPotVals[2];              //Tracking pot vals from past loop.
int curPotVals[2];

int maxDisplay[] = { 
  1900, 1200};                  // actual analogRead minima for {x, y}
int minDisplay[] = {0,0};           // actual analogRead maxima for {x, y}


Encoder wheel (3,2);

//Toggles Arduino controlling mouse.
// void toggleMouseMode() {
//    if (mouseControl){
//      Serial.println("Mouse Control STOP!");
//      Mouse.end(); 
//      digitalWrite(extLEDPin,LOW);
//    }
//    else {
//      Serial.println("Mouse Control Start!");
//      Mouse.begin();
//           digitalWrite(extLEDPin,HIGH);
//    }
//    mouseControl = !mouseControl;
// }
void centerMouse() {
  //Move mouse to (0,0)
    //Zero X.
  int moveBy = -50;
  for (i = 0; i < (maxDisplay[X]/abs(moveBy)); i++){
    Mouse.move(moveBy,0,0);
    delay(MOUSE_DELAY);
  }
    //Zero Y.
  for (i = 0; i < (maxDisplay[Y]/abs(moveBy)); i++){
    Mouse.move(0,moveBy,0);
    delay(MOUSE_DELAY);
  }

  //Move mouse to center
      //Center X.
  moveBy = 15;
  for (i = 0; i < (maxDisplay[X]/2)/moveBy; i++){
    Mouse.move(moveBy,0,0);
    delay(MOUSE_DELAY);
  }
    //Zero Y.
  for (i = 0; i < (maxDisplay[Y]/2)/moveBy; i++){
    Mouse.move(0,moveBy,0);
    delay(MOUSE_DELAY);
  }

  Mouse.click();

  virtualMouse[X] = maxDisplay[X]/2;
  virtualMouse[Y] = maxDisplay[Y]/2;

  Serial.println("Mouse Centered!");
}

int moveMouseAxis(int id) {
  if (abs(curPotVals[id]-oldPotVals[id]) > POT_THRESHOLD){
    int displacement = map(oldPotVals[id],0,POT_RANGE[id],0,maxDisplay[id]) - map(curPotVals[id],0,POT_RANGE[id],0,maxDisplay[id]); //The mouse displacement to get it to the new value
    oldPotVals[id] = curPotVals[id];
    return displacement;
  }
  else{
  	Serial.print("Mouse - No Pot Delta on ");
  	Serial.println(id);
    return 0;
  }
}

void sendData() {
	potVal_0 = analogRead(pot_0);
	potVal_1 = analogRead(pot_1);
	curPotVals[X] = analogRead(xAxis);
	curPotVals[Y] = analogRead(yAxis);

	//If MouseControl send commands via mouse.
	if (mouseControl) {
		int tempX = moveMouseAxis(X);
		int tempY = moveMouseAxis(Y);
		int tempW = wheel.read();
		Mouse.move(tempX,tempY,tempW);
		wheel.write(0);

		Serial.print("Sent #");
		Serial.print(sentCounter++);
		Serial.print(" @mouse || ");
		Serial.print(tempX);
		Serial.print(",");
		Serial.print(tempY);
		Serial.print(",");
		Serial.println(tempW);
	}
	else {  
		Serial.print("Sent #");
		Serial.print(sentCounter++);
		Serial.print(" || MouseControl = ");
		Serial.println(mouseControl);

		Serial.print("Pot values = ");
		Serial.print(potVal_0);
		Serial.print(", ");
		Serial.print(potVal_1);
		Serial.print(" || ");
		Serial.print("Encoder = ");
		Serial.print(digitalRead(encoderPin_grn));
		Serial.print(", ");
		Serial.println(digitalRead(encoderPin_org)); 
	}
}

void setup() {  
  pinMode(ledPin, OUTPUT);       // initialize the LED pin as an output 
  pinMode(buttonPin, INPUT);     // initialize the pushbutton pin as an input:
  pinMode(extLEDPin, OUTPUT);
  pinMode(encoderPin_grn, INPUT);
  pinMode(encoderPin_org, INPUT);
  
  //Setup MsTimer2
  MsTimer2::set(UPDATE_PERIOD, sendData);
  MsTimer2::start();
  
  //Serial.begin(9600);
  Serial.begin(19200);
  Serial.println("Start");
}

void loop() {
  // check if the pushbutton is pressed.
  // read the state of the pushbutton value:
  buttonState = digitalRead(buttonPin);
  
  // if it is, the buttonState is HIGH:
  if (buttonState == HIGH) {     
    // turn LED on:    
    digitalWrite(ledPin, HIGH);  
    // toggleMouseMode();
    if (mouseControl != true) {
      Serial.println("Mouse Control Start!");
      //Initialize Mouse Control via Arduino
      Mouse.begin();
      centerMouse();
      wheel.write(0);
      oldPotVals[X] = analogRead(xAxis);
      oldPotVals[Y] = analogRead(yAxis);

      digitalWrite(extLEDPin,HIGH); 
      mouseControl = true; 
    }
  } 
  else {
    // turn LED off:
    digitalWrite(ledPin, LOW); 

    // Stop Mouse control
    if (mouseControl != false) {
      Serial.println("Mouse Control STOP!");
      Mouse.end(); 
      digitalWrite(extLEDPin,LOW);
      mouseControl = false;
    }
  }
}

