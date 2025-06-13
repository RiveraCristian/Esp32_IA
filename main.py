#include "ColabiOTA.h"

#define LED_PIN 12

void setup() {
  pinMode(LED_PIN, OUTPUT);
  ColabiOTA::begin();
}

void loop() {
  ColabiOTA::handle();
  digitalWrite(LED_PIN, HIGH);
  delay(1000);
  digitalWrite(LED_PIN, LOW);
  delay(1000);
}