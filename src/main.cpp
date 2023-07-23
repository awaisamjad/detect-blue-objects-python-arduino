#include <Arduino.h>


#define led_pin_green 12
#define led_pin_red 13


void setup() {
  pinMode(led_pin_green, OUTPUT);
  pinMode(led_pin_red, OUTPUT);


  Serial.begin(9600);
}


void loop() {
  if (Serial.available() > 0) {
    char receivedChar = Serial.read();


    if (receivedChar == '0') {
      digitalWrite(led_pin_red, HIGH);
      digitalWrite(led_pin_green, LOW);
    } else if (receivedChar == '1') {
      digitalWrite(led_pin_green, HIGH);
      digitalWrite(led_pin_red, LOW);
    }
  }
}
