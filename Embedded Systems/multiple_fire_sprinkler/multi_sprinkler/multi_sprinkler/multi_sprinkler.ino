int LED=8;
int Buzzer=9;
int PumpLine1=2;
int PumpLine2=3;
int PumpLine3=4;
int PumpLine4=5;
int serialRead=0;

unsigned long pumpCurrMillis = 0;
unsigned long pumpPrevMillis = 0;
const long pumpInterval = 3000;
unsigned long currentMillis = 0;
unsigned long previousMillis = 0;
const long interval = 200;
int ledState = LOW; 

void setup()
{
  pinMode(LED, OUTPUT);
  pinMode(Buzzer, OUTPUT);
  pinMode(PumpLine1, OUTPUT);
  pinMode(PumpLine2, OUTPUT);
  pinMode(PumpLine3, OUTPUT);
  pinMode(PumpLine4, OUTPUT);
  digitalWrite(PumpLine1, HIGH);
  //delay(500);
  digitalWrite(PumpLine2, HIGH);
  //delay(500);
  digitalWrite(PumpLine3, HIGH);
  //delay(500);
  digitalWrite(PumpLine4, HIGH);
  
  Serial.begin(9600);
}

void loop()
{
  serialRead=Serial.read();
  if(serialRead == 'a')
  {
    Blink();
    digitalWrite(PumpLine1, LOW);
    //delay(500);
    digitalWrite(PumpLine2, HIGH);
    //delay(500);
    digitalWrite(PumpLine3, HIGH);
    //delay(500);
    digitalWrite(PumpLine4, HIGH);
    //delay(500);
    pumpPrevMillis = millis();
  }

  if(serialRead == 'b')
  {
    Blink();
    digitalWrite(PumpLine1, HIGH);
    //delay(500);
    digitalWrite(PumpLine2, LOW);
    //delay(500);
    digitalWrite(PumpLine3, HIGH);
    //delay(500);
    digitalWrite(PumpLine4, HIGH);
    //delay(500);
    pumpPrevMillis = millis();
  }

  if(serialRead == 'c')
  {
    Blink();
    digitalWrite(PumpLine1, HIGH);
   // delay(500);
    digitalWrite(PumpLine2, HIGH);
    //delay(500);
    digitalWrite(PumpLine3, LOW);
    //delay(500);
    digitalWrite(PumpLine4, HIGH);
   // delay(500);
    pumpPrevMillis = millis();
  }

  if(serialRead == 'd')
  {
    Blink();
    digitalWrite(PumpLine1, HIGH);
    //delay(500);
    digitalWrite(PumpLine2, HIGH);
    //delay(500);
    digitalWrite(PumpLine3, HIGH);
    //delay(500);
    digitalWrite(PumpLine4, LOW);
   // delay(500);
    pumpPrevMillis = millis();
  }

  if(serialRead == 'e')
  {
    Blink();
    digitalWrite(PumpLine1, LOW);
    //delay(500);
    digitalWrite(PumpLine2, HIGH);
   // delay(500);
    digitalWrite(PumpLine3, HIGH);
    //delay(500);
    digitalWrite(PumpLine4, LOW);
    //delay(500);
    pumpPrevMillis = millis();
  }

  if(serialRead == 'f')
  {
    Blink();
    digitalWrite(PumpLine1, LOW);
    //delay(500);
    digitalWrite(PumpLine2, LOW);
   // delay(500);
    digitalWrite(PumpLine3, HIGH);
    //delay(500);
    digitalWrite(PumpLine4, HIGH);
    //delay(500);
    pumpPrevMillis = millis();
  }

  if(serialRead == 'g')
  {
    Blink();
    digitalWrite(PumpLine1, HIGH);
   // delay(500);
    digitalWrite(PumpLine2, LOW);
    //delay(500);
    digitalWrite(PumpLine3, LOW);
    //delay(500);
    digitalWrite(PumpLine4, HIGH);
  //  delay(500);
    pumpPrevMillis = millis();
  }

  if(serialRead == 'h')
  {
    Blink();
    digitalWrite(PumpLine1, HIGH);
    //delay(500);
    digitalWrite(PumpLine2, HIGH);
   // delay(500);
    digitalWrite(PumpLine3, LOW);
  //  delay(500);
    digitalWrite(PumpLine4, LOW);
   // delay(500);
    pumpPrevMillis = millis();
  }

  if(serialRead == 'i')
  {
    Blink();
    digitalWrite(PumpLine1, LOW);
   // delay(500);
    digitalWrite(PumpLine2, LOW);
 //   delay(500);
    digitalWrite(PumpLine3, LOW);
  //  delay(500);
    digitalWrite(PumpLine4, LOW);
  //  delay(500);
    pumpPrevMillis = millis();
  }
  
  if(serialRead == 's')
  {
    digitalWrite(LED, LOW);
    digitalWrite(Buzzer, LOW);
    pumpCurrMillis = millis();
    if ((unsigned long)(pumpCurrMillis - pumpPrevMillis) >= pumpInterval)
    {
      pumpCurrMillis = pumpPrevMillis;
      digitalWrite(PumpLine1, HIGH);
     // delay(500);
      digitalWrite(PumpLine2, HIGH);
      //delay(500);
      digitalWrite(PumpLine3, HIGH);
    //  delay(500);
      digitalWrite(PumpLine4, HIGH);
     // delay(500);
    }
    delay(20);
  }
}

void Blink()
{
  unsigned long currentMillis = millis();
  if (currentMillis - previousMillis >= interval)
  {
    previousMillis = currentMillis;
    if (ledState == LOW)
    {
      ledState = HIGH;
    }
    else
    {
      ledState = LOW;
    }
    digitalWrite(LED, ledState);
    digitalWrite(Buzzer, ledState);
  }  
}


