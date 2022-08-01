// Creator: Nilendu Saha
// KU Id: 1943079
// Topic: Toaster Circuit using Arduino


// Creating vairables for the state of the LEDs
int preState = 0;
int ledState = 0;
// Assigning pin for the smoke detection pot
int smoke_detector_pot = A1;
bool smoke_flag = false; // flag variable for smoke detection



void setup()
{
  pinMode(2, INPUT);    // Toaster Switch
  pinMode(3, INPUT);    // Lever Switch
  pinMode(12, OUTPUT);  // LEVER LED
  pinMode(13, OUTPUT);  // Toaster LED
  pinMode(4, OUTPUT);  // Smoke Detector LED
  pinMode(5, OUTPUT);  // Smoke Detector Buzzer
  
  
  pinMode(6, OUTPUT);    // LED 1 
  pinMode(7, OUTPUT);  // LED 2
  pinMode(8, OUTPUT);  // LED 3
  pinMode(9, OUTPUT);    // LED 4 
  pinMode(10, OUTPUT);  // LED 5
  pinMode(11, OUTPUT);  // LED 6
  pinMode(smoke_detector_pot, INPUT);
  Serial.begin(9600);
}

void loop()
{
  int bState = digitalRead(2);
  int y = analogRead(smoke_detector_pot); // storing the analog value of smoke detector pot
  y = map(y, 0,1023,0,255);
  if((bState == 1) && (preState == 0)){
	delay(5);
    ledState = !ledState;
  }
  digitalWrite(13, ledState);
  preState = bState;
  int x = analogRead(0); // storing the analog value of light timer pot
  int bState2 = digitalRead(3);
  if(ledState == 1 && smoke_flag == false){
  
    analogWrite(4, y);
  }
  if(ledState == 0){
  
    digitalWrite(4, LOW);
    smoke_flag = false;
  }
  
  if((ledState == 1) && (bState2 == 1)){
  
    analogWrite(4, y);
    digitalWrite(12, HIGH);
    //int toast_process = true;
    smoke_flag = lightTimer(x,y,smoke_flag);  // Browning Control
    delay(50);
    digitalWrite(12, LOW);
    if(smoke_flag == true){
    
      digitalWrite(4, LOW);
  
    }
    
   
  
}
}

// Light Timer Function

bool lightTimer(int x, int y, bool smoke_flag) {

  if(x >= 0 && x <= 164 && y <= 204 ){
  
    analogWrite(4, y);
    digitalWrite(6, HIGH);
    delay(1000);
    digitalWrite(6, LOW);
    return smoke_flag;
  }
  else if(x > 164 && x <= 348 && y <= 204){
  
    analogWrite(4, y);
    digitalWrite(6, HIGH);
    digitalWrite(7, HIGH);
    delay(1000);
    digitalWrite(7, LOW);
    delay(1000);
    digitalWrite(6, LOW);
    return smoke_flag;
  }
  else if(x > 348 && x <= 511 && y <= 204){
  
    analogWrite(4, y);
    digitalWrite(6, HIGH);
    digitalWrite(7, HIGH);
    digitalWrite(8, HIGH);
    delay(1000);
    digitalWrite(8, LOW);
    delay(1000);
    digitalWrite(7, LOW);
    delay(1000);
    digitalWrite(6, LOW);
    return smoke_flag;
  }
  else if(x > 511 && x <= 675 && y <= 204){
  
    analogWrite(4, y);
    digitalWrite(6, HIGH);
    digitalWrite(7, HIGH);
    digitalWrite(8, HIGH);
    digitalWrite(9, HIGH);
    delay(1000);
    digitalWrite(9, LOW);
    delay(1000);
    digitalWrite(8, LOW);
    delay(1000);
    digitalWrite(7, LOW);
    delay(1000);
    digitalWrite(6, LOW);
    return smoke_flag;
  }
  else if(x > 675 && x <= 859 && y <= 204){
  
    analogWrite(4, y);
    digitalWrite(6, HIGH);
    digitalWrite(7, HIGH);
    digitalWrite(8, HIGH);
    digitalWrite(9, HIGH);
    digitalWrite(10, HIGH);
    delay(1000);
    digitalWrite(10, LOW);
    delay(1000);
    digitalWrite(9, LOW);
    delay(1000);
    digitalWrite(8, LOW);
    delay(1000);
    digitalWrite(7, LOW);
    delay(1000);
    digitalWrite(6, LOW);
    return smoke_flag;
  }
  else if(x > 859 && y <= 204){
    
    analogWrite(4, y);
    digitalWrite(6, HIGH);
    digitalWrite(7, HIGH);
    digitalWrite(8, HIGH);
    digitalWrite(9, HIGH);
    digitalWrite(10, HIGH);
    digitalWrite(11, HIGH);
    delay(1000);
    digitalWrite(11, LOW);
    delay(1000);
    digitalWrite(10, LOW);
    delay(1000);
    digitalWrite(9, LOW);
    delay(1000);
    digitalWrite(8, LOW);
    delay(1000);
    digitalWrite(7, LOW);
    delay(1000);
    digitalWrite(6, LOW);
    return smoke_flag;
  
    
  }
  else if(y > 204){
    
    for(int i=5;i>=1;i--){
    
      digitalWrite(4, HIGH);
      digitalWrite(5, HIGH);
      delay(500);
      digitalWrite(4, LOW);
      //digitalWrite(5, LOW);
      delay(500);
      
    }
    digitalWrite(5, LOW);
    digitalWrite(12, LOW);
    smoke_flag = true;
    return smoke_flag;
  
  }
  
}