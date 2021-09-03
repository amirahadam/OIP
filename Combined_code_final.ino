// Include the Arduino Stepper.h library:
#include <Stepper.h>
// Define number of steps per rotation:
const int stepsPerRevolution = 2048;
int count=0; // Initalize variable Count
unsigned long postMillis = 0;
unsigned long currentMillis = 0;
const unsigned long period = 10000; //Set the time duration for the pump to be activated before turning off
String string1;
String data;
const int RELAY_PIN_PUMP = A5;  // the Arduino pin, which connects to the IN pin of relay
const int FAN = 3; // Declaration for Fan 
const int BUZZER = 4; //buzzer to arduino pin 9

// Create stepper object called 'myStepper', note the pin order:
Stepper myStepper = Stepper(stepsPerRevolution, 8, 10, 9, 11);
void setup() 
{  
  // Begin Serial communication at a baud rate of 9600:
  Serial.begin(9600);
  // Set the speed to 5 rpm:
  myStepper.setSpeed(5);
  // initialize pin as output.
  pinMode(5, INPUT_PULLUP); // Set pin 5 as output for Button 
  pinMode(RELAY_PIN_PUMP, OUTPUT); // Set pin A5 as output
  pinMode(FAN, OUTPUT); //set Fan - pin 3 as output
  pinMode(BUZZER, OUTPUT); // Set buzzer - pin 4 as an output
}

void loop() {
 pump();
 button1();
}

void pump() 
{
  string1="Start"; // 
  data=Serial.readStringUntil('\n'); //Read the string sent by Raspberry Pi 
  Serial.println("Start of pump loop");
  if(data == string1) // Match the string sent by Raspberry  Pi
    {
      currentMillis = millis();
      period= period + currentMillis
      if (currentMillis  < period) // If condition to follow the duration that is declared for period.
         {
          currentMillis = millis();       
          digitalWrite(RELAY_PIN_PUMP, HIGH); // Turn on pump 
         }
      else
         {
            digitalWrite(RELAY_PIN_PUMP, LOW);  // Turn off pump
         }
    }
}
void buzzer() {
  // buzzer to alert user that process is complete
  tone(BUZZER, 1000); // Send 1KHz sound signal...
  delay(5000);        // ...for 5 sec
  noTone(BUZZER);     // Stop sound...
  delay(1000);        // ...for 1sec
}

void button1()
{
  int sensorVal = digitalRead(5);
  //If button is pressed and the count variable is less than 1
  if (sensorVal == LOW) 
    {
      if (count<1)
        {
          //Stepper motor will move 180 degree anti-clockwise
          myStepper.step(stepsPerRevolution / 2);
          //Fan will be switched on
          analogWrite(FAN, 255); 
          // Count will increase by 1
          count++;
        }
        //If button is pressed and the count variable is exactly 1
       else if (count==1)
         {
            //Stepper motor will move 180 degree clockwise
            myStepper.step(-stepsPerRevolution / 2);
            //Fan will be switched off
            analogWrite(FAN, 0);
            //Run the Buzzer function
            buzzer();
            //Reset count
            count==0;
         }
   } 
}
