float HeaterInputValue = 0.0;
float LEDInputValue = 0.0;
void setup() {
  // put your setup code here, to run once:
pinMode(A0,INPUT); //Heater input signal from Raspberry Pi
pinMode(A1,INPUT); //LED input signal from Raspberry Pi.

}

void loop() {
  // put your main code here, to run repeatedly:
HeaterInputValue = (analogRead(A0)/1023.0)*5.0; //Heater input signal from Raspberry Pi Converted to Volts
Serial.println(HeaterInputValue);
delay(500);
LEDInputValue = (analogRead(A1)/1023.0)*5.0; //Heater input signal from Raspberry Pi Converted to Volts
delay(500);
Serial.println(LEDInputValue);
}
