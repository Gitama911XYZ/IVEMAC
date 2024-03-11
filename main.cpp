#include <Arduino.h>



const int Pin=2;
void setup()
{
pinMode(Pin, INPUT);
Serial.begin(9600);
}
void loop()
{
int sensorValue = digitalRead(Pin);
if(sensorValue==LOW)
{
Serial.println("Metal");
delay(100);
}
else
{
Serial.println("no metal");
delay(100);
}
}
  
