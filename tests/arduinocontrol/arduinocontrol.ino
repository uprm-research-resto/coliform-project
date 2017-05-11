float HeaterInputValue = 0.0;
float LEDInputValue = 0.0;
void setup() {
  // put your setup code here, to run once:
pinMode(A0,INPUT); //Heater input signal from Raspberry Pi
pinMode(A1,INPUT); //LED input signal from Raspberry Pi.
pinMode(10,OUTPUT); //Heater output signal to MOSFET
pinMode(11,OUTPUT); //LED output signal to MOSFET
}

void loop() {
  // put your main code here, to run repeatedly:
HeaterInputValue = (analogRead(A0)/1023.0)*5.0; //Heater input signal from Raspberry Pi Converted to Volts
if (HeaterInputValue >= 3.3){ //If input signal from pi is higher than 3.3 Volts, it activates the output signal
  analogWrite(10,HIGH);
  Serial.println("Heater ON");}
else analogWrite(10,LOW);


LEDInputValue = (analogRead(A1)/1023.0)*5.0; //LED input signal from Raspberry Pi Converted to Volts
if (LEDInputValue >= 3.3) {  //If input signal from pi is higher than 3.3 Volts, it activates the output signal
  analogWrite(11,HIGH);
  Serial.println("LED ON");
}
else analogWrite(11,LOW);
}
